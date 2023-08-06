from hyperstools.mq.lib import eventLoop

RABBITMQ = {
    "host": "10.123.99.99",
    "port": 5672,
    "vhost": "/test",
    "user": "admin",
    "password": "admin",
    "queue": "test1",
    "heart_beat": 100,
}
RABBITMQ2 = {
    "host": "10.123.99.99",
    "port": 5672,
    "vhost": "/test",
    "user": "admin",
    "password": "admin",
    "queue": "test2",
    "heart_beat": 100,
}


@lib.Queue(RABBITMQ)
def listen(body):
    print(body)


@lib.Queue(RABBITMQ2)
def listen2(body):
    print(body)

def main():
    listen()
    listen2()
    eventLoop.run()
