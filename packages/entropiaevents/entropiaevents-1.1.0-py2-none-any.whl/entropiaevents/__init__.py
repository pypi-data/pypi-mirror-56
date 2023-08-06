import requests
import json
import re

from obelixtools import API

class WikiEvents:
    API_URL = 'https://entropia.de/api.php?format=json&action=parse&page=Vorlage:Termine'

    def __init__(self):
        self._api = API(WikiEvents.API_URL, 'json')
        self._api.query()
        self._html = self._api.content['parse']['text']['*'].replace("\n", "")
        self._parse_rows()
        self._parse_events()

    def _parse_rows(self):
        row_re = re.compile("<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>")
        self._rows = row_re.finditer(self._html, re.I)

    def _strip_html(self, data):
        return re.sub('<[^<]+?>', '', data)

    def _parse_events(self):
        self._events = []
        for row in self._rows:
            date, time, place, desc = [self._strip_html(col).strip() for col in row.groups()]
            self._events.append(dict(date=date, time = time, place=place, desc=desc))

    def to_json_file(self, filename):
        with file(filename, 'wb') as f:
            f.write(json.dumps(self.events, ensure_ascii=False).encode('utf8'))

    @property
    def events(self):
        return self._events
