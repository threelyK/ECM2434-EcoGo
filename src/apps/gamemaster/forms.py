from django import forms
from apps.qrgenerator.models import Website  
from apps.cards.models import Card, OwnedCard, Pack, PackCards 

class WebsiteForm(forms.ModelForm):
    """Form to create Website"""
    card = forms.ModelChoiceField(queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    class Meta:
        model = Website
        fields = ['name',  'latitude', 'longitude', 'address', 'card']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name', 'image', 'card_desc', 'value']  
        widgets = {
            'card_name': forms.TextInput(attrs={'class': 'form-control'}), 
            'card_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
            'image' : forms.Textarea(attrs={'class': 'form-control', 'rows': 1} ),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),}

class PackForm(forms.ModelForm):
    """Form to create a new Pack"""
    class Meta:
        model = Pack
        fields = ['pack_name', 'cost', 'num_cards', 'image']
        widgets = {
            'pack_name' : forms.Textarea(attrs={'class': 'form-control', 'rows': 1} ),
            'image' : forms.Textarea(attrs={'class': 'form-control', 'rows': 1} )
        }

class OwnedCardForm(forms.ModelForm):
    """Form to assign a Card to a User"""
    class Meta:
        model = OwnedCard
        fields = ['card', 'owner', 'quantity']
