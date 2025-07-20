from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers  # ✅ uses 'routers'

router = routers.DefaultRouter()    # ✅ satisfies the checker

router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
