import simplejson as json
import pandas as pd
import datetime as dt
import base64
import gzip


class Util:

    @staticmethod
    def compress(value, widget):
        res = (base64.encodebytes(gzip.compress(
            (value).encode('utf-8'), compresslevel=9))).decode('utf-8')
        return res

    @staticmethod
    def data_from_json(value, widget):
        return json.loads(gzip.decompress(value))

    @staticmethod
    def is_df(data):
        if isinstance(data, pd.core.frame.DataFrame):
            return True
        return False

    @staticmethod
    def strip_comments(code):
        lines = code.split('\n')
        lines = [e.strip() for e in lines]
        lines = [e for e in lines if not e.startswith('//')]
        code = '\n'.join(lines)
        return code

    @staticmethod
    def sanitize_str(string):
        string2 = Util.strip_comments(string)
        string2 = string2.replace('\n', '')
        string2 = string2.replace('\t', ' ')
        string2 = string2.replace('\"', '\'')
        return string2

    @staticmethod
    def sanitize_struct(e):
        if isinstance(e, (list, tuple)):
            return [Util.sanitize_struct(sub_e) for sub_e in e]
        elif isinstance(e, dict):
            return {k: Util.sanitize_struct(v) for k, v in e.items()}
        elif isinstance(e, str):
            return Util.sanitize_str(e)
        else:
            return e

    @staticmethod
    def json_serial(obj):
        """
        """
        if isinstance(obj, (dt.datetime, dt.date, pd.Timestamp)):
            return obj.isoformat()

        return obj

    @staticmethod
    def build_options(options):
        options = Util.sanitize_struct(options)
        # options_json = json.dumps(options,
        #                           default=Util.json_serial,
        #                           ignore_nan=True)
        options_json = pd.io.json.dumps(options)
        return options_json

    @staticmethod
    def build_data(data):
        data = Util.sanitize_struct(data)
        # data_json = json.dumps(data,
        #                        default=Util.json_serial,
        #                        ignore_nan=True)
        data_json = pd.io.json.dumps(data)
        return data_json
