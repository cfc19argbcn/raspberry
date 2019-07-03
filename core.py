from libs.utils import *
from libs.pickle import *
from libs.mqtt import MQTTClient, on_message

import threading, time
import asyncio

cfg = instance_config('./config.ini')

WAIT_TIME_SECONDS = int(cfg.CORE.wait_time_seconds)
QSIZE = int(cfg.QUEUE.queue_maxsize)
TIME_CONNECTION = int(cfg.CORE.time_connection)

MQTT_BROKER = cfg.MQTT.mqtt_broker
MQTT_PORT = int(cfg.MQTT.mqtt_port)
MQTT_QOS = int(cfg.MQTT.mqtt_qos)
MQTT_TOPIC = cfg.MQTT.mqtt_topic


async def main():
    # Create two queue
    # 1. the first one stores mock data
    queue = asyncio.Queue()
    # the second file location where the previous queue is saved when there is no connection
    persistence = asyncio.Queue()
    # Create MQTT client and assign callback on response
    client = MQTTClient('CorePublish')
    client.assign_callback(on_message, type='message')
    # create threading
    ticker = threading.Event()
    # set default value for connection and retry
    connection = False
    retry = 0
    # Assign interval to while loop
    while not ticker.wait(WAIT_TIME_SECONDS):
        # Retry time, to re-check connection after 10 segundos
        retry += 1
        if retry == TIME_CONNECTION:
            connection = False
            retry = 0
        # Generate data mock
        data = emit_data_mock()
        # Print on screen Data
        print(time.ctime(), data)
        # Checking connection to internet and mqtt server
        # print("before connection %s" % connection)
        connection = checking_connection(connection)
        # print("connection %s" % connection)
        # if there are connection
        if connection:
            # if previously the connection was failed - reconnection
            if not client.connect_flag:
                # Connecting to client MQTT
                client.connect(MQTT_BROKER, MQTT_PORT)
                client.connect_flag = True
            # It will publish to topic the data
            client.publish(MQTT_TOPIC, str(data), qos=MQTT_QOS)
            # If persistence has store file
            while persistence.qsize() >= 1:
                # Get file path from the queue
                filename = persistence.get_nowait()
                # Extract the data
                response = serialization_load_obj(filename)
                # Put all elements in the queue
                for data in response:
                    queue.put_nowait(data)
                # The loop it will stop when the queue is empty
                if persistence.empty():
                    break
            # If queue has store file
            while queue.qsize() >= 1:
                # get elem
                elem = queue.get_nowait()
                # print('push elem %s' % elem)
                # publish the elemen to assign topic
                client.publish(MQTT_TOPIC, str(elem), qos=MQTT_QOS)
                # The loop it will stop when the queue is empty
                if queue.empty():
                    break
        else:
            # if there aren't connection
            client.connect_flag = False
            # It will be put data on the queue
            queue.put_nowait(data)
            # When the queue is ready for persistence
            if queue.qsize() == QSIZE:
                # transform queue objecto to queue
                deque = queue_to_deque(queue)
                # assign filename
                filename = create_filename(cfg.PICKLE.pickle_tmp)
                # It will be store on filesystem
                response = serialization_dump_obj(deque, filename)
                if response:
                    # if the serialization it was correct, put the filename on queue persistence
                    persistence.put_nowait(filename)
                    # restore queue
                    queue = asyncio.Queue()
    # Wait until all worker tasks are cancelled.
    print("tick toc")


asyncio.run(main())
