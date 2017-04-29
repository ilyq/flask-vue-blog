# coding:utf-8

import uuid
import logging
from datetime import datetime
from sqlalchemy.inspection import inspect


def get_random_token():
    '''生成token'''
    return uuid.uuid4().hex


def dump_datetime(value):
    '''时间转换'''
    if value is None:
        return None
    return [value.strftime('%Y-%m-%d'), value.strftime("%H:%M:%S")]


def to_json(obj, related=False, summary=False):
    '''序列化model
    http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    '''
    def core(model_ojb):
        tmp = {}
        try:
            if related:
                for column in inspect(model_ojb).attrs.keys():
                    value = getattr(model_ojb, column)
                    if str(column) == 'body':
                        if summary:
                            result = value[:250].encode('utf-8')
                            if not result.count('```') / 2:
                                result += '```'
                            tmp[column] = result
                        else:
                            tmp[column] = value.encode('utf-8')
                    else:
                        if isinstance(value, datetime):
                            tmp[column] = value.strftime('%Y-%m-%d %H:%M:%S')
                        elif isinstance(value, int):
                            tmp[column] = value
                        elif isinstance(value, unicode):
                            tmp[column] = value.encode('utf-8')
                        else:
                            tmp[column] = str(getattr(model_ojb, column))
            else:
                for column in model_ojb.__table__.columns:
                    value = getattr(model_ojb, column.name)
                    if isinstance(value, datetime):
                        tmp[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        tmp[column.name] = value
            return tmp
        except Exception as e:
            logging.error(e)
            return tmp

    if hasattr(obj, '__iter__'):
        data = []
        for r in obj:
            data.append(core(r))
        return data
    else:
        return core(obj)


def paginate(obj, page=1, per_page=10, error_out=False, related=False, summary=False):
    '''分页'''
    query = obj.paginate(page=int(page), per_page=int(per_page), error_out=error_out)
    data = {
        "page": query.page,  # 当前是第几页
        "pages": query.pages,  # 总共多少页
        "per_page": query.per_page,  # 每页多少数据
        "has_next": query.has_next,  # 是否有下一页数据
        "has_prev": query.has_prev,  # 是否有前一页数据
        "total": query.total,  # 总共多少数据
        "data": to_json(query.items, related=related, summary=summary)
    }
    return data
