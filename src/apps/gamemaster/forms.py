from django import forms
from apps.qrgenerator.models import Website  
from apps.cards.models import Card, OwnedCard, Pack, PackCards 

class WebsiteForm(forms.ModelForm):
    card = forms.ModelChoiceField(queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    class Meta:
        model = Website
        fields = ['name',  'latitude', 'longitude', 'address', 'card']

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
