import os
from flask import Flask, render_template, request
import folium
import math

app = Flask(__name__)

def get_population_density(latitude, longitude):
    return 1000

def estimate_casualties(yield_kt, population_density, radius):
    area = math.pi * (radius / 1000) ** 2
    people_in_area = area * population_density
    return people_in_area * 1.0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route('/detonate', methods=['POST', 'GET'])
def log():
    if request.method == 'POST':
        radio = request.form.get('Fix')
        if radio == 'surface':
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            y = float(request.form.get('y'))

            
            kappa = folium.Map(width=1200,height=1080,location=[latitude, longitude], zoom_start=6)
            carto_dark_matter = folium.TileLayer(
                tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                attr='CartoDB',
                name='CartoDB Dark Matter',
                overlay=False,
                control=True
            )
            carto_dark_matter.add_to(kappa)

            
            esri_satellite = folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Esri Satellite',
                overlay=False,
                control=True
            )
            esri_satellite.add_to(kappa)

            
           

           
            blast_radius = 0.09*y ** (0.4)
            heavyBlast = 0.18*y ** (0.4)
            moderateBlast = 0.1 * y **(0.4)*1000
            thermal_radius = 218 * y ** 0.334

            folium.Circle(location=[latitude, longitude],
                          radius=blast_radius*1000, 
                          color='yellow', 
                          fill=True
                        ).add_to(kappa)

            folium.Circle(location=[latitude, longitude], 
                          radius=heavyBlast*1000, 
                          color='red', 
                          fill=True
                          ).add_to(kappa)
            
            folium.Circle(location=[latitude, longitude], 
                          radius=moderateBlast, 
                          color='grey', 
                          fill=True
                          ).add_to(kappa)
            
            folium.Circle(location=[latitude, longitude], 
                          radius=thermal_radius, 
                          color='orange', 
                          fill=True
                          ).add_to(kappa)


          
           # population_density = get_population_density(latitude, longitude)

           # blast_casualties = estimate_casualties(y, population_density, blast_radius)
            #fallout_casualties = estimate_casualties(y, population_density, fallout_radius)
           # thermal_casualties = estimate_casualties(y, population_density, thermal_radius)

            #total_casualties = blast_casualties + fallout_casualties + thermal_casualties

           
            folium.LayerControl().add_to(kappa)

            
            map_path = os.path.join(app.root_path, 'templates', 'map.html')
            kappa.save(map_path)

            return render_template('map.html')
        # casualties=round(total_casualties)

        else:
            return "<h1>Under construction</h1>"


if __name__ == '__main__':
    app.run(debug=True)
