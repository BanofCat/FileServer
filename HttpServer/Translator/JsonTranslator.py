from HttpServer.Translator.BaseTranslator import BaseTranslator
import json
import decimal
from datetime import datetime, date
from sqlalchemy.orm.dynamic import AppenderQuery
from flask_sqlalchemy import BaseQuery, DeclarativeMeta
from SQLManager import sql_object


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            counter = 0
            for field in [x for x in dir(o) if not x.startswith('_') and x != 'metadata']:
                data = o.__getattribute__(field)
                counter += 1
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:

                    if isinstance(data, datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S.%F")[:-3]
                    elif isinstance(data, date):
                        fields[field] = data.strftime("%Y-%m-%d")
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = float(data)
                    elif isinstance(data, BaseQuery):
                        pass
                    elif isinstance(data, AppenderQuery):
                        pass
                    elif isinstance(data, type):
                        pass
                    elif isinstance(data, type(JsonEncoder.default)):
                        pass
                    elif isinstance(data, sql_object.Model):
                        pass
                    else:
                        fields[field] = JsonEncoder.default(self, data)
            return fields
        return json.JSONEncoder.default(self, o)




class JsonTranslator(BaseTranslator):

    @classmethod
    def obj2package(cls, obj):
        pass

    @classmethod
    def package2obj(cls, package):
        pass


