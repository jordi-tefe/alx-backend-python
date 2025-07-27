#!/usr/bin/env python3
"""Custom permission classes for chats app."""
#!/usr/bin/env python3
"""Custom permission classes for chats app."""

from rest_framework.permissions import BasePermission

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    Checks permissions for safe and unsafe methods.
    """

    def has_permission(self, request, view):
        # Check that user is authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow participants to access or modify the object
        user_is_participant = False
        if hasattr(obj, 'participants'):
            user_is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            user_is_participant = request.user in obj.conversation.participants.all()

        if not user_is_participant:
            return False

        # For unsafe methods, allow only if participant
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return user_is_participant

        # Allow safe methods (GET, HEAD, OPTIONS) if participant
        return True
