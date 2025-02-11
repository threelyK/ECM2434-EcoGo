from django.contrib import admin
from .models import *

admin.site.register(Card)
admin.site.register(OwnedCard)
admin.site.register(Pack)
admin.site.register(PackCards)
