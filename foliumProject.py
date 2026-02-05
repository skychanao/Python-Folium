import folium
import requests


m = folium.Map(location=(48.1351, 11.5820),zoom_start = 10)

folium.Marker(
    location=[48.140316111464784, 11.559727592980297],
    tooltip = "Munich Hbf",
    popup = "Central Station of munich",
    icon=folium.Icon(icon="cloud")
).add_to(m)

geojson_data = requests.get(
    "https://github.com/isellsoap/deutschlandGeoJSON/blob/main/4_kreise/3_mittel.geo.json"
)

folium.GeoJson(geojson_data, name="hello world").add_to(m)

folium.LayerControl().add_to(m)

m.save('map.html')