from utils import credentials
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from kafka import KafkaProducer
import uuid
import json



DR = [-71.9451120673, 17.598564358, -68.3179432848, 19.8849105901]
-71.823120,17.499347,-68.219604,20.015243
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


class StdOutListener(StreamListener):
    global producer
    
    def on_connect(self):
        print("Conexion establecida....Iniciando transmision!")
    
    def on_data(self,data):
        data = json.loads(data)
        d = json.dumps(data).encode("utf-8")
        key = bytes(str(uuid.uuid1().int),"utf-8")
        
        try:
            producer.send("tweets", key=key, value=d)
            producer.flush()
            print(data.get('retweeted_status'))
            #print(f'Published: {[key for key in data.keys()]}')

        except Exception as ex:
            print(str(ex))
        
        return True

    def on_error(self,status):
        print(status)

if __name__ == '__main__':

    auth = OAuthHandler(credentials.CON_key, credentials.CON_secret)
    auth.set_access_token(credentials.ACC_TOKEN, credentials.ACC_SECRET)

    listener = StdOutListener()
    stream = Stream(auth, listener)

    stream.filter(locations=DR)