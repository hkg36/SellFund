from jinja2 import Environment, FileSystemLoader
import json
import datetime

jinja2_env = Environment(loader=FileSystemLoader('templates'),auto_reload=True)

class AutoFitJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)

DefJsonEncoder=AutoFitJson(skipkeys=False,
    check_circular=True,
    allow_nan=True,
    indent=None,
    encoding='utf-8',
    default=None,ensure_ascii=False,separators=(',', ':'))