from core.mqtt import MQTTSubscribe
from core.woker_pool import MESSAGE_POOLS


def start():
    mqtt_subscribe = MQTTSubscribe()
    for project, message_pool in MESSAGE_POOLS.items():
        message_pool.start_task()
    mqtt_subscribe.server_connect()


if __name__ == '__main__':
    start()
