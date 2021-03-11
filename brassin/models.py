from django.db import models
from django.db.models import Sum
from decimal import *
from math import exp, expm1
from datetime import datetime
from django.contrib.auth.models import User

class ingredient(models.Model):
	INGREDIENT_TYPE = [('Malt','Malt'),('Houblon','Houblon'),('Levure','Levure'),('Autre','Autre'),]
	type_ingredient = models.CharField(null=True,max_length=30,choices=INGREDIENT_TYPE,default='Autre')
	variete = models.CharField(max_length=30)
	prix_kg = models.DecimalField(null=True, max_digits=5, decimal_places=2)
	acide_alpha = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=2)
	ebc_min = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=0)
	ebc_max = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=0)
	attenuation_min = models.DecimalField(blank=True,null=True, max_digits=2, decimal_places=0)
	attenuation_max = models.DecimalField(blank=True,null=True, max_digits=2, decimal_places=0)
	description = models.TextField(blank=True,null=True)

	@property
	def stock(self):
		achat_sum = achat.objects.filter(ingredient=self.id).aggregate(Sum('quantite')).get('quantite__sum',0.00) if achat else 0.00
		brassin_sum = brassin_ingredient.objects.filter(ingredient=self.id).aggregate(Sum('quantite')).get('quantite__sum',0.00) if brassin_ingredient else 0.00
		if not achat_sum:
			return brassin_sum
		if not brassin_sum:
			return achat_sum
		return achat_sum - brassin_sum

	@property
	def unite(self):
	    if self.type_ingredient=="Malt":
	        return "%"
	    else:
	        return "g/L"

	@property
	def ebc(self):
		if not self.ebc_min or not self.ebc_max:
			return
		return (self.ebc_min + self.ebc_max)/2

	@property
	def attenuation(self):
		if not self.attenuation_min or not self.attenuation_max:
			return
		return (self.attenuation_min + self.attenuation_max)/2

	@property
	def propriete(self):
		if self.type_ingredient=="Malt":
			return "EBC: " + str(self.ebc_min) + " - " + str(self.ebc_max)
		if self.type_ingredient=="Houblon":
			return "Acide alpha: " + str(self.acide_alpha) + " %"
		if self.type_ingredient=="Levure":
			return "Attenuation: " + str(self.attenuation_min) + " - " + str(self.attenuation_max) + " %"
		else:
			return ""

	class Meta:
		verbose_name = "Ingredient"
		ordering = ['type_ingredient']

	def __str__(self):
		return self.type_ingredient + " - " + self.variete

class recette(models.Model):
	nom = models.CharField(max_length=30)
	type_biere = models.CharField(blank=True,null=True,max_length=30)
	densite_desire = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=3)
	taux_empatage =  models.DecimalField(max_digits=4, decimal_places=3,default=0.3)
	resucrage = models.DecimalField(blank=True,null=True, max_digits=3, decimal_places=1,default=7)
	notes = models.TextField(blank=True,null=True)

	@property
	def nombre_brassin(self):
		return brassin.objects.filter(recette=self.id).count()

	class Meta:
		verbose_name = "Recette"
		ordering = ['id']

	def __str__(self):
		return self.nom

class note(models.Model):
    date = models.DateField(null=True)
    titre = models.CharField(null=True, blank= True,max_length=30)
    texte = models.TextField(blank=False,null=False)
    auteur = models.CharField(null=True, blank= True,max_length=30)

    class Meta:
        verbose_name = "Notes"
        ordering = ['-date']

class brassin(models.Model):
	date_brassin = models.DateField(null=True)
	date_mise_bouteille = models.DateField(blank=True,null=True)
	densite_avant_ebullition = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=3)
	densite_initiale = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=3)
	densite_finale = models.DecimalField(blank=True,null=True, max_digits=4, decimal_places=3)
	volume_empatage = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=1)
	volume_rincage_dreches = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=1)
	volume_mout = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=1)
	volume_cuve_fermentation = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=1)
	volume_starter = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=1,default=0)
	nombre_bouteilles = models.IntegerField(blank=True,null=True)
	temps_empatage = models.TimeField(blank=True,null=True,default="01:15:00")
	temps_ebullition = models.TimeField(blank=True,null=True,default="01:30:00")
	temps_fermentation = models.TimeField(blank=True,null=True)
	notes = models.TextField(blank=True,null=True)
	ingredient = models.ManyToManyField(ingredient, through='brassin_ingredient',null=True,blank=True)
	recette = models.ForeignKey(recette, on_delete=models.SET_NULL, null=True,blank=True)
	temperature_brassage = models.DecimalField(blank=True,null=True, max_digits=3, decimal_places=1)
	resucrage = models.DecimalField(blank=True,null=True, max_digits=2, decimal_places=1)

	class Meta:
		verbose_name = "Brassin"
		ordering = ['-date_brassin']

	def __str__(self):
	    if not self.recette:
	        return "Sans recette (" + str(self.date_brassin) + ")"
	    return str(self.recette.nom) + " (" + str(self.date_brassin) + ")"

	@property
	def densite_initialeP(self):
		if not self.densite_initiale:
			return
		return ((Decimal(258.6)*(self.densite_initiale-1))/(Decimal(0.88)*self.densite_initiale+Decimal(0.12)));


	@property
	def densite_finaleP(self):
		if not self.densite_finale:
			return
		return ((Decimal(258.6)*(self.densite_finale-1))/(Decimal(0.88)*self.densite_finale+Decimal(0.12)));


	@property
	def densite_avant_ebullitionP(self):
		if not self.densite_avant_ebullition:
			return
		return ((Decimal(258.6)*(self.densite_avant_ebullition-1))/(Decimal(0.88)*self.densite_avant_ebullition+Decimal(0.12)));

	@property
	def malt_kg_total(self):
		return brassin_ingredient.objects.filter(brassin=self.id).filter(ingredient__type_ingredient="Malt").aggregate(Sum('quantite')).get('quantite__sum',0.00) if brassin_ingredient else 0

	@property
	def cout_brassin(self):
		ings_achetes=brassin_ingredient.objects.filter(brassin=self.id).filter(achete=True)
		cout_brassin=0
		if ings_achetes.exists():
			for ing in ings_achetes:
			    cout_brassin += ing.ingredient.prix_kg*ing.quantite
		if not self.volume_cuve_fermentation:
			return
		return cout_brassin/self.volume_cuve_fermentation

	@property
	def attenuation(self):
		if not self.densite_initiale or not self.densite_finale:
			return
		return (self.densite_initiale-self.densite_finale)/(self.densite_initiale-1)*100

	@property
	def rendement(self):
		if not self.volume_mout or not self.densite_initiale or not self.densite_finale or not self.malt_kg_total:
			return
		return (self.volume_mout*self.densite_initiale)*(259-259/self.densite_initiale)/self.malt_kg_total

	@property
	def calories(self):
		if not self.densite_initiale or not self.densite_finale:
			return
		return (Decimal(9862.42)*self.densite_finale*(Decimal(0.1808)*self.densite_initiale+Decimal(0.8192)*self.densite_finale-Decimal(1.0004))) + (Decimal(5300.9)*self.densite_finale*(self.densite_initiale-self.densite_finale)/(Decimal(1.775)-self.densite_initiale))

	@property
	def taux_alcool(self):
		if not self.densite_initiale or not self.densite_finale:
			return
		return (self.densite_initiale-self.densite_finale)*Decimal(133.333)

	@property
	def bouteilles_vendues(self):
		ventes_sum = vente.objects.filter(brassin=self.id).aggregate(Sum('quantite')).get('quantite__sum',0.00) if achat else 0.00
		return ventes_sum

	@property
	def IBU(self):
		Houblons_brassin=brassin_ingredient.objects.filter(brassin=self).filter(ingredient__type_ingredient="Houblon")
		IBU=0
		utilisation=0
		cdensite=0
		if Houblons_brassin.exists() and self.densite_initiale:
			for houblon in Houblons_brassin:
				t=str(houblon.temps_infusion).split(':')
				t_min= int(t[0])*60+int(t[1])*1 +int(t[2])/60
				if t_min:
				    utilisation=Decimal(1.65)*Decimal(0.000125)**(self.densite_initiale-Decimal(1.00))*(Decimal(1.0)-Decimal(exp(Decimal(-0.04)*Decimal(t_min))))/Decimal(4.15)
				else:
				    utilisation= 0
				if self.densite_initiale>1.05:
					cdensite= 1+(self.densite_initiale-Decimal(1.05))/Decimal(0.2)
				else: cdensite=1
				IBU += houblon.quantite*1000*utilisation*houblon.ingredient.acide_alpha*10/(Decimal(self.volume_mout)*cdensite)
		return IBU

	@property
	def EBC(self):
		Malts_brassin =brassin_ingredient.objects.filter(brassin=self.id).filter(ingredient__type_ingredient="Malt")
		MCU =0
		if Malts_brassin.exists() and self.volume_mout and self.volume_mout != 0:
			    for malt in Malts_brassin:
				    MCU += Decimal(4.23)*malt.quantite*malt.ingredient.ebc/self.volume_mout
		return Decimal(2.939)*MCU**Decimal(0.6859)


class brassin_ingredient(models.Model):
	brassin = models.ForeignKey(brassin, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(ingredient, on_delete=models.CASCADE)
	quantite = models.DecimalField(null=True,max_digits=8,decimal_places=4)
	temps_infusion = models.TimeField(blank=True,null=True,default="01:30:00")
	achete = models.BooleanField(default=True)

class recette_ingredient(models.Model):
	recette = models.ForeignKey(recette, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(ingredient, on_delete=models.CASCADE)
	quantite = models.DecimalField(null=True,max_digits=8,decimal_places=4)
	temps_infusion = models.TimeField(blank=True,null=True,default="01:30:00")

class achat(models.Model):
    ACHAT_TYPE = [('Fonctionnement','Fonctionnement'),('MAJ','MAJ'),]
    type_achat = models.CharField(null=True,max_length=30,choices=ACHAT_TYPE,default='Fonctionnement')
    date_achat = models.DateField(null=True)
    ingredient = models.ForeignKey(ingredient, on_delete=models.SET_NULL,null=True)
    quantite = models.DecimalField(null=True,max_digits=6,decimal_places=3)

    class Meta:
        verbose_name = "Achat"
        ordering = ['date_achat']

    @property
    def prix(self):
        if self.type_achat == 'MAJ':
            return 0
        else:
            ing = self.ingredient
            return ing.prix_kg*self.quantite

    @property
    def total(self):
        total = 0
        achats = achat.objects.all()
        for a in achats:
            ing = a.ingredient
            total += ing.prix_kg*a.quantite
        return total

    @property
    def unite(self):
        if self.type_ingredient=="Malt":
            return "%"
        else:
            return "g/L"


class vente(models.Model):
	date_vente = models.DateField(default=datetime.now,null=True)
	brassin = models.ForeignKey(brassin, on_delete=models.SET_NULL,null=True)
	quantite = models.PositiveIntegerField()
	client = models.CharField(null=True, blank= True,max_length=30)
	vendeur = models.CharField(null=True, blank= True,max_length=30)
	prix = models.DecimalField(null=True, blank= True,max_digits=6,decimal_places=2)
	virement = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Vente"
		ordering = ['date_vente']
