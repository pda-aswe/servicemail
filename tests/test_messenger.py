from src import messenger
from unittest.mock import patch, ANY, MagicMock
import json

@patch("mail.Mail")
def test_connect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.connect()
        mock_connect.connect.assert_called_with("localhost",1883,60)

@patch("mail.Mail")
def test_disconnect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'connected', True), patch.object(obj, 'mqttConnection') as mock_connect:
        obj.disconnect()
        mock_connect.disconnect.assert_called()

@patch("mail.Mail")
def test_foreverLoop(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.foreverLoop()
        mock_connect.loop_forever.assert_called()

@patch("mail.Mail")
def test_onMQTTconnect(mock_travel):
    obj = messenger.Messenger()

    mock_client = MagicMock()

    obj._Messenger__onMQTTconnect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([("mail/send",0)])


@patch("mail.Mail")
def test_onMQTTMessage(mock_travel):
    obj = messenger.Messenger()

    try:
        obj._Messenger__onMQTTMessage(MagicMock(),None,None)
        assert True
    except:
        assert False

class DummyMSG:
    def __init__(self):
        self.payload = "Test"

    def set_payload(self,data):
        self.payload = str.encode(data)

@patch("mail.Mail")
def test_mailMQTTRideTimecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
        "to":"test@test.de",
        "subject":"Testsubject",
        "message":[
            "line 1",
            "line 2"
        ]
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'mailClient') as mock_mail:
        obj._Messenger__mailMQTTSentcallback(None,None,responseData)
        mock_mail.send.assert_called_with('test@test.de', 'Testsubject', ['line 1', 'line 2'])