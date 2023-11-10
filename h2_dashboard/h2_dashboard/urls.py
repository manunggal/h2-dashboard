from django.contrib import admin
from django.urls import include, path
from h2_prod.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('h2_prod/', include('h2_prod.urls')),  # Include the app's URLs
]
