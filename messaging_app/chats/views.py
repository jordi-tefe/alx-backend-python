from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['participants']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)  # enforces custom permission
        return super().retrieve(request, *args, **kwargs)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id, participants=self.request.user).first()
            if conversation:
                return Message.objects.filter(conversation=conversation)
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if conversation and self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
