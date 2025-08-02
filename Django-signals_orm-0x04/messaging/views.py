from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status , generics, permissions
from .models import MessageHistory,Message
from .serializers import MessageHistorySerializer,MessageSerializer
from rest_framework.generics import ListAPIView

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)

class MessageHistoryView(generics.ListAPIView):
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        message_id = self.kwargs['message_id']
        return MessageHistory.objects.filter(message__id=message_id)

class MessageThreadView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Load all messages received or sent by the user, including replies
        return Message.objects.filter(
            sender=self.request.user
        ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')
