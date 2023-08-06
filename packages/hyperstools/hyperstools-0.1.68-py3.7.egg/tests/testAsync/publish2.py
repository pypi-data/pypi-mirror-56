from hyperstools.mq.lib import Queue
RABBITMQ2 = {
    "host": "10.123.99.99",
    "port": 5672,
    "vhost": "/test",
    "user": "admin",
    "password": "admin",
    "queue": "test2",
    "heart_beat": 100,
}
def main():
    Queue(RABBITMQ).publish({"msg": 2}) 