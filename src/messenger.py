import paho.mqtt.client as mqtt
import os
import mail
import json

class Messenger:
    def __init__(self):
        self.connected = False
        self.mailClient = mail.Mail()

        #aufbau der MQTT-Verbindung
        self.mqttConnection = mqtt.Client()
        self.mqttConnection.on_connect = self.__onMQTTconnect
        self.mqttConnection.on_message = self.__onMQTTMessage

        #Definition einer Callback-Funktion für ein spezielles Topic
        self.mqttConnection.message_callback_add("mail/send", self.__mailMQTTSentcallback)

    def connect(self):
        if not self.connected:
            try:
                docker_container = os.environ.get('DOCKER_CONTAINER', False)
                if docker_container:
                    mqtt_address = "broker"
                else:
                    mqtt_address = "localhost"
                self.mqttConnection.connect(mqtt_address,1883,60)
            except:
                return False
        self.connected = True
        return True
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.mqttConnection.disconnect()
        return True

    def __onMQTTconnect(self,client,userdata,flags, rc):
        client.subscribe([("mail/send",0)])

    def __onMQTTMessage(self,client, userdata, msg):
        pass


    def __mailMQTTSentcallback(self,client, userdata, msg):
        try:
            mailData = json.loads(str(msg.payload.decode("utf-8")))
        except:
            print("Can't decode message")
            return

        reqKeys = ['to','subject','message']

        if not all(key in mailData for key in reqKeys):
            print("not all keys available")
            return
        
        self.mailClient.send(mailData['to'],mailData['subject'],mailData['message'])

    def foreverLoop(self):
        self.mqttConnection.loop_forever()