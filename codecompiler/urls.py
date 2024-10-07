from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from compiler.views import CodeSnippetViewSet

router = DefaultRouter()
router.register(r'codesnippets', CodeSnippetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compiler.urls')),  # Include the app's URLs
    path('api/', include(router.urls)),  # Include the API URLs
]