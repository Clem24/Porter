from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import brassin, brassin_ingredient, recette, ingredient, achat, vente, recette_ingredient
from .forms import BrassinForm, RecetteForm, BrassinIngredientForm, IngredientForm, AchatForm, VenteForm,RecetteIngredientForm

#-------------------------------------------------------------------------------------------------------------
# BRASSIN
#-------------------------------------------------------------------------------------------------------------

class BrassinsList(ListView):
	model = brassin
	context_object_name = "derniers_brassins"
	template_name = "brassin/brassin_list.html"
	ordering = ['-date_brassin']

class BrassinCreate(CreateView):
	model = brassin
	template_name = 'brassin/brassin_create_form.html'
	form_class = BrassinForm
	success_url =  reverse_lazy('brassin_list')

class BrassinUpdate(UpdateView):
	model = brassin
	id = brassin.id
	template_name = 'brassin/brassin_update_form.html'
	form_class = BrassinForm
	success_url = "/brassin/consult-{id}"

class BrassinDelete(DeleteView):
    model = brassin
    template_name = 'brassin/brassin_delete_form.html'
    success_url = reverse_lazy('brassin_list')

def BrassinConsult(request, id):
	b = get_object_or_404(brassin, id=id)
	bi = brassin_ingredient.objects.all().filter(brassin=b)
	r = recette.objects.get(id=b.recette_id)
	return render(request, 'brassin/brassin_consulter.html', {'brassin': b,'brassin_ingredient':bi,'recette':r})

#-------------------------------------------------------------------------------------------------------------
# BRASSIN INGREDIENT
#-------------------------------------------------------------------------------------------------------------

def BrassinIngredientAdd(request,id):

	if request.method == 'POST':
		form = BrassinIngredientForm(request.POST)
		form.fields["brassin"].initial = id
		form.fields["achete"].initial = True
		if form.is_valid():
			data = form.cleaned_data
			message = str(data["quantite"]) + " kg de " + str(data["ingredient"]) + " ont étés ajoutés."
			form.save()
			messages.success(request, message)
	else:
		form = BrassinIngredientForm()
		form.fields["brassin"].initial = id
		form.fields["achete"].initial = True
	return render(request, 'brassin/brassin_ingredient_add_form.html', {'form': form})

class BrassinIngredientDelete(DeleteView):
    model = brassin_ingredient
    brassin_id = brassin_ingredient.brassin
    template_name = 'brassin/brassin_ingredient_delete_form.html'
    success_url = "/brassin/consult-{brassin_id}"


#-------------------------------------------------------------------------------------------------------------
# RECETTE
#-------------------------------------------------------------------------------------------------------------

class RecettesList(ListView):
	model = recette
	context_object_name = "recettes"
	template_name = "brassin/recettes_list.html"

class RecetteCreate(CreateView):
	model = recette
	template_name = 'brassin/recette_create_form.html'
	form_class = RecetteForm
	success_url =  reverse_lazy('recettes_list')

class RecetteUpdate(UpdateView):
	model = recette
	id = recette.id
	template_name = 'brassin/recette_update_form.html'
	form_class = RecetteForm
	success_url = "/brassin/recette/consult-{id}"

class RecetteDelete(DeleteView):
    model = recette
    template_name = 'brassin/recette_delete_form.html'
    success_url = reverse_lazy('recettes_list')

def RecetteConsult(request, id):
	r = get_object_or_404(recette, id=id)
	ri = recette_ingredient.objects.all().filter(recette=r)
	return render(request, 'brassin/recette_consulter.html', {'recette': r,'recette_ingredient':ri})

#-------------------------------------------------------------------------------------------------------------
# RECETTE INGREDIENT
#-------------------------------------------------------------------------------------------------------------

def RecetteIngredientAdd(request,id):

	if request.method == 'POST':
		form = RecetteIngredientForm(request.POST)
		form.fields["recette"].initial = id

		if form.is_valid():
			data = form.cleaned_data
			message = str(data["quantite"]) + " kg de " + str(data["ingredient"]) + " ont étés ajoutés."
			form.save()
			messages.success(request, message)
	else:
		form = RecetteIngredientForm()
		form.fields["recette"].initial = id
	return render(request, 'brassin/recette_ingredient_add_form.html', {'form': form})

class RecetteIngredientDelete(DeleteView):
    model = recette_ingredient
    brassin_id = recette_ingredient.recette
    template_name = 'brassin/recette_ingredient_delete_form.html'
    success_url = "/brassin/recette/consult-{recette_id}"

#-------------------------------------------------------------------------------------------------------------
# INGREDIENTS
#-------------------------------------------------------------------------------------------------------------

class IngredientsList(ListView):
	model = ingredient
	template_name = "brassin/ingredients_list.html"

	def get_context_data(self, **kwargs):
		context = super(IngredientsList, self).get_context_data(**kwargs)
		context['malt'] = ingredient.objects.filter(type_ingredient="Malt")
		context['houblon'] = ingredient.objects.filter(type_ingredient="Houblon")
		context['levure'] = ingredient.objects.filter(type_ingredient="Levure")
		context['autre'] = ingredient.objects.filter(type_ingredient="Autre")
		return context

class IngredientCreate(CreateView):
	model = ingredient
	template_name = 'brassin/ingredient_create_form.html'
	form_class = IngredientForm
	success_url =  reverse_lazy('ingredients_list')
		
class IngredientUpdate(UpdateView):
	model = ingredient
	template_name = 'brassin/ingredient_update_form.html'
	form_class = IngredientForm
	success_url =  reverse_lazy('ingredients_list')

		
class IngredientDelete(DeleteView):
	model = ingredient
	template_name = 'brassin/ingredient_delete_form.html'
	form_class = IngredientForm
	success_url =  reverse_lazy('ingredients_list')

#-------------------------------------------------------------------------------------------------------------
# ACHATS
#-------------------------------------------------------------------------------------------------------------

class AchatsList(ListView):
	model = achat
	context_object_name = "achats"
	template_name = "brassin/achats_list.html"
	ordering = ['-date_achat']

class AchatCreate(CreateView):
	model = achat
	template_name = 'brassin/achat_create_form.html'
	form_class = AchatForm
	success_url =  reverse_lazy('achats_list')

class AchatUpdate(UpdateView):
	model = achat
	template_name = 'brassin/achat_update_form.html'
	form_class = AchatForm
	success_url = reverse_lazy('achats_list')

class AchatDelete(DeleteView):
    model = achat
    template_name = 'brassin/achat_delete_form.html'
    success_url = reverse_lazy('achats_list')

#-------------------------------------------------------------------------------------------------------------
# ACHATS
#-------------------------------------------------------------------------------------------------------------

class VentesList(ListView):
	model = vente
	context_object_name = "ventes"
	template_name = "brassin/ventes_list.html"
	ordering = ['-date_vente']

class VenteCreate(CreateView):
	model = vente
	template_name = 'brassin/vente_create_form.html'
	form_class = VenteForm
	success_url =  reverse_lazy('ventes_list')

class VenteUpdate(UpdateView):
	model = vente
	template_name = 'brassin/vente_update_form.html'
	form_class = VenteForm
	success_url = reverse_lazy('ventes_list')

class VenteDelete(DeleteView):
    model = vente
    template_name = 'brassin/vente_delete_form.html'
    success_url = reverse_lazy('ventes_list')