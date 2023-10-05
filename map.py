from datetime import datetime as dt, timezone
import json
import os

import folium
from folium.plugins import MarkerCluster


class Map:
    def __init__(self, path_to_save: str = './map.html', path_to_data: str = 'Records.json') -> None:
        if not path_to_save.endswith('.html'):
            self.path_to_save = './map.html'
        else:
            self.path_to_save = path_to_save
        self.path_to_data = path_to_data
        self.map = None
        self.data = []
        self.sources = set()
        # self.tz = dt.now(timezone.utc).astimezone().tzinfo

    @staticmethod
    def _len(x1: int, y1: int, x2: int, y2: int) -> float:
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    @property
    def _load_data(self) -> list:
        with open(self.path_to_data, 'r', encoding='utf8') as f:
            data = json.load(f)['locations']

        return data

    def analysis(self) -> None:
        self.data = []
        self.sources = set()
        data = self._load_data
        before = {}

        for d in data:
            if d['deviceTag'] in before:
                if all((
                    100 >= self._len(d['latitudeE7'], d['longitudeE7'], before[d['deviceTag']]['latitudeE7'], before[d['deviceTag']]['longitudeE7'] ),
                    d['source'] == before[d['deviceTag']]['source'],
                )):
                    date = dt.fromisoformat(d['timestamp'][:-1])
                    # date = date.astimezone(timezone.utc)
                    # date = date.astimezone(self.tz)
                    date = date.strftime('%Y.%m.%d %H:%M:%S')
                    self.data[before[d['deviceTag']]['num'] - len(self.data) - 1]['dt_end'] = date
                    continue

            latitudeE7 = d['latitudeE7']
            longitudeE7 = d['longitudeE7']
            if latitudeE7 > 900000000:
                latitudeE7 -= 4294967296
            if longitudeE7 > 1800000000:
                longitudeE7 -= 4294967296
            latitudeE7 /= 10000000
            longitudeE7 /= 10000000

            date = dt.fromisoformat(d['timestamp'][:-1])
            # date = date.astimezone(timezone.utc)
            # date = date.astimezone(self.tz)
            date = date.strftime('%Y.%m.%d %H:%M:%S')

            if d['source'] not in self.sources:
                self.sources.add(d['source'])

            self.data.append({
                'coordinates': (latitudeE7, longitudeE7),
                'dt': date,
                'source': d['source'],
            })

            before[d['deviceTag']] = {
                'latitudeE7': d['latitudeE7'],
                'longitudeE7': d['longitudeE7'],
                'source': d['source'],
                'num': len(self.data),
            }

    def create_map(self) -> None:
        coordinates_of_center = self.data[0]['coordinates']
        self.map = folium.Map(location=coordinates_of_center, tiles=None, min_zoom=2, max_zoom=22, zoom_start=2, )

        tiles = (
            'OpenStreetMap',
            'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor',
            'CartoDB positron', 'CartoDB dark_matter',
        )
        for i in tiles:
            folium.TileLayer(i, min_zoom=2, max_zoom=22, zoom_start=2, name=i).add_to(self.map)

        marker_clusters = {}
        for i in self.sources:
            marker_clusters[i] = MarkerCluster(name=i, ).add_to(self.map)
        # folium.Marker(location=coordinates_of_center, popup='Center', icon=folium.Icon(color='red')).add_to(self.map)
        for i in self.data:
            if 'dt_end' in i:
                text = f'{i["dt"]} - {i["dt_end"]}<br>{i["source"]}'
            else:
                text = f'{i["dt"]}<br>{i["source"]}'
            folium.CircleMarker(
                location=i['coordinates'],
                radius=8,
                popup=text,
                tooltip=text,
                fill_color='green',
                color='white',
                fill_opacity=0.8
            ).add_to(marker_clusters[i['source']])

            # folium.Marker(
            #     location=i['coordinates'],
            #     popup=i['dt'],
            #     icon=folium.Icon(color='green')
            # ).add_to(self.map)

        folium.LayerControl(collapsed=False).add_to(self.map)
        print(f'Created {len(self.data)} points')

    def open(self) -> None:
        # self.map.show_in_browser()
        self.map.save(self.path_to_save)
        os.system(f'start {self.path_to_save}')
