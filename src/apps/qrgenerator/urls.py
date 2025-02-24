from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.qr_code_list, name='qr_code_list'),  # Page of all generated QR Codes
    path('<slug:slug>/', views.website_detail, name='website_detail'),    # Creation of Website
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
## Currently http://127.0.0.1:8000/qrgenerator/ lists all the websites with a qr code while the slug path is qr/generator/(created Page Name here) is the sites with a QRCode on it