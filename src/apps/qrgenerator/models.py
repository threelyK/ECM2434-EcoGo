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
## This stuff is used for creating a Website and saving a specific QRCode for specific templated and create Websites
class Website(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateField("Date", auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    url = models.URLField(max_length=200, blank=True, default='http://127.0.0.1:8000/', editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


    #unused function but grabs own URL link
    def get_absolute_url(self):
        return reverse('website_detail', args=[self.id])  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Ensures spaces become hyphens

        domain = settings.SITE_DOMAIN if hasattr(settings, "SITE_DOMAIN") else "http://127.0.0.1:8000" #site domain if we have one but nope.
        self.url = f"{domain}/qrgenerator/{self.slug}/"

        # Creates QR Code
        qr = qrcode.make(self.url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        fname = f'qr_code-{self.slug}.png'
        self.qr_code.save(fname, File(buffer), save=False)

        buffer.close()

        super().save(*args, **kwargs)

    ## my failure of attempt to create a QR code for templates automatically 
    @staticmethod
    def get_user_urls():
        user_urls = []
        resolver = get_resolver()
        for pattern in resolver.reverse_dict.keys():
            if isinstance(pattern, str) and pattern not in ["admin", "qrgenerator"]:  
                user_urls.append(pattern)  
        return user_urls
    ## failure for adding to Websites Templated QRCodes
    @classmethod
    def create_from_templates(cls):
        templates_path = os.path.join(settings.BASE_DIR, "apps/user/templates/")
        if os.path.exists(templates_path):
            for file in os.listdir(templates_path):
                if file.endswith(".html"):
                    name = file.replace(".html", "")
                    slug = name.replace(" ", "-").lower()
                    if not cls.objects.filter(slug=slug).exists():
                        cls.objects.create(name=name, slug=slug)
