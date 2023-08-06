from datetime import datetime
from prueba import Queue
def callback_f(**kwargs):
    msg = kwargs['msg']
    print("mensaje: {}".format(msg))
    return True

t1 = datetime.now()
with Queue(
    bootstrap_servers='18.184.154.2:9092',
    group_id='grp5',
    redis_host='18.197.176.129',
    redis_port='5151',
    redis_password='3antsRedisWs785$*11',
    topic='test_001',
    redis_db=1) as q:
        ret = True
        for i in range(15):
            ret = q.consumer(callback=callback_f)
            if ret:
                print('total partition {}'.format(q.cons.total_partitions()))
                print('partition {}'.format(q.cons.partition()))
                print('time used: {}'.format(str((datetime.now() - t1).total_seconds())))
                t1 = datetime.now()




from datetime import datetime
from prueba import Queue
with Queue(
    bootstrap_servers='18.184.154.2:9092',
    group_id='grp5',
    redis_host='18.197.176.129',
    redis_port='5151',
    redis_password='3antsRedisWs785$*11',
    topic='test_001',
    redis_db=1) as q:
        q.expand_partitions(num_partitions=4)
        for i in range(500):
            t1 = datetime.now()
            q.producer(msg='mensaje {}'.format(str(i)))
            print('time used: {}'.format(str((datetime.now() - t1).total_seconds())))



from datetime import datetime
from prueba import Queue
for num in range(1,16):
    with Queue(
        bootstrap_servers='18.184.154.2:9092',
        group_id='grp5',
        redis_host='18.197.176.129',
        redis_port='5151',
        redis_password='3antsRedisWs785$*11',
        topic='test_001',
        redis_db=1) as q:
            q.expand_partitions(num_partitions=4)
            for i in range(500):
                t1 = datetime.now()
                q.producer(msg='mensaje {}'.format(str(i)))
                print('time used: {}'.format(str((datetime.now() - t1).total_seconds())))
    print('Vuelta numero {}'.format(num))
# source /home/usuario/workspace/virtualenv/kafka3.6/bin/activate && cd /home/usuario/workspace/kafka_client_syn/kafka_client


'''
topic_partition = TopicPartition(topic=list_topic[0], partition=msg.partition(), offset=msg.offset())
consumer.committed(partitions=[topic_partition2])

topic_partition2 = TopicPartition(topic=list_topic[0], partition=msg.partition())
consumer.commit(offsets=[topic_partition])
consumer.committed(partitions=[topic_partition2])

consumer.seek(partition=topic_partition)
consumer.committed() 



%load_ext autoreload                                           
%autoreload 2        
from kafka_client_3ants import KafkaConsumer
from kafka_client_3ants import Producer

cons = KafkaConsumer(bootstrap_servers='18.184.154.2:9092', group_id='ktc1')
cons.connect(topics=['tt7'])
cons.is_connected
cons.get_messages
cons.close()
cons.is_connected
prod = KafkaProducer(bootstrap_servers='18.184.154.2:9092')
prod.send_message(topic='tt7', msg='class3', partition=0) 
'''


import test_init 
k = test_init.SynKafka() 

ka = k.Admin(server='18.184.154.2:9092')
ka.create_topic(topic='len1', num_partitions=30, delete_retention_ms=1000, retention_ms=3000)

with k.Consumer(server='18.184.154.2:9092', group='ktc1') as kc: 
    kc.connect(topics=['len1']) 
    for _ in range(1, 100):  
        print(kc.get_message())

with k.Producer(server='18.184.154.2:9092') as kp: 
    kp.connect(topic='len1') 
    for _ in range(1, 300):
        kp.send_message(msg={'a': 1})

r = syn_client.SynRedis()


with r.Consumer(host='18.197.176.129', port='5151', password='3antsRedisWs785$*11', db=0) as rc:
    rc.connect(topic='len1')    
    for _ in range(1, 300):
        rc.get_message()

with r.Producer(host='18.197.176.129', port='5151', password='3antsRedisWs785$*11', db=0) as rp: 
    rp.connect(topic='len1') 
    for _ in range(0,100): 
        rp.send_message({"a":1}) 
