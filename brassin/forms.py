from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import brassin, recette, recette_ingredient,ingredient, brassin_ingredient, achat, vente
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.forms import ModelForm, HiddenInput, IntegerField, CharField, DecimalField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import AppendedText

class BrassinForm(forms.ModelForm):
	
	class Meta:
		model = brassin
		exclude = ['ingredient']
		widgets = {
			'date_brassin': DatePickerInput(),
			'date_mise_bouteille': DatePickerInput(),
			'temps_empatage': TimePickerInput(),
			'temps_fermentation': TimePickerInput(),
			'temps_ebullition': TimePickerInput(),}

	def __init__(self, *args, **kwargs):
		super(BrassinForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			AppendedText('volume_empatage', 'L'),
			AppendedText('volume_cuve_fermentation', 'L'),
			AppendedText('volume_mout', 'L'),
		)

class BrassinIngredientForm(forms.ModelForm):
	class Meta:
		model = brassin_ingredient
		fields = '__all__'
		widgets = {'brassin': forms.HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(BrassinIngredientForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			AppendedText('quantite', 'ouasi'),)

class RecetteForm(forms.ModelForm):
	class Meta:
		model = recette
		fields = '__all__'

class RecetteIngredientForm(forms.ModelForm):
	class Meta:
		model = recette_ingredient
		fields = '__all__'
		widgets = {'recette': forms.HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(RecetteIngredientForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			AppendedText('quantite', 'ouasi'),)

class IngredientForm(forms.ModelForm):
	class Meta:
		model = ingredient
		fields = '__all__'

class AchatForm(forms.ModelForm):
	class Meta:
		model = achat
		fields = '__all__'
		widgets = {
			'date_achat': DatePickerInput(),}

class VenteForm(forms.ModelForm):
	class Meta:
		model = vente
		fields = '__all__'
		widgets = {
			'date_vente': DatePickerInput(),}





		



