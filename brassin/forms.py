from django import forms
from .models import note, brassin, recette, recette_ingredient,ingredient, brassin_ingredient, achat, vente
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class NoteForm(forms.ModelForm):
	class Meta:
		model = note
		exclude = ['auteur','date']
		fields = '__all__'

class BrassinForm(forms.ModelForm):
	volume_empatage = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'L'}))
	volume_cuve_fermentation = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'L'}))
	volume_mout = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'L'}))
	volume_starter = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'L'}))
	volume_rincage_dreches = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'L'}))
	resucrage = forms.DecimalField(required=False, max_digits=2, min_value=0,widget= forms.TextInput(attrs={'placeholder':'g/L'}))
	temperature_brassage = forms.DecimalField(required=False, max_digits=3, min_value=0,widget= forms.TextInput(attrs={'placeholder':'°C'}))

	class Meta:
		model = brassin
		exclude = ['ingredient']
		attrs = {'class':'form-control'}
		widgets = {
			'date_brassin': DatePickerInput(format='%d/%m/%Y'),
			'date_mise_bouteille': DatePickerInput(format='%d/%m/%Y'),
			'temps_empatage': TimePickerInput(),
			'temps_fermentation': TimePickerInput(),
			'temps_ebullition': TimePickerInput(),}

class BrassinIngredientForm(forms.ModelForm):
	quantite = forms.DecimalField(required=True, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'kg'}))

	class Meta:
		model = brassin_ingredient
		fields = '__all__'
		widgets = {
			'brassin': forms.HiddenInput(),
			'quantite': forms.TextInput(attrs={'placeholder': 'kg'}),
			'temps_infusion': TimePickerInput(),}

class RecetteForm(forms.ModelForm):
	class Meta:
		model = recette
		fields = '__all__'

class RecetteIngredientForm(forms.ModelForm):
	quantite = forms.DecimalField(required=True, max_digits=6, min_value=0)

	class Meta:
		model = recette_ingredient
		fields = '__all__'
		widgets = {
			'recette': forms.HiddenInput(),
			'quantite': forms.TextInput(attrs={'placeholder': '%'}),
			'temps_infusion': TimePickerInput(),}

class IngredientForm(forms.ModelForm):
	prix_kg = forms.DecimalField(required=False, max_digits=6, min_value=0,widget= forms.TextInput(attrs={'placeholder':'€/kg'}))
	ebc_min = forms.DecimalField(required=False, max_digits=4, min_value=0)
	ebc_max = forms.DecimalField(required=False, max_digits=4, min_value=0)
	acide_alpha = forms.DecimalField(required=False, max_digits=2, min_value=0,widget= forms.TextInput(attrs={'placeholder':'%'}))
	attenuation_min = forms.DecimalField(required=False, max_digits=2, min_value=0,widget= forms.TextInput(attrs={'placeholder':'%'}))
	attenuation_max = forms.DecimalField(required=False, max_digits=3, min_value=0,widget= forms.TextInput(attrs={'placeholder':'%'}))

	class Meta:
		model = ingredient
		fields = '__all__'

class AchatForm(forms.ModelForm):
	class Meta:
		model = achat
		fields = '__all__'
		widgets = {
			'date_achat': DatePickerInput(format='%d/%m/%Y'),}

class VenteForm(forms.ModelForm):
    brassin = forms.ModelChoiceField(queryset=brassin.objects.exclude(date_mise_bouteille__isnull=True),initial=brassin.objects.exclude(date_mise_bouteille__isnull=True).latest('date_brassin'))
    class Meta:
        model = vente
        exclude = ['vendeur']
        widgets = {
			'date_vente': DatePickerInput(format='%d/%m/%Y'),}




