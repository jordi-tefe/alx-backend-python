from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status , generics, permissions
from .models import MessageHistory,Message
from .serializers import MessageHistorySerializer,MessageSerializer
from rest_framework.generics import ListAPIView ,RetrieveAPIView
from rest_framework.views import APIView

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

class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get messages sent by the authenticated user
        messages = Message.objects.filter(sender=request.user)\
            .select_related('receiver', 'sender', 'parent_message')\
            .prefetch_related('history')  # optimize history loading if needed

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageWithRepliesView(RetrieveAPIView):
    queryset = Message.objects.all().select_related('sender', 'receiver', 'edited_by', 'parent_message').prefetch_related('replies')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'pk'  # or 'id'

class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_at', 'edited_by', 'parent_message', 'replies']

    def get_replies(self, obj):
        replies = obj.replies.all().select_related('sender', 'receiver', 'edited_by')
        return MessageSerializer(replies, many=True).data

class MessageWithRepliesView(RetrieveAPIView):
    queryset = Message.objects.all().select_related('sender', 'receiver', 'edited_by', 'parent_message').prefetch_related('replies')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'pk'  # or 'id'
