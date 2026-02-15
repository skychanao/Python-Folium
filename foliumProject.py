import folium
import requests
import json
def main():
    '''m = folium.Map(location=(48.15266871079503, 11.547840081444003),
                   zoom_start = 11.5,
                   min_zoom=10.5,
                   control_scale = True,
                   #tiles="cartodb positron"
                   )'''
    
    cartonDB = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'

    m = folium.Map(location=(48.15266871079503, 11.547840081444003),
	    maxZoom= 20,
        zoom_start = 11.5,
        min_zoom=10.5,
        control_scale=True
    )

    folium.TileLayer(
    tiles= cartonDB,
	    attr= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	    name = 'cartonDB',
        subdomains= 'abcd',
	    maxZoom= 20,
        min_zoom=10.5,
    ).add_to(m)

    folium.TileLayer(
        tiles= 'cartodb positron'
    ).add_to(m)

    addDraw(m)
    districts(m)
    trainsitLines(m)
    stations(m)  
    zoos(m)
    parks(m)
    golfCourse(m)
    museum(m)
    cinemas(m)
    hospitals(m)
    see(m)
    library(m)
    consulates(m)

    folium.LayerControl().add_to(m)

    print("sucessfully generated map")

    file_name = 'E:\TUE\Projects\Python-Folium\map'
    m.save(file_name + '.html')

def addDraw(m):

    from folium.plugins import Draw

    draw = Draw(position='bottomright',
        draw_options={
            'poliyline': {
                'shapeOption' : {
                    'fillcolor': '#434343',
                    'color': '#434343',
                }
            },
            'polygon': {
                'shapeOptions': {
                    'color': "#000000", 
                    'weight': 0,
                }
            },
            'circle': {
                'shapeOptions': {
                    'fillColor': "#000000",
                    'weight': 0,
                }
            },
            'rectangle': {
                'shapeOptions': {
                    'fillColor': "#000000",
                    'weight': 0,
                    }
            },
            'circlemarker': False
            }
    )

    draw.add_to(m)

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

    folium.GeoJson(munich_SBahn,name="SBahn",color ="red").add_to(m)

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
                    icon=folium.Icon(color='black', icon='flag-checkered', prefix='fa')
                    ).add_to(station_hauptbahnhof)
                
                #add hiding zones
                circle(hiding_zone,500,lat,lon)

            #Add remaining stations as a group, depending on services
            else:
                #add trains stations
                if train:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        icon=folium.Icon(color = 'red', icon='train', prefix='fa')
                    ).add_to(station_train)

                    #add hiding zones
                    circle(hiding_zone,500,lat,lon)
                
                #add metro stations
                elif metro:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
                        icon=folium.Icon(color="darkblue", icon='subway', prefix='fa')
                    ).add_to(station_metro)   

                    #add hiding zones
                    circle(hiding_zone,500,lat,lon)
                
                #add tram stations stations
                '''else:
                    folium.Marker(
                        location=[lat, lon],
                        popup=name,
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

def circle(group,radius,lat,long,fillcolor="lightblue",border=1):
    folium.Circle(
        location=[lat, long],
        radius=radius,
        weight=border,
        color = "black",
        fill_opacity=0.5,
        opacity=1,
        fill_color = fillcolor,
        show=False,
    ).add_to(group)

def zoos(m):

    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichZoo.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_Zoos = json.load(f)

    zoo_group = folium.FeatureGroup(name="Zoos")

    # 2. Loop through the features list
    for feature in munich_Zoos['features']:

        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='darkred', icon='paw', prefix='fa') #can use beautify plugin to get hex colors
        ).add_to(zoo_group)

    zoo_group.show=False
    zoo_group.add_to(m)

def parks(m):

    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichParks.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_parks = json.load(f)

    park_group = folium.FeatureGroup(name="Parks")

    for feature in munich_parks['features']:

        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='green', icon='tree', prefix='fa')
        ).add_to(park_group)

    park_group.show=False
    park_group.add_to(m)

def golfCourse(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichGolfCouse.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_golf = json.load(f)
    
    golf_group = folium.FeatureGroup(name="Golf Course")

    for feature in munich_golf['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='darkgreen', icon='golf-ball', prefix='fa')
        ).add_to(golf_group)

    golf_group.show=False
    golf_group.add_to(m)

def museum(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichMuseum.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_museum = json.load(f)
    
    museum_group = folium.FeatureGroup(name="Museums")

    for feature in munich_museum['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='cadetblue', icon='university', prefix='fa')
        ).add_to(museum_group)

    museum_group.show=False
    museum_group.add_to(m)

def cinemas(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichCinemas.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_cinemas = json.load(f)
    
    cinema_group = folium.FeatureGroup(name="Movie Theaters")

    for feature in munich_cinemas['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='orange', icon='film', prefix='fa')
        ).add_to(cinema_group)

    cinema_group.show=False
    cinema_group.add_to(m)

def hospitals(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichHospital.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_hospitals = json.load(f)
    
    hospital_group = folium.FeatureGroup(name="Hospitals")

    for feature in munich_hospitals['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='red', icon='ambulance', prefix='fa')
        ).add_to(hospital_group)

    hospital_group.show=False
    hospital_group.add_to(m)

def see(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichSee.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_see = json.load(f)
    
    see_group = folium.FeatureGroup(name="See (Lake)")

    for feature in munich_see['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='blue', icon='tint', prefix='fa')
        ).add_to(see_group)

    see_group.show=False
    see_group.add_to(m)

def library(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichLibrary.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_library = json.load(f)
    
    library_group = folium.FeatureGroup(name="Library")

    for feature in munich_library['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='lightred', icon='book', prefix='fa')
        ).add_to(library_group)

    library_group.show=False
    library_group.add_to(m)

def consulates(m):
    url = 'https://httpbin.org/post'
    file_path = r"E:\TUE\Projects\Python-Folium\munichConsulate.geojson"
    with open(file_path, 'r', encoding='utf-8') as f:
        munich_consulates = json.load(f)
    
    consulate_group = folium.FeatureGroup(name="Consulate")

    for feature in munich_consulates['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties']['name']

        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='gray', icon='globe', prefix='fa')
        ).add_to(consulate_group)

    consulate_group.show=False
    consulate_group.add_to(m)

if __name__ == "__main__":
    main()