import streamlit as st
import folium
from streamlit_folium import folium_static
import googlemaps
from geopy.geocoders import Nominatim


def get_user_location():
    """Get user's location using IP geolocation"""
    try:
        import requests
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        return data['latitude'], data['longitude']
    except:
        # Fallback to a default location if geolocation fails
        return 37.3387, 121.8853  # San Jose City coordinates

def find_nearby_therapists(latitude, longitude, radius=5):
    """Find nearby therapists using Google Places API"""
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    
    # Search for therapists and counseling centers
    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=radius * 1609.34,  # Convert miles to meters
        type='health',
        keyword='therapist OR counseling OR mental health'
    )
    
    return places_result.get('results', [])

def create_map(latitude, longitude, therapists):
    """Create an interactive map with therapist locations"""
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add user's location marker
    folium.Marker(
        [latitude, longitude], 
        popup='Your Location', 
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(m)
    
    # Add therapist markers
    for therapist in therapists:
        therapist_lat = therapist['geometry']['location']['lat']
        therapist_lng = therapist['geometry']['location']['lng']
        
        folium.Marker(
            [therapist_lat, therapist_lng],
            popup=therapist['name'],
            icon=folium.Icon(color='green', icon='medical')
        ).add_to(m)
    
    return m

def therapy_finder_page():
    st.divider()
    st.markdown("""
    <p class="subtitle">Find supportive mental health professionals near you</p>
    """, unsafe_allow_html=True)
    
    # Radius selection
    radius = st.slider(
        "Search Radius (miles)",
        min_value=1,
        max_value=20,
        value=5
    )
    
    # Location input
    location_option = st.radio(
        "Location Selection", 
        ["Enter Address Manually", "Use My Current Location"]
    )
    
    latitude, longitude = None, None
    
    if location_option == "Use My Current Location":
        latitude, longitude = get_user_location()
    
    else:
        address = st.text_input("Enter your address")
        if address:
            geolocator = Nominatim(user_agent="therapy_finder")
            location = geolocator.geocode(address)
            if location:
                latitude, longitude = location.latitude, location.longitude
            else:
                st.error("Could not find coordinates for the given address")
    
    if latitude and longitude:
        with st.spinner('Finding nearby therapists...'):
            therapists = find_nearby_therapists(latitude, longitude, radius)
        
        if therapists:
            st.success(f"Found {len(therapists)} therapy locations within {radius} miles")
            
            # Display therapist details with enhanced formatting
            for therapist in therapists[:5]:  # Limit to first 5 results
                st.markdown(f"""
                ### {therapist.get('name', 'Unnamed Location')}
                
                - 📍 **Address:** {therapist.get('vicinity', 'Address not available')}
                - ⭐ **Rating:** {therapist.get('rating', 'Not rated')} / 5
                - 🏥 **Open Now:** {'Yes' if therapist.get('opening_hours', {}).get('open_now', False) else 'No'}
                
                ---
                """)
            # Create and display map
            map_obj = create_map(latitude, longitude, therapists)
            folium_static(map_obj)
        
        else:
            st.warning("No therapy locations found in the selected radius.")


therapy_finder_page()