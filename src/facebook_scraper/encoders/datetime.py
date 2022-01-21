from datetime import datetime
from json import JSONEncoder


class DateEncoder(JSONEncoder):
    def default(self, date):
        if isinstance(date, datetime):
            return date.isoformat()
