from rest_framework import serializers
from .models import Message, MessageHistory

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read', 'attachment', 'parent_message']
        read_only_fields = ['sender', 'timestamp', 'read']


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message', 'replies']

    def get_replies(self, obj):
        # Recursive fetching of nested replies
        replies = obj.replies.all().select_related('sender', 'receiver')
        return MessageSerializer(replies, many=True).data
