# -- coding: utf-8 --
from __future__ import print_function

import paho.mqtt.client as mqtt
import struct
import time
import datetime
import json

#修改成自己的即可
DEV_ID = "529020612" #设备ID
PRO_ID = "248625" #产品ID
AUTH_INFO = "rD2gsXmuxf7EJr=BCX1aKifFPSg="  #APIKEY

TYPE_JSON = 0x01
TYPE_FLOAT = 0x17

def build_payload(type, payload):
    datatype = type
    packet = bytearray()
    packet.extend(struct.pack("!B", datatype))
    if isinstance(payload, str):
        udata = payload.encode('utf-8')
        length = len(udata)
        packet.extend(struct.pack("!H" + str(length) + "s", length, udata))
    return packet
 
def publish_data(client, IsTemp=True):
    #上传数据
    if IsTemp:
        filename = '/home/pi/xinzhu/tmp_data.txt'
        Id = "temp"
    else:
        filename = '/home/pi/xinzhu/hmd_data.txt'
        Id = "hum"
    flag = False
    file = open(filename, 'r')
    Value= float(file.read())
    json_body = json.dumps({
        "datastreams":[
                {
                    "id":Id,  #对应OneNet的数据流名称
                    "datapoints":[
                        {
                            "at":datetime.datetime.now().isoformat(), #数据提交时间，这里可通过函数来获取实时时间
                            "value":Value  #数据值
                            }
                        ]
                    }
                ]
            })
    packet = build_payload(TYPE_JSON, json_body)
    client.publish("$dp", packet, qos=1)  #qos代表服务质量

def main():
    client = mqtt.Client(client_id=DEV_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(username=PRO_ID, password=AUTH_INFO)
    client.connect('183.230.40.39', port=6002, keepalive=120)
    publish_data(client, IsTemp=True)
    publish_data(client, IsTemp=False)
    time.sleep(1)
    client.disconnect()
            
if __name__ == '__main__':
    main()
