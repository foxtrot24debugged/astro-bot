import requests
import json
import time
from datetime import datetime

def prompt_for_webex_token():
    use_preset = input("Use default Webex token? (y/n): ").strip().lower()
    if use_preset == 'n':
        custom_token = input("Input your Webex token: ").strip()
        return f"Bearer {custom_token}"
    return "Bearer YOUR_WEBEX_TOKEN"

def prompt_for_key(service_name, default_key):
    choice = input(f"Use hardcoded {service_name} key? (y/n): ").strip().lower()
    if choice == 'n':
        return input(f"Enter {service_name} key: ").strip()
    return default_key

def fetch_webex_rooms(auth_token):
    endpoint = "https://webexapis.com/v1/rooms"
    req_headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    res = requests.get(endpoint, headers=req_headers)
    
    if res.status_code != 200:
        print(f"Failed to retrieve rooms. Status: {res.status_code}")
        return []
    return res.json().get("items", [])

def display_rooms_menu(room_list):
    print("\n=== Active Webex Rooms ===")
    for item in room_list:
        print(f"Name: {item.get('title')} [ID: {item.get('id')}]")

def choose_room(room_list):
    while True:
        target_name = input("\nType part of the room name to monitor: ").strip().lower()
        for item in room_list:
            if target_name in item.get("title", "").lower():
                print(f"Connected to: {item.get('title')}")
                return item.get("id")
        print("No matching room found. Try again.")

def get_latest_msg(auth_token, chat_room_id):
    endpoint = "https://webexapis.com/v1/messages"
    req_params = {"roomId": chat_room_id, "max": 1}
    req_headers = {"Authorization": auth_token}
    
    res = requests.get(endpoint, headers=req_headers, params=req_params)
    if res.status_code != 200:
        return None, None
        
    items = res.json().get("items", [])
    if not items:
        return None, None
        
    latest_msg = items[0]
    return latest_msg.get("id"), latest_msg.get("text", "")

def post_message(auth_token, chat_room_id, text_content):
    endpoint = "https://webexapis.com/v1/messages"
    req_headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    payload = {"roomId": chat_room_id, "text": text_content}
    requests.post(endpoint, headers=req_headers, data=json.dumps(payload))

def lookup_city_coords(city_name, api_key):
    endpoint = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city_name, "limit": 1, "appid": api_key}
    res = requests.get(endpoint, params=params)
    
    if res.status_code != 200:
        return None
    data = res.json()
    return data[0] if data else None

def get_weather_forecast(city_name, api_key):
    geo_data = lookup_city_coords(city_name, api_key)
    if not geo_data:
        return f"Error: Could not locate city '{city_name}'."
        
    lat, lon = geo_data["lat"], geo_data["lon"]
    country_code = geo_data.get("country", "")
    
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}
    res = requests.get(endpoint, params=params)
    
    if res.status_code != 200:
        return "Error: Weather service unavailable."
        
    payload = res.json()
    temperature = payload["main"]["temp"]
    condition = payload["weather"][0]["description"].title()
    hum = payload["main"]["humidity"]
    wind_spd = payload["wind"]["speed"]
    
    stargazing_status = "Good" if "clear" in condition.lower() else "Poor (Cloudy/Obscured)"
    
    return (
        f"📍 Weather for {geo_data['name']}, {country_code}:\n"
        f"• Condition: {condition}\n"
        f"• Temperature: {temperature}°C\n"
        f"• Humidity: {hum}%\n"
        f"• Wind Speed: {wind_spd} m/s\n"
        f"🌌 Stargazing Quality: {stargazing_status}"
    )

def reverse_lookup_coords(lat, lon, api_key):
    endpoint = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}
    res = requests.get(endpoint, params=params)
    if res.status_code != 200:
        return None
    data = res.json()
    return data[0] if data else None

def fetch_iss_telemetry(api_key):
    endpoint = "http://api.open-notify.org/iss-now.json"
    res = requests.get(endpoint)
    if res.status_code != 200:
        return "Error: Unable to fetch ISS telemetry."
        
    data = res.json()
    ts = data.get("timestamp")
    formatted_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]
    
    place_info = reverse_lookup_coords(lat, lon, api_key)
    location_desc = "Over Ocean / No Nearby City"
    if place_info:
        location_desc = f"{place_info.get('name')}, {place_info.get('country')}"
        
    return (
        f"🛸 ISS Current Location:\n"
        f"• Latitude: {lat}\n"
        f"• Longitude: {lon}\n"
        f"• Nearest Location: {location_desc}\n"
        f"• Time: {formatted_time}"
    )

def fetch_sun_schedule(city_name, api_key):
    geo_data = lookup_city_coords(city_name, api_key)
    if not geo_data:
        return f"Error: City '{city_name}' not found."
        
    lat, lon = geo_data["lat"], geo_data["lon"]
    endpoint = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "daily": "sunrise,sunset", "timezone": "auto"}
    res = requests.get(endpoint, params=params)
    if res.status_code != 200:
        return "Error: Solar schedule unavailable."
        
    data = res.json()
    sunrise_time = data["daily"]["sunrise"][0].split("T")[1]
    sunset_time = data["daily"]["sunset"][0].split("T")[1]
    
    return (
        f"☀️ Solar Schedule for {geo_data['name']}:\n"
        f"• Sunrise: {sunrise_time}\n"
        f"• Sunset: {sunset_time}\n"
        f"• Stargazing begins after sunset!"
    )

def main():
    token = prompt_for_webex_token()
    weather_key = prompt_for_key("Weather API key", "YOUR_OPENWEATHER_API_KEY")
    
    rooms = fetch_webex_rooms(token)
    if not rooms:
        print("Initialization failed: No rooms available.")
        return
        
    display_rooms_menu(rooms)
    room_id = choose_room(rooms)
    
    last_msg_id, _ = get_latest_msg(token, room_id)
    print("\n--- Bot Running & Polling ---")
    
    while True:
        msg_id, msg_text = get_latest_msg(token, room_id)
        
        if msg_id and msg_id != last_msg_id:
            last_msg_id = msg_id
            print(f"New message caught: '{msg_text}'")
            
            if msg_text.startswith("/"):
                command_lower = msg_text.lower().strip()
                
                if command_lower == "/help":
                    post_message(token, room_id, "AstroBot Commands:\n/weather <city>\n/iss\n/sun <city>\n/help\n/quit")
                elif command_lower.startswith("/weather"):
                    chunks = msg_text.split(maxsplit=1)
                    if len(chunks) < 2:
                        post_message(token, room_id, "Usage: /weather <city>")
                    else:
                        post_message(token, room_id, get_weather_forecast(chunks[1], weather_key))
                elif command_lower.startswith("/sun"):
                    chunks = msg_text.split(maxsplit=1)
                    if len(chunks) < 2:
                        post_message(token, room_id, "Usage: /sun <city>")
                    else:
                        post_message(token, room_id, fetch_sun_schedule(chunks[1], weather_key))
                elif command_lower == "/iss":
                    post_message(token, room_id, fetch_iss_telemetry(weather_key))
                elif command_lower == "/quit":
                    post_message(token, room_id, "AstroBot shutting down.")
                    print("Shutdown command received.")
                    break
                else:
                    post_message(token, room_id, "Unknown command. Type /help for assistance.")
                    
        time.sleep(5)

if __name__ == '__main__':
    main()
