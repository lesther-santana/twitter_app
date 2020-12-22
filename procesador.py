from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import requests
import utils.parser as parser



def create_contex():
      sc = SparkContext("local","tweetspark")
      sc.setLogLevel("ERROR")
      ssc = StreamingContext(sc,60)


      server = 'http://localhost:5000/'
      tweets_endpoint = server + 'spark_data'
      top_users_endpoint = server + 'top_users'

      def send_tweets(Dstream,endpoint):

            def send_to_flask(time, rdd,):
                  if not rdd.isEmpty():
                        request_data = json.dumps({
                              'tweets':rdd.collect(),
                              'batch':str(time)
                              })
                        response = requests.post(endpoint, json=request_data)
            Dstream.foreachRDD(send_to_flask)

      def send_top_users(Dstream,endpoint):

            def send(time,rdd):
                  if not rdd.isEmpty():
                        top = rdd.take(10)
                        lista = []
                        for data in top:
                              lista.append(data)
                        request_data = json.dumps({'users':lista})
                        response = requests.post(endpoint, json=request_data)
            Dstream.foreachRDD(send)

      KafkaStream = KafkaUtils.createDirectStream(ssc, ["tweets"], {"bootstrap.servers": 'localhost:9092'})

      parsed = KafkaStream.map(lambda x: json.loads(x[1])).map(lambda x: parser.parse_json(x))
      batch_count = KafkaStream.count().map(lambda x: f'batch received size: {x}')
      parsed_count = parsed.count().map(lambda x: f'batch parsed count: {x}')

      count_windowed = KafkaStream.countByWindow(60*10,60).map(lambda x:('Tweets total (One minute rolling count): %s' % x))
      top_users = parsed.map(lambda x: x['user_screen_name'])\
            .countByValueAndWindow(60*10,60)\
                  .transform(lambda rdd:rdd.sortBy(lambda x:-x[1]))\
                              .map(lambda x: (x[0],x[1]))


      #parsed.foreachRDD(send_to_flask)

      send_tweets(parsed,tweets_endpoint)
      send_top_users(top_users, top_users_endpoint)

      batch_count.union(parsed_count).pprint()
      count_windowed.pprint()
      return ssc

ssc = StreamingContext.getOrCreate('tmp/checkpoint1', lambda: create_contex())

ssc.start()
ssc.awaitTermination()