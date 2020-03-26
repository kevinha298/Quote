
from django.contrib import admin
from django.urls import path, include

from core.views import QuoteView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('', QuoteView.as_view(), name='test')
]
