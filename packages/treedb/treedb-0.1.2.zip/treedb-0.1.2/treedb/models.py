# models.py - sqlalchemy schema, loading, checking, and queries for sqlite3 db

from __future__ import unicode_literals

import sqlalchemy as sa

from sqlalchemy import (Table, Column, ForeignKey, CheckConstraint,
                        Integer, Float, String, Text, Enum, DateTime, Date,
                        UniqueConstraint, Index)

from sqlalchemy.orm import relationship, aliased

from .backend import Model

__all__ = ['LEVEL', 'Languoid']

FAMILY, LANGUAGE, DIALECT = LEVEL = ('family', 'language', 'dialect')

BOOKKEEPING = 'Bookkeeping'

SPECIAL_FAMILIES = (
    'Unattested',
    'Unclassifiable',
    'Pidgin',
    'Mixed Language',
    'Artificial Language',
    'Speech Register',
    'Sign Language',
)

MACROAREA = {
    'North America', 'South America',
    'Eurasia',
    'Africa',
    'Australia', 'Papunesia',
}

LINK_SCHEME = {'https', 'http'}

SOURCE_PROVIDER = {'glottolog'}

ALTNAME_PROVIDER = {
    'multitree', 'lexvo', 'hhbib_lgcode',
    'wals', 'wals other', 'moseley & asher (1994)', 'ruhlen (1987)',
    'glottolog', 'ethnologue', 'elcat',
}

TRIGGER_FIELD = {'lgcode', 'inlg'}

IDENTIFIER_SITE = {
    'multitree', 'endangeredlanguages',
    'wals', 'languagelandscape',
}

CLASSIFICATION = {
    'sub': (False, 'sub'), 'subrefs': (True, 'sub'),
    'family': (False, 'family'), 'familyrefs': (True, 'family')
}

CLASSIFICATION_KIND = {c for _, c in CLASSIFICATION.values()}

ENDANGERMENT_STATUS = (
    'not endangered',
    'threatened', 'shifting',
    'moribund', 'nearly extinct',
    'extinct',
)

ENDANGERMENT_SOURCE = {'E20', 'E21', 'E22', 'ElCat', 'UNESCO', 'Glottolog'}

EL_COMMENT_TYPE = {'Missing', 'Spurious'}

ISORETIREMENT_REASON = {'split', 'merge', 'duplicate', 'non-existent', 'change'}


class Languoid(Model):

    __tablename__ = 'languoid'

    id = Column(String(8), CheckConstraint('length(id) = 8'), primary_key=True)

    name = Column(String, CheckConstraint("name != ''"), nullable=False, unique=True)

    level = Column(Enum(*LEVEL), nullable=False)

    parent_id = Column(ForeignKey('languoid.id'), index=True)

    hid = Column(Text, CheckConstraint('length(hid) >= 3'), unique=True)
    iso639_3 = Column(String(3), CheckConstraint('length(iso639_3) = 3'), unique=True)
    latitude = Column(Float, CheckConstraint('latitude BETWEEN -90 AND 90'))
    longitude = Column(Float, CheckConstraint('longitude BETWEEN -180 AND 180'))

    __table_args__ = (
        CheckConstraint('(latitude IS NULL) = (longitude IS NULL)'),
    )

    def __repr__(self):
        hid_iso = ['%s=%r' % (n, getattr(self, n)) for n in ('hid', 'iso639_3') if getattr(self, n)]
        return '<%s id=%r level=%r name=%r%s>' % (self.__class__.__name__,
            self.id, self.level, self.name, ' ' + ' '.join(hid_iso) if hid_iso else '')

    parent = relationship('Languoid', remote_side=[id])

    children = relationship('Languoid', remote_side=[parent_id], order_by=id)

    macroareas = relationship('Macroarea',
                              secondary='languoid_macroarea',
                              order_by='Macroarea.name',
                              back_populates='languoids')

    countries = relationship('Country',
                             secondary='languoid_country',
                             order_by='Country.id',
                             back_populates='languoids')

    links = relationship('Link',
                         order_by='Link.ord',
                         back_populates='languoid')

    sources = relationship('Source',
                           order_by='[Source.provider, Source.ord]',
                           back_populates='languoid')

    altnames = relationship('Altname',
                            order_by='[Altname.provider, Altname.ord]',
                            back_populates='languoid')

    triggers = relationship('Trigger',
                            order_by='[Trigger.field, Trigger.ord]',
                            back_populates='languoid')

    identifiers = relationship('Identifier',
                               order_by='Identifier.site',
                               back_populates='languoid')

    subclassificationcomment = relationship('ClassificationComment', uselist=False,
        primaryjoin="and_(ClassificationComment.languoid_id == Languoid.id, ClassificationComment.kind == 'sub')")

    subclassificationrefs = relationship('ClassificationRef', order_by='ClassificationRef.ord',
        primaryjoin="and_(ClassificationRef.languoid_id == Languoid.id, ClassificationRef.kind == 'sub')")

    familyclassificationcomment = relationship('ClassificationComment', uselist=False,
        primaryjoin="and_(ClassificationComment.languoid_id == Languoid.id, ClassificationComment.kind == 'family')")

    familyclassificationrefs = relationship('ClassificationRef', order_by='ClassificationRef.ord',
        primaryjoin="and_(ClassificationRef.languoid_id == Languoid.id, ClassificationRef.kind == 'family')")

    endangerment = relationship('Endangerment',
                                uselist=False,
                                back_populates='languoid')

    ethnologue_comment = relationship('EthnologueComment',
                                      uselist=False,
                                      back_populates='languoid')

    iso_retirement = relationship('IsoRetirement',
                                  uselist=False,
                                  back_populates='languoid')

    @classmethod
    def tree(cls, include_self=False, with_steps=False, with_terminal=False):
        Child, Parent = (aliased(cls, name=n) for n in ('child', 'parent'))

        tree_1 = sa.select([Child.id.label('child_id')])

        if include_self:
            parent_id = Child.id
        else:
            parent_id = Child.parent_id
            tree_1.append_whereclause(parent_id != None)
        tree_1.append_column(parent_id.label('parent_id'))

        if with_steps:
            steps = 0 if include_self else 1
            tree_1.append_column(sa.literal(steps).label('steps'))

        if with_terminal:
            if include_self:
                terminal = sa.type_coerce(Child.parent_id == None, sa.Boolean)
            else:
                terminal = sa.literal(False)
            tree_1.append_column(terminal.label('terminal'))

        tree_1 = tree_1.cte('tree', recursive=True)

        tree_2 = sa.select([tree_1.c.child_id, Parent.parent_id])\
            .select_from(tree_1.join(Parent, Parent.id == tree_1.c.parent_id))\
            .where(Parent.parent_id != None)

        if with_steps:
            tree_2.append_column((tree_1.c.steps + 1).label('steps'))

        if with_terminal:
            Granny = aliased(Languoid, name='grandparent')

            tree_2.append_column((Granny.parent_id == None).label('terminal'))
            tree_2 = tree_2.select_from(tree_2.froms[-1]
                .outerjoin(Granny, Granny.id == Parent.parent_id))

        return tree_1.union_all(tree_2)

    @classmethod
    def path(cls, label='path', delimiter='/', include_self=True, bottomup=False, _tree=None):
        tree = _tree
        if tree is None:
            tree = cls.tree(include_self=include_self, with_steps=True, with_terminal=False)

        squery = sa.select([tree.c.parent_id.label('path_part')])\
            .where(tree.c.child_id == cls.id).correlate(cls)\
            .order_by(tree.c.steps if bottomup else tree.c.steps.desc())

        path = sa.func.group_concat(squery.c.path_part, delimiter)
        return sa.select([path]).label(label)

    @classmethod
    def path_family_language(cls, path_label='path', path_delimiter='/', include_self=True, bottomup=False,
                             family_label='family_id', language_label='language_id'):
        tree = cls.tree(include_self=include_self, with_steps=True, with_terminal=True)

        path = cls.path(label=path_label, delimiter=path_delimiter, bottomup=bottomup, _tree=tree)

        family = sa.select([tree.c.parent_id])\
            .where(tree.c.child_id == cls.id).correlate(cls)\
            .where(tree.c.steps > 0).where(tree.c.terminal == True)

        Ancestor = aliased(Languoid, name='ancestor')

        language = sa.select([tree.c.parent_id])\
            .where(tree.c.child_id == cls.id).correlate(cls)\
            .where(cls.level == DIALECT)\
            .where(sa.exists()
                .where(Ancestor.id == tree.c.parent_id)
                .where(Ancestor.level == LANGUAGE))

        return path, family.label(family_label), language.label(language_label)


class Macroarea(Model):

    __tablename__ = 'macroarea'

    name = Column(Enum(*sorted(MACROAREA)), primary_key=True)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)

    languoids = relationship('Languoid',
                             secondary='languoid_macroarea',
                             order_by='Languoid.id',
                             back_populates='macroareas')


languoid_macroarea = Table('languoid_macroarea', Model.metadata,
    Column('languoid_id', ForeignKey('languoid.id'), primary_key=True),
    Column('macroarea_name', ForeignKey('macroarea.name'), primary_key=True))


class Country(Model):

    __tablename__ = 'country'

    id = Column(String(2), CheckConstraint('length(id) = 2'), primary_key=True)

    name = Column(Text, CheckConstraint("name != ''"), nullable=False, unique=True)

    def __repr__(self):
        return '<%s id=%r name=%r>' % (self.__class__.__name__, self.id, self.name)

    languoids = relationship('Languoid',
                             secondary='languoid_country',
                             order_by='Languoid.id',
                             back_populates='countries')


languoid_country = Table('languoid_country', Model.metadata,
    Column('languoid_id', ForeignKey('languoid.id'), primary_key=True),
    Column('country_id', ForeignKey('country.id'), primary_key=True))


class Link(Model):

    __tablename__ = 'link'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    ord = Column(Integer, CheckConstraint('ord >= 1'), primary_key=True)

    url = Column(Text, CheckConstraint("url != ''"), nullable=False)

    title = Column(Text, CheckConstraint("title != ''"))
    scheme = Column(Text, Enum(*sorted(LINK_SCHEME)))

    __table_args__ = (
        UniqueConstraint(languoid_id, url),
        CheckConstraint("substr(url, 1, length(scheme) + 3) = scheme || '://'"),
    )

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='links')

    def __repr__(self):
        return '<%s languoid_id=%r ord=%r url=%r title=%r scheme=%r>' % (
            self.__class__.__name__,
            self.languoid_id, self.ord, self.url, self.title, self.scheme)

    @classmethod
    def printf(cls):
        return sa.case([
            (cls.title != None,
                sa.func.printf('(%s)[%s]', cls.title, cls.url)),
            ], else_=cls.url)


class Source(Model):

    __tablename__ = 'source'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    provider = Column(Text, Enum(*sorted(SOURCE_PROVIDER)), primary_key=True)
    bibfile = Column(Text, CheckConstraint("bibfile != ''"), primary_key=True)
    bibkey = Column(Text, CheckConstraint("bibkey != ''"), primary_key=True)

    ord = Column(Integer, CheckConstraint('ord >= 1'), nullable=False)

    pages = Column(Text, CheckConstraint("pages != ''"))
    trigger = Column(Text, CheckConstraint("trigger != ''"))

    __table_args__ = (
        UniqueConstraint(languoid_id, provider, ord),
    )

    def __repr__(self):
        return '<%s languoid_id=%r povider=%r bibfile=%r bibkey=%r>' % (self.__class__.__name__,
            self.languoid_id, self.provider, self.bibfile, self.bibkey)

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='sources')

    @classmethod
    def printf(cls):
        return sa.case([
            (sa.and_(cls.pages != None, cls.trigger != None),
                 sa.func.printf('**%s:%s**:%s<trigger "%s">', cls.bibfile, cls.bibkey, cls.pages, cls.trigger)),
            (cls.pages != None,
                 sa.func.printf('**s:%s**:%s', cls.bibfile, cls.bibkey, cls.pages)),
            (cls.trigger != None,
                 sa.func.printf('**%s:%s**<trigger "%s">', cls.bibfile, cls.bibkey, cls.trigger)),
            ], else_=sa.func.printf('**%s:%s**', cls.bibfile, cls.bibkey))


class Altname(Model):

    __tablename__ = 'altname'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    provider = Column(Text, Enum(*sorted(ALTNAME_PROVIDER)), primary_key=True)
    lang = Column(String(3), CheckConstraint("length(lang) IN (0, 2, 3) OR lang = '!'"), primary_key=True)
    name = Column(Text, CheckConstraint("name != ''"), primary_key=True)

    ord = Column(Integer, CheckConstraint('ord >= 1'), nullable=False)

    __table_args__ = (
        UniqueConstraint(languoid_id, provider, ord),
    )

    def __repr__(self):
        return '<%s languoid_id=%r povider=%r lang=%r name=%r>' % (self.__class__.__name__,
            self.languoid_id, self.provider, self.lang, self.name)

    languoid = relationship('Languoid', innerjoin=True,
                            back_populates='altnames')

    @classmethod
    def printf(cls):
        return sa.case([
            (cls.lang == '',
                 cls.name),
            (sa.between(sa.func.length(cls.lang), 2, 3),
                 sa.func.printf('%s [%s]', cls.name, cls.lang)),
            ], else_=cls.name)


class Trigger(Model):

    __tablename__ = 'trigger'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    field = Column(Enum(*sorted(TRIGGER_FIELD)), primary_key=True)
    trigger = Column(Text, CheckConstraint("trigger != ''"), primary_key=True)

    ord = Column(Integer, CheckConstraint('ord >= 1'), nullable=False)

    __table_args__ = (
        UniqueConstraint(languoid_id, field, ord),
    )

    def __repr__(self):
        return '<%s languoid_id=%r field=%r trigger=%r>' % (self.__class__.__name__,
            self.languoid_id, self.field, self.trigger)

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='triggers')


class Identifier(Model):

    __tablename__ = 'identifier'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    site = Column(Enum(*sorted(IDENTIFIER_SITE)), primary_key=True)

    identifier = Column(Text, CheckConstraint("identifier != ''"), nullable=False)

    def __repr__(self):
        return '<%s languoid_id=%r site=%r identifier=%r>' % (self.__class__.__name__,
            self.languoid_id, self.site, self.identifier)

    languoid = relationship('Languoid', innerjoin=True,
                             back_populates='identifiers')


class ClassificationComment(Model):

    __tablename__ = 'classificationcomment'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    kind = Column(Enum(*sorted(CLASSIFICATION_KIND)), primary_key=True)

    comment = Column(Text, CheckConstraint("comment != ''"), nullable=False)

    def __repr__(self):
        return '<%s languoid_id=%r kind=%r comment=%r>' % (self.__class__.__name__,
            self.languoid_id, self.kind, self.comment)

    languoid = relationship('Languoid', innerjoin=True)


class ClassificationRef(Model):

    __tablename__ = 'classificationref'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)
    kind = Column(Enum(*sorted(CLASSIFICATION_KIND)), primary_key=True)
    bibfile = Column(Text, CheckConstraint("bibfile != ''"), primary_key=True)
    bibkey = Column(Text, CheckConstraint("bibkey != ''"), primary_key=True)

    ord = Column(Integer, CheckConstraint('ord >= 1'), nullable=False)

    pages = Column(Text, CheckConstraint("pages != ''"))

    __table_args__ = (
        UniqueConstraint(languoid_id, kind, ord),
    )

    def __repr__(self):
        return '<%s languoid_id=%r kind=%r bibfile=%r bibkey=%r>' % (self.__class__.__name__,
            self.languoid_id, self.kind, self.bibfile, self.bibkey)

    languoid = relationship('Languoid', innerjoin=True)

    @classmethod
    def printf(cls):
        format_ = sa.case([(cls.pages != None, '**s:%s**:%s')], else_='**%s:%s**')
        return sa.func.printf(format_, cls.bibfile, cls.bibkey, cls.pages)


class Endangerment(Model):

    __tablename__ = 'endangerment'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)

    status = Column(Enum(*ENDANGERMENT_STATUS), nullable=False)
    source = Column(Enum(*sorted(ENDANGERMENT_SOURCE)), nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(Text, CheckConstraint("comment != ''"), nullable=False)

    def __repr__(self):
        return '<%s languoid_id=%r status=%r source=%r date=%r>' % (self.__class__.__name__,
            self.languoid_id, self.status, self.source, self.date)

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='endangerment')


class EthnologueComment(Model):

    __tablename__ = 'ethnologuecomment'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)

    isohid = Column(Text, CheckConstraint('length(isohid) >= 3'), nullable=False)
    comment_type = Column(Enum(*sorted(EL_COMMENT_TYPE)), nullable=False)
    ethnologue_versions = Column(Text, CheckConstraint('length(ethnologue_versions) >= 3'), nullable=False)
    comment = Column(Text, CheckConstraint("comment != ''"), nullable=False)

    def __repr__(self):
        return '<%s languoid_id=%r isohid=%r comment_type=%r ethnologue_versions=%r>' % (self.__class__.__name__,
            self.languoid_id, self.isohid, self.comment_type, self.ethnologue_versions)

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='ethnologue_comment')


class IsoRetirement(Model):

    __tablename__ = 'isoretirement'

    languoid_id = Column(ForeignKey('languoid.id'), primary_key=True)

    code = Column(String(3), CheckConstraint('length(code) = 3'), nullable=False)
    name = Column(Text, CheckConstraint("name != ''"), nullable=False)

    change_request = Column(String(8), CheckConstraint("change_request LIKE '____-___' "))

    effective = Column(Date, nullable=False)
    reason = Column(Enum(*sorted(ISORETIREMENT_REASON)), nullable=False)

    remedy = Column(Text, CheckConstraint("remedy != ''"))
    comment = Column(Text, CheckConstraint("comment != ''"))

    __table_args__ = (
        # TODO: fix disagreement
        Index('change_request_key', sa.func.coalesce(change_request, effective)),
        CheckConstraint("remedy IS NOT NULL OR reason = 'non-existent'"),
    )

    def __repr__(self):
        return '<%s languoid_id=%r code=%r name=%r change_request=%r effective=%r reason=%r remedy=%r>' % (
            self.__class__.__name__, self.languoid_id, self.code, self.name, self.change_request,
            self.effective, self.reason, self.remedy)

    languoid = relationship('Languoid',
                            innerjoin=True,
                            back_populates='iso_retirement')

    change_to = relationship('IsoRetirementChangeTo',
                             order_by='IsoRetirementChangeTo.ord',
                             back_populates='iso_retirement')


class IsoRetirementChangeTo(Model):

    __tablename__ = 'isoretirement_changeto'

    languoid_id = Column(ForeignKey('isoretirement.languoid_id'), primary_key=True)
    code = Column(String(3), CheckConstraint('length(code) = 3'), primary_key=True)

    ord = Column(Integer, CheckConstraint('ord >= 1'), nullable=False)

    __table_args__ = (
        UniqueConstraint('languoid_id', 'ord'),
    )

    def __repr__(self):
        return '<%s languoid_id=%r code=%r>' % (self.__class__.__name__,
            self.languoid_id, self.code)

    iso_retirement = relationship('IsoRetirement',
                                  innerjoin=True,
                                  back_populates='change_to')
