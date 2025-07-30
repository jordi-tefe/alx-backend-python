from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTests(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='sender')
        receiver = User.objects.create_user(username='receiver')
        Message.objects.create(sender=sender, receiver=receiver, content='Hello')

        self.assertEqual(Notification.objects.count(), 1)
def test_log_on_update(self):
    sender = User.objects.create_user(username='sender')
    receiver = User.objects.create_user(username='receiver')
    message = Message.objects.create(sender=sender, receiver=receiver, content='Initial')
    
    message.content = 'Updated message'
    message.save()
    # The log will be printed to the console when this test runs
