from django import forms
from apps.qrgenerator.models import Website  
from apps.cards.models import Card, OwnedCard, Pack, PackCards 

class WebsiteForm(forms.ModelForm):
    """Form to create a Website"""
    card = forms.ModelChoiceField(queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    class Meta:
        model = Website
        fields = ['name',  'latitude', 'longitude', 'address', 'card']

class CardForm(forms.ModelForm):
    """"Form to create Card"""
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

class PackCreationForm(forms.Form): # Was originally forms.ModelForm
    """Form to populate new Pack"""
    pack_name = forms.CharField(label="Pack Name", max_length=100)
    pack_cost = forms.IntegerField(label="Pack Cost", min_value=0)
    pack_image = forms.CharField(label="Image", max_length=150, initial="images/card_images/Missing_Texture.png")

    card1 = forms.ModelChoiceField(label="Card 1", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity1 = forms.IntegerField(label="Rarity", min_value=1)

    card2 = forms.ModelChoiceField(label="Card 2", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity2 = forms.IntegerField(label="Rarity", min_value=1)

    card3 = forms.ModelChoiceField(label="Card 3", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity3 = forms.IntegerField(label="Rarity", min_value=1)
    
    card4 = forms.ModelChoiceField(label="Card 4", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity4 = forms.IntegerField(label="Rarity", min_value=1)
    
    card5 = forms.ModelChoiceField(label="Card 5", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity5 = forms.IntegerField(label="Rarity", min_value=1)

    card6 = forms.ModelChoiceField(label="Card 6", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity6 = forms.IntegerField(label="Rarity", min_value=1)

    card7 = forms.ModelChoiceField(label="Card 7", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity7 = forms.IntegerField(label="Rarity", min_value=1)

    card8 = forms.ModelChoiceField(label="Card 8", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity8 = forms.IntegerField(label="Rarity", min_value=1)

    card9 = forms.ModelChoiceField(label="Card 9", queryset=Card.objects.all(), required=False, empty_label="Select a Card")
    rarity9 = forms.IntegerField(label="Rarity", min_value=1)

    card10 = forms.ModelChoiceField(label="Card 10", queryset=Card.objects.all(), required=False, empty_label="Select aCard")
    rarity10 = forms.IntegerField(label="Rarity", min_value=1)

class OwnedCardForm(forms.ModelForm):
    """Form to assign a Card to a User"""
    class Meta:
        model = OwnedCard
        fields = ['card', 'owner', 'quantity']
