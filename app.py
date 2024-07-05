import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title('On se retrouve où ?')

# Initialize the session state if not already present
if 'entries' not in st.session_state:
    st.session_state.entries = []

# Function to add a new entry to the list
def add_entry(name, address):
    lat, lon = geocode_address(address)
    st.session_state.entries.append({'name': name, 'address': address, 'latitude': lat, 'longitude': lon})

# Function to geocode an address
def geocode_address(address):
    geolocator = Nominatim(user_agent="geopy_test/1.0")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Function to calculate the midpoint
def calculate_midpoint(entries):
    valid_entries = [entry for entry in entries if entry['latitude'] is not None and entry['longitude'] is not None]
    if not valid_entries:
        return None, None
    avg_latitude = sum(entry['latitude'] for entry in valid_entries) / len(valid_entries)
    avg_longitude = sum(entry['longitude'] for entry in valid_entries) / len(valid_entries)
    return avg_latitude, avg_longitude

# Section to add a new entry
st.header('Add a New Entry')
with st.form(key='add_entry_form'):
    name = st.text_input('Name')
    address = st.text_input('Address')
    submit_button = st.form_submit_button(label='Add Entry')
    if submit_button:
        if name and address:
            add_entry(name, address)
            st.success(f'Added {name} at {address}')
        else:
            st.error('Please enter both name and address')

# Display the input fields for each entry
st.header('Entries')
if st.session_state.entries:
    for i, entry in enumerate(st.session_state.entries):
        st.write(f"{i+1}. **{entry['name']}**: {entry['address']}")
else:
    st.info('No entries yet. Add some above!')

# Add a button to calculate the midpoint
st.header('Midpoint Calculation')
if st.button('Calculate Midpoint'):
    midpoint_lat, midpoint_lon = calculate_midpoint(st.session_state.entries)
    if midpoint_lat is not None and midpoint_lon is not None:
        st.success(f'The midpoint is located at latitude: {midpoint_lat}, longitude: {midpoint_lon}')
        
        # Create a folium map centered at the midpoint
        m = folium.Map(location=[midpoint_lat, midpoint_lon], zoom_start=12)
        
        # Add the midpoint marker
        folium.Marker(
            location=[midpoint_lat, midpoint_lon],
            popup='Midpoint',
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        # Add markers for all valid entries
        for entry in st.session_state.entries:
            if entry['latitude'] is not None and entry['longitude'] is not None:
                folium.Marker(
                    location=[entry['latitude'], entry['longitude']],
                    popup=f"{entry['name']}: {entry['address']}",
                    icon=folium.Icon(color='blue')
                ).add_to(m)
        
        # Store the map in session state
        st.session_state['map'] = m
    else:
        st.error('Unable to calculate midpoint. Please check the addresses.')

# Display the map if it exists in the session state
if 'map' in st.session_state:
    st.header('Map')
    st_folium(st.session_state['map'], width=700, height=500)

# Optionally, display the entries with their coordinates
if st.checkbox('Show entries with coordinates'):
    st.write(pd.DataFrame(st.session_state.entries))