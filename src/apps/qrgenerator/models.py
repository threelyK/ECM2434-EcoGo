import os
import qrcode
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils.text import slugify
from django.urls import reverse, get_resolver
from django.conf import settings
from uuid import uuid4
from apps.cards.views import add_card_website
## This stuff is used for creating a Website and saving a specific QRCode for specific templated and create Websites
class Website(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateField("Date", auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    url = models.URLField(max_length=200, blank=True, default='http://127.0.0.1:8000/', editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    latitude = models.FloatField(null=True, blank=True)  
    longitude = models.FloatField(null=True, blank=True)  
    address = models.CharField(max_length=255, null=True, blank=True) 
    card = models.ForeignKey('cards.Card', on_delete=models.SET_NULL, null=True, blank=True)  # Card to attach to webpage
    def __str__(self):
        return self.name


    #unused function but grabs own URL link
    def get_absolute_url(self):
        return reverse('website_detail', args=[self.id])  
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Ensures spaces become hyphens

        domain = settings.SITE_DOMAIN if hasattr(settings, "SITE_DOMAIN") else "http://127.0.0.1:8000" #site domain if we have one but nope.
        # Creating a UUID for the URL of the QR code
        new_id = str(uuid4())
        self.url = f"{domain}/cards/card-scan/{new_id}/"
        add_card_website(self.card, new_id)

        # Creates QR Code
        qr = qrcode.make(self.url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        fname = f'qr_code-{new_id}.png'
        self.qr_code.save(fname, File(buffer), save=False)

        buffer.close()

        super().save(*args, **kwargs)

        return self.qr_code.url

 