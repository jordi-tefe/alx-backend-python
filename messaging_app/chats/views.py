from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation  # import your custom permission

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['participants']  # allow filtering by participants

    def get_queryset(self):
        # Only show conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            # Return messages of the conversation only if user is a participant
            conversation = Conversation.objects.filter(id=conversation_id, participants=self.request.user).first()
            if conversation:
                return Message.objects.filter(conversation=conversation)
        return Message.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
