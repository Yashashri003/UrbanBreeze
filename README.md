# 🌬️ UrbanBreeze

### Cooler & Smarter Climate-Aware Journeys

UrbanBreeze is a climate-aware route planning web application built with **Python and Streamlit**.

Instead of choosing a route based only on distance or travel time, UrbanBreeze considers **temperature, heat exposure, climate comfort, and travel preferences** to help users choose a more comfortable route.

---

## ✨ Features

- 🗺️ **Climate-Aware Route Planning**
  - Find routes between locations while considering environmental conditions.

- 🌡️ **Temperature Information**
  - View temperature conditions associated with routes.

- 🧊 **CoolScore**
  - Compare routes based on climate comfort.

- 🚀 **Fastest Route**
  - Provides the quickest available route.

- ❄️ **Coolest Route**
  - Helps users choose a route with lower heat exposure.

- 🤖 **AI Recommended Route**
  - Provides a recommended route based on multiple factors such as travel time and climate conditions.

- 🚶 **Multiple Travel Modes**
  - Pedestrian
  - Cyclist
  - EV

- 📍 **Saved Places**
  - Save frequently visited locations such as Home, College, Office, etc.

- 🕘 **Route History**
  - View previously planned routes and reuse them.

- 👤 **User Preferences**
  - Manage travel preferences used by the application.

- 🗺️ **Interactive Maps**
  - View selected locations and routes on an interactive map.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Folium**
- **Streamlit-Folium**
- **Requests**
- **OpenStreetMap / Nominatim**
- **Routing API**
- **FortyGuard API**

---

## 📁 Project Structure

```text
UrbanBreeze/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 0_Login.py
│   ├── 1_Plan_Route.py
│   ├── 2_Route_Results.py
│   ├── 3_Saved_Places.py
│   ├── 4_Route_History.py
│   └── 5_Profile.py
│
├── utils/
│   ├── __init__.py
│   ├── routing.py
│   ├── climate.py
│   ├── fortyguard.py
│   └── ui.py
│
├── data/
│   └── fortyguard_cache.json
│
└── .gitignore
