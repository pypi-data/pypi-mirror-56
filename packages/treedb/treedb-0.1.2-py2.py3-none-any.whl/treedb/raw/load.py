# load.py

from __future__ import unicode_literals

import logging

from .._compat import iteritems

from sqlalchemy import insert

from .. import files as _files
from .. import tools as _tools

from .models import File, Option, Value, Fields

__all__ = ['load']


log = logging.getLogger(__name__)


class Options(dict):
    """Insert optons on demand and cache id and lines config."""

    def __init__(self, items=(), insert=None):
        super(Options, self).__init__(items)
        self.insert = insert

    def __missing__(self, key):
        log.debug('insert option %r', key)

        section, option = key
        is_lines = Fields.is_lines(section, option)

        id_, = self.insert(section=section, option=option,
                           is_lines=is_lines).inserted_primary_key

        self[key] = result = (id_, is_lines)
        return result


def itervalues(cfg, file_id, options):
    get_line = _tools.next_count(start=1)
    for section, sec in iteritems(cfg):
        for option, value in iteritems(sec):
            option_id, is_lines = options[section, option]
            if is_lines:
                for v in value.strip().splitlines():
                    yield {'file_id': file_id, 'option_id': option_id,
                           'line': get_line(), 'value': v}
            else:
                yield {'file_id': file_id, 'option_id': option_id,
                       'line': get_line(), 'value': value}


def load(root, conn):
    insert_file = insert(File, bind=conn).execute

    options = Options(insert=insert(Option, bind=conn).execute)

    insert_value = insert(Value, bind=conn).execute

    for path_tuple, dentry, cfg in _files.iterfiles(root):
        file_params = {
            'glottocode': path_tuple[-1],
            'path': '/'.join(path_tuple),
            'size': dentry.stat().st_size,
            'sha256': _tools.sha256sum(dentry.path, raw=True).hexdigest(),
        }
        file_id, = insert_file(file_params).inserted_primary_key

        value_params = list(itervalues(cfg, file_id, options))
        insert_value(value_params)
