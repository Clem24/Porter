from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from datetime import datetime

from .models import note, brassin, brassin_ingredient, recette, ingredient, achat, vente, recette_ingredient
from .forms import NoteForm, BrassinForm, RecetteForm, BrassinIngredientForm, IngredientForm, AchatForm, VenteForm,RecetteIngredientForm,ConnexionForm

#-------------------------------------------------------------------------------------------------------------
# CONNEXION
#-------------------------------------------------------------------------------------------------------------
def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('brassin_list')
            else:
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion.html', locals())

@login_required
def deconnexion(request):
    logout(request)
    return redirect('connexion')

#-------------------------------------------------------------------------------------------------------------
# NOTE
#-------------------------------------------------------------------------------------------------------------

class NoteCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = note
	template_name = 'brassin/note_create_form.html'
	form_class = NoteForm
	success_url =  reverse_lazy('brassin_list')
	permission_required = 'note.add_choice'

	def form_valid(self, form):
		n = form.save(commit=False)
		n.auteur = self.request.user.username
		n.date = datetime.now()
		n.save()
		return super().form_valid(form)

class NoteUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = note
	id = note.id
	template_name = 'brassin/note_update_form.html'
	form_class = NoteForm
	success_url =  reverse_lazy('brassin_list')
	permission_required = 'note.change_choice'

class NoteDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = note
    template_name = 'brassin/note_delete_form.html'
    success_url = reverse_lazy('brassin_list')
    permission_required = 'note.delete_choice'

#-------------------------------------------------------------------------------------------------------------
# BRASSIN
#-------------------------------------------------------------------------------------------------------------

@login_required
def BrassinsList(request):
    brassins = brassin.objects.all()
    total_brassins = brassin.objects.all().count()
    notes = note.objects.all()
    return render(request, "brassin/brassin_list.html", {'brassins': brassins,'notes':notes,'total': total_brassins})

class BrassinCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = brassin
	template_name = 'brassin/brassin_create_form.html'
	form_class = BrassinForm
	permission_required = 'brassin.add_choice'
	success_url =  reverse_lazy('brassin_list')

class BrassinUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = brassin
	id = brassin.id
	template_name = 'brassin/brassin_update_form.html'
	form_class = BrassinForm
	permission_required = 'brassin.change_choice'
	success_url = "/brassin/consult-{id}"

class BrassinDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = brassin
    template_name = 'brassin/brassin_delete_form.html'
    permission_required = 'brassin.delete_choice'
    success_url = reverse_lazy('brassin_list')

def BrassinConsult(request, id):
	b = get_object_or_404(brassin, id=id)
	bi = brassin_ingredient.objects.all().filter(brassin=b)
	try:
		r = recette.objects.get(id=b.recette_id)
	except recette.DoesNotExist:
		r = None
	return render(request, 'brassin/brassin_consulter.html', {'brassin': b,'brassin_ingredient':bi,'recette':r})

#-------------------------------------------------------------------------------------------------------------
# BRASSIN INGREDIENT
#-------------------------------------------------------------------------------------------------------------

@login_required
@permission_required('brassin_ingredient.add_choice', raise_exception=True)
def BrassinIngredientAdd(request,id):

	if request.method == 'POST':
		form = BrassinIngredientForm(request.POST)
		form.fields["brassin"].initial = id
		form.fields["achete"].initial = True

		if form.is_valid():
		    data = form.cleaned_data
		    if "Levure" in str(data["ingredient"]):
		        message = "Paquets de " + str(data["ingredient"]) + " ajouté: "  + str(data["quantite"])
		    else:
		        message = str(data["quantite"]) + " kg de " + str(data["ingredient"]) + " ont étés ajoutés."
		    form.save()
		    messages.success(request, message)
	else:
		form = BrassinIngredientForm()
		form.fields["brassin"].initial = id
		form.fields["achete"].initial = True
	return render(request, 'brassin/brassin_ingredient_add_form.html', {'form': form})

class BrassinIngredientDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = brassin_ingredient
    brassin_id = brassin_ingredient.brassin
    template_name = 'brassin/brassin_ingredient_delete_form.html'
    permission_required = 'brassin_ingredient.delete_choice'
    success_url = "/brassin/consult-{brassin_id}"


#-------------------------------------------------------------------------------------------------------------
# RECETTE
#-------------------------------------------------------------------------------------------------------------

class RecettesList(LoginRequiredMixin,ListView):
	model = recette
	context_object_name = "recettes"
	template_name = "brassin/recettes_list.html"

class RecetteCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = recette
	template_name = 'brassin/recette_create_form.html'
	form_class = RecetteForm
	permission_required = 'recette.add_choice'
	success_url =  reverse_lazy('recettes_list')

class RecetteUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = recette
	id = recette.id
	template_name = 'brassin/recette_update_form.html'
	form_class = RecetteForm
	permission_required = 'recette.change_choice'
	success_url = "/brassin/recette/consult-{id}"

class RecetteDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = recette
    template_name = 'brassin/recette_delete_form.html'
    permission_required = 'recette.delete_choice'
    success_url = reverse_lazy('recettes_list')

@login_required
def RecetteConsult(request, id):
	r = get_object_or_404(recette, id=id)
	ri = recette_ingredient.objects.all().filter(recette=r)
	dataset_chart_recette = brassin.objects.all().filter(recette=r).exclude(densite_initiale__isnull=True).values('id','date_brassin', 'densite_initiale','densite_finale')
	return render(request, 'brassin/recette_consulter.html', {'recette': r,'recette_ingredient':ri,'dataset_chart_recette':dataset_chart_recette})

#-------------------------------------------------------------------------------------------------------------
# RECETTE INGREDIENT
#-------------------------------------------------------------------------------------------------------------
@login_required
@permission_required('recette_ingredient.add_choice', raise_exception=True)
def RecetteIngredientAdd(request,id):

	if request.method == 'POST':
		form = RecetteIngredientForm(request.POST)
		form.fields["recette"].initial = id

		if form.is_valid():
			data = form.cleaned_data
			if "Levure" in str(data["ingredient"]):
			    message = str(data["ingredient"]) + " ajouté."
			elif "Malt" in str(data["ingredient"]):
			    message = str(data["quantite"])+ " % masse totale de " + str(data["ingredient"]) + " ajouté."
			else:
			    message = str(data["quantite"]) + " g/l de " + str(data["ingredient"]) + " ont étés ajoutés."
			form.save()
			messages.success(request, message)
	else:
		form = RecetteIngredientForm()
		form.fields["recette"].initial = id
	return render(request, 'brassin/recette_ingredient_add_form.html', {'form': form})

class RecetteIngredientDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = recette_ingredient
    brassin_id = recette_ingredient.recette
    template_name = 'brassin/recette_ingredient_delete_form.html'
    permission_required = 'recette_ingredient.delete_choice'
    success_url = "/brassin/recette/consult-{recette_id}"

#-------------------------------------------------------------------------------------------------------------
# INGREDIENTS
#-------------------------------------------------------------------------------------------------------------

class IngredientsList(LoginRequiredMixin,ListView):
	model = ingredient
	template_name = "brassin/ingredients_list.html"

	def get_context_data(self, **kwargs):
	    context = super(IngredientsList, self).get_context_data(**kwargs)
	    context['malt'] = ingredient.objects.filter(type_ingredient="Malt")
	    context['houblon'] = ingredient.objects.filter(type_ingredient="Houblon")
	    context['levure'] = ingredient.objects.filter(type_ingredient="Levure")
	    context['autre'] = ingredient.objects.filter(type_ingredient="Autre")
	    return context

class IngredientCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = ingredient
	template_name = 'brassin/ingredient_create_form.html'
	form_class = IngredientForm
	permission_required = 'ingredient.add_choice'
	success_url =  reverse_lazy('ingredients_list')

class IngredientUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = ingredient
	template_name = 'brassin/ingredient_update_form.html'
	form_class = IngredientForm
	permission_required = 'ingredient.change_choice'
	success_url =  reverse_lazy('ingredients_list')


class IngredientDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
	model = ingredient
	template_name = 'brassin/ingredient_delete_form.html'
	form_class = IngredientForm
	permission_required = 'ingredient.delete_choice'
	success_url =  reverse_lazy('ingredients_list')

#-------------------------------------------------------------------------------------------------------------
# ACHATS
#-------------------------------------------------------------------------------------------------------------

class AchatsList(LoginRequiredMixin,ListView):
	model = achat
	context_object_name = "achats"
	template_name = "brassin/achats_list.html"
	ordering = ['-date_achat']

	def get_context_data(self, **kwargs):
	    context = super(AchatsList, self).get_context_data(**kwargs)
	    achats = achat.objects.all()
	    context['achat'] = achats
	    context['fonctionnement'] = achat.objects.filter(type_achat='Fonctionnement').order_by('-date_achat')
	    prix_achat = 0
	    for a in achats:
	        prix_achat += a.ingredient.prix_kg*a.quantite
	    context['total_achats'] = prix_achat
	    return context

class AchatCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = achat
	template_name = 'brassin/achat_create_form.html'
	form_class = AchatForm
	permission_required = 'achat.add_choice'
	success_url =  reverse_lazy('achats_list')

class AchatUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = achat
	template_name = 'brassin/achat_update_form.html'
	form_class = AchatForm
	permission_required = 'achat.change_choice'
	success_url = reverse_lazy('achats_list')

class AchatDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = achat
    template_name = 'brassin/achat_delete_form.html'
    permission_required = 'achat.delete_choice'
    success_url = reverse_lazy('achats_list')

#-------------------------------------------------------------------------------------------------------------
# VENTES
#-------------------------------------------------------------------------------------------------------------

class VentesList(LoginRequiredMixin,ListView):
	model = vente
	context_object_name = "ventes"
	template_name = "brassin/ventes_list.html"
	ordering = ['-date_vente']

	def get_context_data(self, **kwargs):
	    context = super(VentesList, self).get_context_data(**kwargs)
	    context['vente'] = vente.objects.all()
	    context['total_recettes'] = vente.objects.all().aggregate(sum_all=Sum('prix')).get('sum_all')
	    context['total_bouteilles_vendues'] = vente.objects.all().aggregate(sum_all=Sum('quantite')).get('sum_all')
	    return context

class VenteCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = vente
	template_name = 'brassin/vente_create_form.html'
	form_class = VenteForm
	permission_required = 'vente.add_choice'
	success_url =  reverse_lazy('ventes_list')

	def form_valid(self, form):
		v = form.save(commit=False)
		v.vendeur = self.request.user.username
		v.save()
		return super().form_valid(form)

class VenteUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = vente
	template_name = 'brassin/vente_update_form.html'
	form_class = VenteForm
	permission_required = 'vente.change_choice'
	success_url = reverse_lazy('ventes_list')

class VenteDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = vente
    template_name = 'brassin/vente_delete_form.html'
    permission_required = 'vente.delete_choice'
    success_url = reverse_lazy('ventes_list')


#-------------------------------------------------------------------------------------------------------------
# OUTILS
#-------------------------------------------------------------------------------------------------------------

@login_required
def Outils(request,id=0):
	if id != 0:
		b = brassin.objects.get(id=id)
	else:
		b = brassin.objects.latest('id')
	r = recette.objects.get(id=b.recette_id)
	if r is None:
	    r = recette.objects.get(id=1)
	return render(request, "brassin/outils.html", {'brassin_x': b,'recette':r})

