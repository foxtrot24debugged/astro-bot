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
| API Provider | '_________' |
| API Base URL | `_______________________________` |
| Endpoint | `_______________________________` |
| Authentication method | `_______________________________` |
| Required query parameters | `_______________________________` |
| Sample JSON response (formatted example) |  
```

```
|

--- 

##  Evaluation – Web Architecture, MVC Design & Security 

In this section, evaluate how web technologies, architecture, and design patterns have been applied in your **AstroBot**. Your responses must relate directly to your implementation and include reflection on your design decisions.

---

###  Web Architecture – Client–Server Model (3 marks)

Explain how the client–server model applies to your AstroBot:

- Identify the **client** 
- Identify the **server(s)** 
- Describe how data flows between:
  - User, AstroBot and APIs

Include a **simple block diagram** to illustrate this interaction.

####  Security Considerations: (3 marks )
- Consider but not limiting to secure handling of API keys and tokens, API rate limiting, and Input validation (e.g., handling user commands safely), include examples from code where necessary to illustrate.

---

###  RESTful API Usage in Your Application (3 marks )

Explain how REST APIs are used in your AstroBot: 

- Describe how HTTP methods (GET, POST) are used  
- Explain how your bot interacts with APIs (Webex, Weather, ISS, Geocoding)  
- Describe how JSON responses are received and processed  

Note: Relate your explanation directly to your code for higher grade. 

#### Security Considerations: (2 marks)
- Check response status codes, Handling invalid or unexpected API responses, Avoiding excessive API calls

---

###  MVC Design Pattern in AstroBot (3 Marks)

Explain how the **Model–View–Controller (MVC)** pattern applies to your solution:
Provide a short example based on your implementation

| Component   | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model**  |  |
| **View**   |  |
| **Controller** |  |

---

### 📝 Reflection and Evaluation ( 8 marks )

Reflect on your AstroBot (400 words):

- How effective is your bot in meeting the Astronomy Club’s needs?  
- What design decisions worked well?  
- What challenges did you face when integrating APIs?  
- What security risks did you identify and how were they handled?  
- How could your solution be improved in the future?  

---

 **Tip:** Link your answers directly to your code and examples for higher marks.
### Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

###  Total: /40
