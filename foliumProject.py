import folium
import requests


def main():
    m = folium.Map(location=(48.15266871079503, 11.547840081444003),
                   zoom_start = 11.5,
                   min_zoom=10.5,
                   control_scale = True,
                   tiles="cartodb positron")

    districts(m)

    trainsitLines(m)

    stations(m)

    

    #circle(m,10000,48.1351, 11.5820)

    folium.LayerControl().add_to(m)

    print("sucessfully generated map")

    file_name = 'E:\TUE\Projects\Python-Folium\map'
    m.save(file_name + '.html')

def districts(m):
    districts_data = requests.get(
        "https://gist.githubusercontent.com/freinold/26eba0e6038bc1cff80cf250bde402ab/raw/b2607a53629bdbd9b0625fa633e2b136eec0acaa/munichDistricts.geo.json"
    ).json()

    world_border = [[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]
    
    all_district_coords = []

    for feature in districts_data['features']:
        full_name = feature['properties']['name']
        feature['properties']['name'] = full_name[14:]
        
        #coordinates of districts
        all_district_coords.append(feature['geometry']['coordinates'][0])
    # 2. Create the Mask Feature
    mask_geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [world_border] + all_district_coords
        }
    }

    # 3. Add the Darkened Mask to the map
    folium.GeoJson(
        mask_geojson,
        name="Map Mask",
        style_function=lambda x: {
            'fillColor': 'dark_gray',
            'color': 'none',
            'fillOpacity': 0.5   
        },
        control=False
    ).add_to(m)
    
    folium.GeoJson(
        districts_data,
        name="Boroughs",
        fillColor="white",
        color="black",
        tooltip=folium.GeoJsonTooltip(
            fields=['name'],       # The key in the JSON properties
            aliases=['Borough:'], # The label shown before the name
            localize=True
        ),
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 1
        }
    ).add_to(m)    

def trainsitLines(m):
    munich_SBahn = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_SBahn.geojson"
    ).json()

    folium.GeoJson(munich_SBahn,name="SBahn",color ="green").add_to(m)

    munich_UBahn = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_UBahn.geojson"
    ).json()

    folium.GeoJson(munich_UBahn,name="UBahn",color = "blue").add_to(m)


    munich_tram = requests.get(
        "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/Lines_Tram.geojson"
    ).json()

    #folium.GeoJson(munich_tram,name="Trams",color = "red").add_to(m)

def stations(m):
    stationsC = 0
    #get response from json file
    url = "https://gist.githubusercontent.com/leftshift/c3d0bcf4ab848fa49ebd90cc85904ae6/raw/c2db558f00d3e75ea043396c80bf43bd5e15486f/station_data_list.json"
    response = requests.get(url)
    stations = response.json()

    #initialize feature groups
    station_train = folium.FeatureGroup(name="S-Bahn Stations")
    station_metro = folium.FeatureGroup(name="U-Bahn Stations")
    #station_tram = folium.FeatureGroup(name="Tram Stations")
    station_hauptbahnhof = folium.FeatureGroup(name="München Hauptbahnhof")
    hiding_zone = folium.FeatureGroup(name="Hiding Zone", show=False)

    #iterate through all stations in the list
    for station in stations:

        # Extract variables from the feature group
        lat = station['latitude']
        lon = station['longitude']
        name = station['locationName']
        place = station['place']
        train = station['sbahn']
        metro = station['ubahn']
        tram = station['tram']
        notBus = train or metro or tram
        
        #select trams,metro,train stops
        if place == "München" and notBus:
            stationsC += 1
            #Add München Hauptbahnhof as individual group
            if "Hauptbahnhof" in name:
                if name == "Hauptbahnhof":
                    folium.Marker(
                    location=[lat, lon],
                    popup=name,
                    tooltip=name,
                    icon=folium.Icon(color='black', icon='train', prefix='fa')
                    ).add_to(station_hauptbahnhof)
                circle(hiding_zone,500,lat,lon)

            #Add remaining stations as a group, depending on services
            else:
                #add trains stations
                if train:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color = 'green', icon='train', prefix='fa')
                    ).add_to(station_train)
                    circle(hiding_zone,500,lat,lon)
                #add metro stations
                elif metro:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color="darkblue", icon='subway', prefix='fa')
                    ).add_to(station_metro)   
                    circle(hiding_zone,500,lat,lon)
                #add tram stations stations
                '''else:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color='red', icon='tram', prefix='fa')
                    ).add_to(station_tram) '''
                    # show hiding zones  
        

    #hide stations on deafult
    #station_tram.show=False
    station_metro.show=False
    station_train.show=False

    #add stations to the map
    #station_tram.add_to(m)
    station_metro.add_to(m)
    station_train.add_to(m)
    station_hauptbahnhof.add_to(m)
    hiding_zone.add_to(m)

def circle(group,radius,lat,long):
    folium.Circle(
        location=[lat, long],
        radius=radius,
        weight=0,
        color = "none",
        fill_opacity=0.5,
        opacity=1,
        fill_color="red",
        show=False,
    ).add_to(group)

#def Zoos(m):
    

if __name__ == "__main__":
    main()