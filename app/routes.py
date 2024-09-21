from flask import render_template, request, jsonify
from app import app
from app.earth_engine import get_light_pollution_data
from app.geocoding import geocode_address
from app.air_quality import get_air_quality
import ee

@app.route('/')
def index():
    return render_template('location.html')

@app.route('/find_stargazing_places', methods=['POST'])
def find_stargazing_places():
    user_location = request.json['location']
    lat, lng = user_location['lat'], user_location['lng']
    
    # Define the bounds around the user's location (e.g., 50 km radius)
    bounds = ee.Geometry.Point(lng, lat).buffer(50000)
    
    # Fetch light pollution data
    light_pollution_data = get_light_pollution_data(bounds)
    
    # Generate candidate locations in a grid pattern
    candidate_locations = []
    num_candidates = 5  # Number of candidates in each direction (+lat, -lat, +lng, -lng)
    step_size = 0.01  # Step size in degrees (approximately 1.11 km at the equator)
    
    for i in range(-num_candidates, num_candidates + 1):
        for j in range(-num_candidates, num_candidates + 1):
            candidate_lat = lat + i * step_size
            candidate_lng = lng + j * step_size
            candidate_locations.append({
                'name': f'Candidate {i},{j}',
                'lat': candidate_lat,
                'lng': candidate_lng
            })

    places = []
    
    # Evaluate each candidate location
    for candidate in candidate_locations:
        candidate_lat = candidate['lat']
        candidate_lng = candidate['lng']
        
        # Fetch air quality data for the candidate location
        air_quality_data = get_air_quality(candidate_lat, candidate_lng)
        
        # Get the corresponding light pollution data for this location
        candidate_light_pollution = light_pollution_data['light_pollution']  # Placeholder logic
        
        # Apply criteria: Low light pollution and high air quality
        if candidate_light_pollution < 0.3 and air_quality_data['data']['aqi'] < 50:  # Example thresholds
            places.append({
                'name': candidate['name'],
                'lat': candidate_lat,
                'lng': candidate_lng,
                'light_pollution': candidate_light_pollution,
                'air_quality': air_quality_data['data']['aqi']
            })
    
    # Sort places by light pollution and air quality (optional)
    places = sorted(places, key=lambda x: (x['light_pollution'], -x['air_quality']))

    print(places)
    
    return jsonify(places)

@app.route('/news_tips')
def news_tips():
    return render_template('news_tips.html')
