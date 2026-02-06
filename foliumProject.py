import folium
import requests

def main():
    m = folium.Map(location=(48.1351, 11.5820),zoom_start = 10,)


    munich_districts = requests.get(
        "https://gist.githubusercontent.com/freinold/26eba0e6038bc1cff80cf250bde402ab/raw/b2607a53629bdbd9b0625fa633e2b136eec0acaa/munichDistricts.geo.json"
    ).json()

    # add names and stuff
    folium.GeoJson(munich_districts, name="District Maps").add_to(m)

    trainsitLines(m)

    stations(m)


    folium.LayerControl().add_to(m)

    print("sucessfully generated map")
    m.save('map.html')


def trainsitLines(m):
    munich_SBahn = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_SBahn.geojson"
    ).json()

    folium.GeoJson(munich_SBahn,name="SBahn",color = "#0B520B").add_to(m)

    munich_UBahn = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_UBahn.geojson"
    ).json()

    folium.GeoJson(munich_UBahn,name="UBahn",color = "blue").add_to(m)


    munich_tram = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_Tram.geojson"
    ).json()

    folium.GeoJson(munich_tram,name="Trams",color = "red").add_to(m)

def stations(m):
    #get response from json file
    url = "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/station_data_list.json"
    response = requests.get(url)
    stations = response.json()

    #initialize feature groups
    station_train = folium.FeatureGroup(name="S-Bahn Stations")
    station_metro = folium.FeatureGroup(name="U-Bahn Stations")
    station_tram = folium.FeatureGroup(name="Tram Stations")
    station_hauptbahnhof = folium.FeatureGroup(name="München Hauptbahnhof")

    #iterate through all stations in the list
    for station in stations:

        # Extract variables from the feature group
        lat = station['latitude']
        lon = station['longitude']
        name = station['locationName']
        place = station['place']
        train = station['ubahn']
        metro = station['sbahn']
        tram = station['tram']
        notBus = train or metro or tram
        
        #select trams,metro,train stops
        if place == "München" and notBus:

            #Add München Hauptbahnhof as individual group
            if "Hauptbahnhof" in name:
                folium.Marker(
                location=[lat, lon],
                popup=name,
                tooltip=name,
                icon=folium.Icon(color='black', icon='train', prefix='fa')
                ).add_to(station_hauptbahnhof)

            #Add remaining stations as a group, depending on services
            else:

                #add trains stations
                if train:
                        folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color = "darkgreen", icon='train', prefix='fa')
                    ).add_to(station_train)
                        
                #add metro stations
                elif metro:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color='darkblue', icon='subway', prefix='fa')
                    ).add_to(station_metro)

                #add tram stations stations
                else:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color='red', icon='tram', prefix='fa')
                    ).add_to(station_tram)

        #hide stations on deafult
        station_tram.show=False
        station_metro.show=False
        station_train.show=False

        #add stations to the map
        station_tram.add_to(m)
        station_metro.add_to(m)
        station_train.add_to(m)
        station_hauptbahnhof.add_to(m)

