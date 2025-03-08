from django import forms
from apps.qrgenerator.models import Website  
from apps.cards.models import Card, OwnedCard, Pack, PackCards 
from django.contrib.gis.forms import PointField
from django.contrib.gis.forms.widgets import OSMWidget
class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'qr_code', 'location']
    location = PointField(widget=OSMWidget(attrs={'map_width': 600, 'map_height': 400}))

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name', 'image', 'card_desc', 'value']  # Add fields relevant to Card

class PackForm(forms.ModelForm):
    """Form to create a new Pack"""
    class Meta:
        model = Pack
        fields = ['pack_name', 'cost', 'num_cards', 'image']  # Adjust fields based on your model

class OwnedCardForm(forms.ModelForm):
    """Form to assign a Card to a User"""
    class Meta:
        model = OwnedCard
        fields = ['card', 'owner', 'quantity']  # Adjust based on your model
