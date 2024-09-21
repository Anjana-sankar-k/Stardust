import ssl
import certifi
import ee

# Create an SSL context with the certifi certificate bundle

ssl._create_default_https_context = ssl._create_unverified_context

def authenticate_earth_engine():
    try:
        ee.Authenticate()  # Authenticate Earth Engine
        ee.Initialize(project="location-432112")    # Initialize the Earth Engine API
    except Exception as e:
        print(f"Authentication failed: {e}")
        exit()

# Call the authentication function
authenticate_earth_engine()

def get_light_pollution_data(lat, lng):
    bounds = ee.Geometry.Rectangle([
        lng - 0.05, lat - 0.05,  # southwest corner
        lng + 0.05, lat + 0.05   # northeast corner
    ])
    
    image = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG') \
        .filterBounds(bounds) \
        .mean()

    # Compute the mean light pollution value for the area
    light_pollution = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=bounds,
        scale=500
    ).get('avg_rad')  # Replace 'avg_rad' with the appropriate band name

    return {
        'light_pollution': light_pollution.getInfo()  # Convert to a Python value
    }
