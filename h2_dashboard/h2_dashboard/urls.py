from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('h2_prod/', include('h2_prod.urls')),  # Include the app's URLs
]
