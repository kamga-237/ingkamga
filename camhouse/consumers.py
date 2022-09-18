import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
import time

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        idh = text_data_json['idh']
        user = text_data_json['user']
        d=time.time()
        etat=0
        info = House.objects.filter(id=idh)
        for donnee in info:
            proprio = donnee.user.id

        sauvMessage = Message(send=user, date=d, etat=etat, receve_id= proprio, house_id= idh, sms= message)
        sauvMessage.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user': user

            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        print(user)

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'user': user
        }))