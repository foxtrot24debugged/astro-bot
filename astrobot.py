# AstroBot - Web Technology Assignment 1
# Complete modular implementation

import requests
import json
import time
from datetime import datetime

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ").strip()
        return f"Bearer {token}"
    else:
        # Fallback placeholder token for testing
        return "Bearer YOUR_WEBEX_TOKEN"

def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use hard-coded {prompt}? (y/n): ").lower()
    if choice == "n":
        return input(f"Enter your {prompt}: ").strip()
    return hardcoded_key

# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching rooms:", response.status_code)
        return []

    return response.json().get("items", [])


def print_rooms(rooms):
    print("\n--- Available Webex Rooms ---")
    for room in rooms:
        print(f"Title: {room.get('title')} | ID: {room.get('id')}")


def select_room(rooms):
    while True:
        name = input("\nEnter the name of the room to monitor: ").strip()
        for room in rooms:
            if name.lower() in room.get("title", "").lower():
                print(f"Selected Room: {room.get('title')}")
                return room.get("id")
        print("Room not found. Please try again.")


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None, None

    data = response.json().get("items", [])

    if not data:
        return None, None

    latest = data[0]
    return latest.get("id"), latest.get("text", "")


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "text": message
    }
    requests.post(url, headers=headers, data=json.dumps(data))

# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_weather(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return f"Error: City '{city}' could not be found."

    lat = location["lat"]
    lon = location["lon"]
    country = location.get("country", "")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return "Error: Could not retrieve weather data at this time."

    weather = response.json()
    temp = weather["main"]["temp"]
    desc = weather["weather"][0]["description"].title()
    humidity = weather["main"]["humidity"]
    wind = weather["wind"]["speed"]

    # Simple stargazing evaluation based on sky description
    stargazing = "Good" if "clear" in desc.lower() else "Poor (Cloudy/Obscured)"

    return (
        f"📍 Weather for {location['name']}, {country}:\n"
        f"• Condition: {desc}\n"
        f"• Temperature: {temp}°C\n"
        f"• Humidity: {humidity}%\n"
        f"• Wind Speed: {wind} m/s\n"
        f"🌌 Stargazing Quality: {stargazing}"
    )

# =========================
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):
    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json"

    response = requests.get(url)

    if response.status_code != 200:
        return "Error: Could not retrieve ISS location from API."

    data = response.json()
    timestamp = data.get("timestamp")
    human_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    location = reverse_geocode(lat, lon, api_key)
    place = "Over Ocean / No Nearby City"

    if location:
        place = f"{location.get('name')}, {location.get('country')}"

    return (
        f"🛸 ISS Current Location:\n"
        f"• Latitude: {lat}\n"
        f"• Longitude: {lon}\n"
        f"• Nearest Location: {place}\n"
        f"• Time: {human_time}"
    )

# =========================
# EXTENDED FEATURE (ASTRONOMY SUN/MOON)
# =========================
def get_sun_times(city, api_key):
    location = get_city_coordinates(city, api_key)
    if not location:
        return f"Error: City '{city}' not found."

    lat, lon = location["lat"], location["lon"]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "sunrise,sunset",
        "timezone": "auto"
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return "Error: Stargazing solar times unavailable."

    data = res.json()
    sunrise = data["daily"]["sunrise"][0].split("T")[1]
    sunset = data["daily"]["sunset"][0].split("T")[1]

    return (
        f"☀️ Solar Schedule for {location['name']}:\n"
        f"• Sunrise: {sunrise}\n"
        f"• Sunset: {sunset}\n"
        f"🌌 Stargazing begins after sunset!"
    )

# =========================
# MAIN BOT LOGIC
# =========================
def main():
    token = get_webex_token()

    weather_key = get_api_key(
        "Weather API key",
        "YOUR_OPENWEATHER_API_KEY"
    )

    rooms = get_rooms(token)

    if not rooms:
        print("No Webex rooms found or invalid token provided.")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _ = get_latest_message(token, room_id)
    print("\n[AstroBot Active] Polling for Webex messages...")

    while True:
        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:
            last_message_id = message_id

            print(f"Received message: '{message_text}'")

            if not message_text.startswith("/"):
                continue

            cmd_lower = message_text.lower().strip()

            if cmd_lower == "/help":
                send_message(
                    token,
                    room_id,
                    "AstroBot Commands:\n/weather <city>\n/iss\n/sun <city>\n/help\n/quit"
                )

            elif cmd_lower.startswith("/weather"):
                parts = message_text.split(maxsplit=1)
                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /weather <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_weather(city, weather_key))

            elif cmd_lower.startswith("/sun"):
                parts = message_text.split(maxsplit=1)
                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /sun <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_sun_times(city, weather_key))

            elif cmd_lower == "/iss":
                send_message(token, room_id, get_iss_location(weather_key))

            elif cmd_lower == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                print("Bot shut down requested via command.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help for a list of available commands.")

        time.sleep(5)


if __name__ == '__main__':
    main()
