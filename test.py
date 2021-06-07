# written for Python3
# from https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-security
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
# you can use pip install paho-mqtt
from paho.mqtt import client as mqtt


def generate_sas_token(uri, key, policy_name, expiry=900):
    ttl = time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
    sign_key = sign_key.encode('utf-8')
    signature = b64encode(HMAC(b64decode(key), sign_key, sha256).digest())

    rawtoken = {
        'sr':  uri,
        'sig': signature,
        'se': str(int(ttl))
    }
    return 'SharedAccessSignature ' + urlencode(rawtoken)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe("devices/test/messages/devicebound/#")


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)


def on_message(client, userdata, msg):
    print(" - ".join((msg.topic, str(msg.payload))))
    # Do this only if you want to send a reply message every time you receive one
    client.publish("devices/test/messages/events", "REPLY", qos=1)


def on_publish(client, userdata, mid):
    print("Sent message")


device_id = "rpi-core"  # Add device id
iot_hub_name = "MWIoTHub"  # Add iot hub name
device_key = "lkG1pZn5PAGTNDsMBQlHtRw2zr6FNQJOcOO0yu0WLtE="

print(generate_sas_token(iot_hub_name +
      ".azure-devices.net/devices/" + device_id, device_key, device_id))
