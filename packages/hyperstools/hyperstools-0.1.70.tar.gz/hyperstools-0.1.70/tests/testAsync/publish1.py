from hyperstools.mq.lib import Queue
RABBITMQ = {
    "host": "10.123.99.99",
    "port": 5672,
    "vhost": "/test",
    "user": "admin",
    "password": "admin",
    "queue": "test1",
    "heart_beat": 100,
}

def main():
    Queue(RABBITMQ).publish({"msg": 1})    