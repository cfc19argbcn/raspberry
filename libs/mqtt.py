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

    def __init__(self, cname, broker='172.17.0.1', port=1883, **kwargs):
        """
        :param cname:
        :param kwargs:
        """
        super(MQTTClient, self).__init__(cname, **kwargs)
        self.last_pub_time = time.time()
        self.topic_ack = []
        self.broker = broker
        self.port = port
        self.connect_flag = False
        self.reconnect_flag = False
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
        """
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        print(msg.topic + " " + str(msg.payload))

    @staticmethod
    def on_connect_mqtt(client, userdata, flags, rc):
        """
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        if rc == 0:
            print("connected OK Returned code=", rc)
            return True
        print("Bad connection Returned code=", rc)
        return False

    def disconnect_flag(self, reconnect=None, connected=None):
        if reconnect in (False, True):
            self.reconnect_flag = reconnect
        elif connected in (False, True):
            self.connect_flag = connected
        else:
            self.connect_flag = False
            self.reconnect_flag = False

    def assign_callback(self, function, type):
        """
        :param function:
        :param type:
        :return:
        """
        if type == 'message':
            self.on_message = function
        elif type == 'publish':
            self.on_publish = function
        elif type == 'log':
            self.on_log = function
        elif type == 'connect':
            self.on_connect = function

    def checking(self):
        """
        :return:
        """
        try:
            self.connect(self.broker, self.port)
            self.loop()
            return True
        except:
            return False


def logging(client, userdata, level, buf):
    """
    :param client:
    :param userdata:
    :param level:
    :param buf:
    :return:
    """
    print("log: ", buf)


def on_message(client, userdata, message):
    """
    :param client:
    :param userdata:
    :param message:
    :return:
    """
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_publish(client, userdata, result):
    print("data published \n")
