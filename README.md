# Real-Time Tweet Analysis App (not finished)

The goal of this project is to practice real-time data analysis using python.

Once completed this Web application is for real-time analysis of tweets made in the Dominican Republic. 
- The Tweepy library handles the connection to the Twitter API stream endpoint. 
-An Apache Kafka topic handles the JSON-encoded tweets . 
  -Spark Streaming job translates the tweets into English for sentiment analysis using TextBlob
  -Keywords extracted using YAKE!. 
  -Web-based dashboard to display results implemented using HTML, CSS and JavaScript through requests to a Flask backend.

