import json
import pandas as pd 
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from dateutil import tz


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.twitter'

db = SQLAlchemy(app)

count = 0
top = {'users':['']}

class Tweet(db.Model):
    created_at = db.Column(db.DateTime)
    tweet_ID = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    user_name = db.Column(db.String)
    user_screen_name = db.Column(db.String)
    text = db.Column(db.String)
    lang = db.Column(db.String)
    hashtags = db.Column(db.String)
    user_mentions = db.Column(db.String)
    source = db.Column(db.String)
    coords = db.Column(db.String)
    coords_type = db.Column(db.String)
    is_quote = db.Column(db.String)
    is_retweet = db.Column(db.String)
    is_reply = db.Column(db.String)
    batch = db.Column(db.DateTime)
    truncated = db.Column(db.String)

@app.route("/")
def index():

    return render_template('main.html')


@app.route("/spark_data", methods=['POST'])
def data():
    global count
    if not request.json:
        return "error: not json", 400

    data = json.loads(request.json)
    batch_time = datetime.strptime(data['batch'],'%Y-%m-%d %H:%M:%S')
    added = 0

    for tweet in data['tweets']:

        inbound_tweet = Tweet(
            created_at = datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y').\
                replace(tzinfo=tz.tzutc()).\
                    astimezone(tz.tzlocal()),
            tweet_ID = tweet["id"],
            user_id = tweet["user_id"],
            user_name = tweet["user_name"],
            user_screen_name = tweet["user_screen_name"],
            text = tweet["text"],
            lang = tweet["lang"],
            hashtags = ",".join([hashtag for hashtag in tweet["hashtags"]]) if tweet["hashtags"] else None,
            user_mentions = ",".join([mention for mention in tweet["user_mentions"]]) if tweet["user_mentions"] else None,
            source = tweet["source"],
            coords = ",".join([str(coord) for coord in tweet["coords"]]) if tweet["coords"] else None,
            coords_type = tweet["coords_type"],
            is_quote = tweet["is_quote"],
            is_retweet = tweet["is_retweet"],
            is_reply = tweet["is_reply"],
            truncated = tweet["truncated"],
            batch = batch_time
        )
        db.session.add(inbound_tweet)
        db.session.commit()
        added += 1
    count += added
    print(f'Successfully added {added} /n Added since start:{count}')
    
    return 'Success', 201

@app.route('/top_users', methods=['POST'])
def top_users():
    global top

    if not request.data:
        return "Error", 400
        
    data = json.loads(request.json)
    data['users'] = [(usuario[0].replace("\'",""),usuario[1]) for usuario in data['users']]
    top['users'] = data['users']
    print(top)
    return 'Success', 201


@app.route('/top_users', methods=['GET'])
def send_users():
    global top
    return jsonify(top)

@app.route('/counters', methods=['GET'])
def get_counters():

    result = db.session.query(Tweet.batch, func.count(Tweet.batch)).group_by(Tweet.batch).all()
    df = pd.DataFrame(result, columns=['batch','size'])
    return jsonify({'labels':df['batch'].apply(str).tolist(), 'count':df['size'].tolist()})


if __name__=="__main__" :

    app.run(host = 'localhost',debug=True,port="5000")

