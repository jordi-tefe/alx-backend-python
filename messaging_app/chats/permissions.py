#!/usr/bin/env python3
"""Custom permission classes for chats app."""
#!/usr/bin/env python3
"""Custom permission classes for chats app."""

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access its messages.
    """

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Only allow access if the user is a participant in the conversation.
        """
        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return user in obj.conversation.participants.all()
        return False
