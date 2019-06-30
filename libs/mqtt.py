import paho.mqtt.client as mqtt
import time

STATUS = {
    0: 'Connection successful',
    1: 'Connection refused – incorrect protocol version',
    2: 'Connection refused – invalid client identifier',
    3: 'Connection refused – server unavailable',
    4: 'Connection refused – bad username or password',
    5: 'Connection refused – not authorised',
    6: 'Currently unused',
}


class MQTTClient(mqtt.Client):
    STATUS = STATUS

    def __init__(self, cname, **kwargs):
        super(MQTTClient, self).__init__(cname, **kwargs)
        self.last_pub_time = time.time()
        self.topic_ack = []
        self.broker = None
        self.run_flag = True
        self.subscribe_flag = False
        self.bad_connection_flag = False
        self.connected_flag = True
        self.disconnect_flag = False
        self.qos = 0
        self.disconnect_time = 0.0
        self.pub_msg_count = 0
        self.devices = []

    @staticmethod
    def on_message_mqtt(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    @staticmethod
    def on_connect_mqtt(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK Returned code=", rc)
            return True
        print("Bad connection Returned code=", rc)
        return False

    def assign_callback(self, function, type):
        if type == 'message':
            self.on_message = function
        elif type == 'publish':
            self.on_publish = function
        elif type == 'log':
            self.on_log = function

    def check_connection(self):
        self.on_connect = MQTTClient.on_connect_mqtt
        self.connect(self.broker)
        self.loop()


def logging(client, userdata, level, buf):
    print("log: ", buf)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_publish(client, userdata, result):
    print("data published \n")


def sample():
    """
    https://pypi.org/project/paho-mqtt/#usage-and-api
        1. Create a client object.
        2. Create a client connection.
        3. publish the message
        4. Examine the return code of the publish request
        5. Examine the publish acknowledgement using the on_publish callback
    """
    client = MQTTClient('test1')
    print("connecting to broker")
    client.connect('172.17.0.1')
    client.assign_callback(on_message, type='message')
    print("Subscribing to topic", "house/bulbs/bulb1")
    client.publish("test/topic", "OFF", qos=0, retain=False)
