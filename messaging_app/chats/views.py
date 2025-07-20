from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['participants']  # ✅ Allow filtering by user id using ?participants=ID

    def get_queryset(self):
        # Only show conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
