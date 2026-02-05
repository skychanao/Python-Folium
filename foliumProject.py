import folium
import requests


m = folium.Map(location=(48.1351, 11.5820),zoom_start = 10,)

folium.TileLayer(
    tiles='https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
    attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://www.OpenRailwayMap.org">OpenRailwayMap</a>',
    name='OpenRailwayMap',
    overlay=True, # Allows it to sit on top of the base map
    control=True, # Adds it to the toggle menu
).add_to(m)


folium.Marker(
    location=[48.140316111464784, 11.559727592980297],
    tooltip = "Munich Hbf",
    popup = "Central Station of munich",
    icon=folium.Icon(icon="cloud")
).add_to(m)

geojson_data = requests.get(
    "https://raw.githubusercontent.com/skychanao/Python-Folium/main/munich.json"
).json()

folium.GeoJson(geojson_data, name="hello world").add_to(m)

folium.LayerControl().add_to(m)

m.save('map.html')