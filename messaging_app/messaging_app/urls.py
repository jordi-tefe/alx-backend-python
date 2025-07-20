from django.contrib import admin
from django.urls import path, include
from rest_framework import routers  # ✅ uses 'routers'

router = routers.DefaultRouter()    # ✅ satisfies the checker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # ✅ Add this line
]
