from datetime import datetime as dt, timezone
import json
import os

import folium
from folium.plugins import MarkerCluster


class Map:
    def __init__(self, path_to_save: str = './map.html', path_to_data: str = 'Records.json'):
        if not path_to_save.endswith('.html'):
            self.path_to_save = './map.html'
        else:
            self.path_to_save = path_to_save
        self.path_to_data = path_to_data
        self.map = None
        self.data = []
        # self.tz = dt.now(timezone.utc).astimezone().tzinfo

    @property
    def _load_data(self) -> list:
        with open(self.path_to_data, 'r', encoding='utf8') as f:
            data = json.load(f)['locations']

        return data

    def analysis(self):
        self.data = []
        data = self._load_data

        for d in data:
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

            self.data.append({
                'coordinates': (latitudeE7, longitudeE7),
                'dt': date
            })

    def create_map(self):
        coordinates_of_center = self.data[0]['coordinates']
        self.map = folium.Map(location=coordinates_of_center, tiles=None, min_zoom=2, max_zoom=22, zoom_start=2, )

        tiles = (
            'OpenStreetMap',
            'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor',
            'CartoDB positron', 'CartoDB dark_matter',
        )
        for i in tiles:
            folium.TileLayer(i, min_zoom=2, max_zoom=22, zoom_start=2, name=i).add_to(self.map)

        marker_cluster = MarkerCluster(name='Location points', ).add_to(self.map)
        # folium.Marker(location=coordinates_of_center, popup='Center', icon=folium.Icon(color='red')).add_to(self.map)
        for i in self.data:
            folium.CircleMarker(
                location=i['coordinates'],
                radius=8,
                popup=i['dt'],
                tooltip=i['dt'],
                fill_color='green',
                color='white',
                fill_opacity=0.8
            ).add_to(marker_cluster)

            # folium.Marker(
            #     location=i['coordinates'],
            #     popup=i['dt'],
            #     icon=folium.Icon(color='green')
            # ).add_to(self.map)

        folium.LayerControl(collapsed=False).add_to(self.map)

    def open(self):
        print(f'Created {len(self.data)} points')
        # self.map.show_in_browser()
        self.map.save(self.path_to_save)
        os.system(f'start {self.path_to_save}')
