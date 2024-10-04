import os
from flask import Flask, render_template, request
import folium

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def log():
    if request.method == 'POST':
        radio = request.form.get('Fix')
        if (radio == 'surface'):

        
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            y = float(request.form.get('y'))
    
            kappa = folium.Map(location=[latitude, longitude], zoom_start=13)   
            folium.Circle(
            location=[latitude, longitude],
            radius=120 * y ** (1/3),
            color='yellow',
            fill=True,
            ).add_to(kappa)

            folium.Circle(
            location=[latitude, longitude],
            radius=239*y**(0.427),
            color='green',
                fill=True,
            ).add_to(kappa)

            folium.Circle(
            location=[latitude, longitude],
            radius=218*y**0.334,
            color='red',
            fill=True,
            ).add_to(kappa)

            map_path = os.path.join(app.root_path, 'templates', 'map.html')
            kappa.save(map_path)

            return render_template('map.html')
        else :
            return "hello there"



if __name__ == '__main__':
    app.run(debug=True)
