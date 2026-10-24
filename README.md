[README_template_v1.md](https://github.com/user-attachments/files/33814151/README_template_v1.md)
# 🚀 Space Bot API Investigation Sheet

**Total Marks: 40**  
**TASK 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, **Weather API** and a **Geocoding API** , plus the Python time module. Also furhter investigate the application of Web Architecture and MVC design pattern in development of the Bot

---

##  Webex Messaging API (4 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `Authorization: Bearer <TOKEN>` |
| Endpoint to list rooms | `https://webexapis.com/v1/rooms` |
| Endpoint to get messages | `https://webexapis.com/v1/messages` |
| Endpoint to send message | `https://webexapis.com/v1/messages` |
| Required headers | `Authorization: Bearer <TOKEN>`, `Content-Type: application/json` |
| Sample full GET or POST request | `POST https://webexapis.com/v1/messages` <br> Header: `Authorization: Bearer YOUR_TOKEN` <br> Body: `{"roomId": "ROOM_ID", "text": "Hello Space Bot"}` |

---

##  ISS Current Location API (2 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `http://api.open-notify.org/iss-now.json` |
| Sample response format (example JSON) |  
```json
{
  "message": "success",
  "timestamp": 1713200000,
  "iss_position": {
    "latitude": "-24.1234",
    "longitude": "135.5678"
  }
}

```
|

---

##  Geocoding API (4 marks)

| Criteria | Details |
|---------|---------|
| Provider used (Choose one) | **LocationIQ / Mapbox/ OpenWeatherMap other -provide detail** |
| API Base URL | `http://api.openweathermap.org/geo/1.0` |
| Endpoint for geocoding | `http://api.openweathermap.org/geo/1.0/direct` |
| Endpoint for reverse geocoding | `http://api.openweathermap.org/geo/1.0/reverse` |
| Authentication method | `API Key (appid query parameter)` |
| Required query parameters | `lat, lon, limit, appid` |
| Sample request with latitude/longitude | `http://api.openweathermap.org/geo/1.0/reverse?lat=51.5074&lon=-0.1278&limit=1&appid=YOUR_API_KEY` |
| Sample JSON response (formatted example) |  
```[
  {
    "name": "London",
    "lat": 51.5074,
    "lon": -0.1278,
    "country": "GB",
    "state": "England"
  }
]

```
|

---


##  Weather API (3 marks)

| Criteria | Details |
|---------|---------|
| API Provider (Choose one) | **OpenWeather, OpenWeatherMap (or other – provide details)** |
| API Base URL | `https://api.openweathermap.org/data/2.5` |
| Endpoint for current weather | `https://api.openweathermap.org/data/2.5/weather` |
| Authentication method | `API Key (appid query parameter)` |
| Required query parameters | `lat, lon, units=metric, appid` |
| Sample JSON response (formatted example) |  
```{
  "weather": [{"main": "Clear", "description": "clear sky"}],
  "main": {"temp": 15.5, "humidity": 68},
  "wind": {"speed": 3.6},
  "name": "London",
  "sys": {"country": "GB"}
}

```
|

---

##  Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `datetime / time` |
| Function used to convert epoch | `datetime.fromtimestamp() or time.strftime()` |
| Sample code to convert timestamp |  
```import datetime
epoch_time = 1713200000
human_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S UTC')
print(human_time)
```
|
| Output (human-readable time) | `2024-04-15 17:20:00 UTC` |

---

##  Extended Feature API ( 3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | 'Open-Meteo Astronomy API' |
| API Base URL | `https://api.open-meteo.com/v1` |
| Endpoint | `https://api.open-meteo.com/v1/forecast` |
| Authentication method | `None (Free open API)` |
| Required query parameters | `latitude, longitude, daily=sunrise,sunset, timezone=auto` |
| Sample JSON response (formatted example) |  
```{
  "daily": {
    "time": ["2026-04-05"],
    "sunrise": ["2026-04-05T06:25"],
    "sunset": ["2026-04-05T19:40"]
  }
}

```
|

--- 

##  Evaluation – Web Architecture, MVC Design & Security 

In this section, evaluate how web technologies, architecture, and design patterns have been applied in your **AstroBot**. Your responses must relate directly to your implementation and include reflection on your design decisions.

---

###  Web Architecture – Client–Server Model (3 marks)

Explain how the client–server model applies to your AstroBot:

The AstroBot operates within a multi-tiered client-server architecture:

    Client: The Cisco Webex desktop or mobile application used by Astronomy Club members to submit user input commands (/weather, /iss, /sun).

    Server:

        The AstroBot Python Script (Middle-tier application server) which polls Webex, parses commands, executes logic, and handles responses.

        The External Web Services (APIs): Webex API, OpenWeather API, Open-Notify ISS API, and Open-Meteo API.

+------------------+         HTTP POST         +--------------------+
|  Webex Client    |  ---------------------->  |  AstroBot Python   |
| (Astronomy Club) |  <----------------------  | Application Server |
+------------------+         HTTP GET          +--------------------+
                                                         |
                                            HTTP GET     |  JSON Data
                                            Requests     v  Responses
                                              +---------------------+
                                              | External APIs       |
                                              | (OpenWeather, ISS,  |
                                              |  Open-Meteo)        |
                                              +---------------------+

####  Security Considerations: (3 marks )
1. API Key Protection: API keys and Webex Bearer tokens are dynamically requested or read from secure environment variables (.env) rather than being hardcoded into public repositories. .gitignore prevents secret leaks.

2. Input Validation: User text is validated (.startswith('/'), .split()) before making request calls to prevent path injection or unexpected API errors.

3. Rate Limiting: A time.sleep(5) delay is implemented inside the main execution loop to prevent excessive polling that could trigger HTTP 429 (Too Many Requests) rate limits from Webex endpoints.

---

###  RESTful API Usage in Your Application (3 marks )

AstroBot uses standard HTTP methods:

    GET Method: Used to pull data from OpenWeather, Open-Notify, Open-Meteo, and retrieve rooms/messages from Webex (requests.get()).

    POST Method: Used to submit new chat messages to Webex channels via requests.post() with a JSON payload containing roomId and text.

    JSON Processing: Responses are parsed into Python dictionary structures using .json(), extracting specific keys safely via .get() to avoid runtime key errors.

Security Considerations: (2 marks)

    HTTP Status Code Verification: Checks response.status_code == 200 before parsing responses to prevent crashes on server errors (500) or missing resources (404).

    Error Handling: Graceful fallback strings are returned to the chat if external services fail or return invalid data.
---

###  MVC Design Pattern in AstroBot (3 Marks)

Explain how the **Model–View–Controller (MVC)** pattern applies to your solution:
Provide a short example based on your implementation

| Component   | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model**  | Functions handling external API data processing (get_weather(), get_iss_location(), get_sun_times()). They fetch, parse JSON, and return raw structured data. |
| **View**   | The Webex Chat Interface and message formatting logic that presents human-readable formatted text outputs back to club members. |
| **Controller** | The main() event loop that monitors new incoming messages, validates command prefixes, and delegates tasks to the appropriate Model function. |

---

### 📝 Reflection and Evaluation ( 8 marks )

Reflect on your AstroBot (400 words):

The AstroBot successfully automates critical information gathering for the Astronomy Club by bridging real-time observation data straight into their Webex communication workspace. Integrating the /weather, /iss, and /sun features directly assists event organizers in deciding whether stargazing sessions can proceed based on real-time weather and cloud visibility.

A key design decision that worked effectively was modularizing each API integration into independent helper functions (get_weather, get_iss_location). This maintainable structure enabled rapid feature extension (adding the Open-Meteo solar API) without disrupting core bot execution. Furthermore, incorporating tracking for the last processed message ID prevented infinite messaging feedback loops.

The main technical challenge faced during development was reverse geocoding the coordinates returned by the ISS API. Because the International Space Station spends the majority of its orbit over open water, reverse geocoding API queries frequently returned empty lists. This was gracefully solved by catching empty responses and displaying "Over Ocean / No Nearby City" to maintain user context. Security was ensured by omitting tokens from version control and using .gitignore. In future iterations, implementing Webhooks instead of constant polling would improve performance and network efficiency.
---

###  Total: /40
