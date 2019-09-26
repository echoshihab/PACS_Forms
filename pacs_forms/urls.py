
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tech_forms.urls')),
    path('server-configs/', include('server_configs.urls'))
]
