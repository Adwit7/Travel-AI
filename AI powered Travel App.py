# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 20:12:31 2025

@author: adwit
"""

import streamlit as st
import openai
import requests
import json

# Set up OpenAI API key
OPENAI_API_KEY = "your_openai_api_key_here"
GOOGLE_PLACES_API_KEY = "your_google_places_api_key_here"

# Function to get place details from Google Places API
def get_places(query, location, place_type):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": location,
        "radius": 5000,
        "type": place_type,
        "key": GOOGLE_PLACES_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Function to generate travel itinerary
def generate_itinerary(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI travel planner that provides personalized itineraries."},
            {"role": "user", "content": user_input}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI setup
st.title("AI-Powered Travel Planner")

destination = st.text_input("Enter your destination:")
budget = st.number_input("Enter your budget ($):", min_value=50, max_value=10000, step=50)
room_type = st.selectbox("Select room type:", ["En-suite", "Double", "Bathroom Attached"])
purpose = st.text_area("What kind of trip do you want? (Adventure, Relaxing, Cultural, etc.)")

discover = st.button("Find Hotels & Places")
if discover:
    if destination:
        # Fetch hotels
        hotels = get_places(f"hotels in {destination}", "", "lodging")
        hotel_info = [f"{h['name']} - {h.get('formatted_address', 'Address not available')}" for h in hotels[:5]]
        st.subheader("Top Hotels")
        st.write("\n".join(hotel_info) if hotel_info else "Hotel information not found.")
        
        # Fetch restaurants
        restaurants = get_places(f"restaurants in {destination}", "", "restaurant")
        restaurant_info = [f"{r['name']} - {r.get('formatted_address', 'Address not available')}" for r in restaurants[:5]]
        st.subheader("Top Restaurants")
        st.write("\n".join(restaurant_info) if restaurant_info else "Restaurant information not found.")
        
        # Fetch tourist spots
        attractions = get_places(f"tourist attractions in {destination}", "", "tourist_attraction")
        attraction_info = [f"{a['name']} - {a.get('formatted_address', 'Address not available')}" for a in attractions[:5]]
        st.subheader("Top Attractions")
        st.write("\n".join(attraction_info) if attraction_info else "Tourist attraction information not found.")

plan_trip = st.button("Generate Itinerary")
if plan_trip:
    user_prompt = f"Create a travel itinerary for {destination} within a budget of ${budget}. Include best hotels with {room_type} rooms, top attractions, and food recommendations. Purpose: {purpose}."
    itinerary = generate_itinerary(user_prompt)
    st.subheader("Your Travel Itinerary")
    st.write(itinerary)
