🚴‍♂️ Strava OAuth 2.0 Demo App
✅ Still in progress: Currently working with Strava to enable multi-athlete access — at the moment, only the developer (me) can authenticate and retrieve data due to Strava’s "Single Player Mode."

🌐 About the Project
This project demonstrates how to interact with APIs that use OAuth 2.0 authentication, specifically with the Strava API. It showcases a working web application built with Flask that authorizes a user, retrieves their athlete data, and displays it.

🧠 What I Learned
This project deepened my understanding of:

📡 Making HTTP Requests
Using the requests library to send data, set headers, and handle responses from web APIs.

🔐 Implementing OAuth 2.0 Authorization
Safely managing the flow of user authorization using access and refresh tokens.

🛠️ Error Handling with Try-Except Blocks
Gracefully catching exceptions like ConnectionError and HTTPError to improve user experience.

🔄 Managing API Tokens
Persisting and refreshing tokens to maintain authenticated sessions between user visits.

🌍 Building Flask Web Interfaces
Creating user-facing routes to connect, display, and handle interaction with the Strava API.

🖥️ Features
✅ User login with Strava (OAuth 2.0)

🔑 Token management (access + refresh)

📊 Fetch and display athlete stats from Strava

⚠️ Error handling with user-friendly messages

🧪 Local and deployed versions supported (e.g., Render)

🧪 Status
 OAuth flow implemented

 Token storage and management via Flask sessions

 Basic error handling

 Multi-user support pending Strava Developer Program approval