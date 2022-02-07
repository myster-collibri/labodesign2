from django import forms
from labocore.models import Vetements,Composants,VetementsImage,ComposantDesign,ComposantDesignImage,CaoModelImage


class AddVetements(forms.ModelForm):

	class Meta:
		model=Vetements
		fields=['nom','description','sexe']
		widgets={
			'nom': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 2,'id':"niveau-name",}),
			'sexe': forms.Select(attrs={'class':'form-select form-control-sm','cols': 80, 'rows': 10,'id':"niveau-name"}),
			'description': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 10,'id':"niveau-name"}),
		}


class AddComposants(forms.ModelForm):

	class Meta:
		model=Composants
		fields=['nom','details']
		widgets={
			'nom': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 2,'id':"niveau-name",}),
			'details': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 10,'id':"niveau-name"}),
		}

class AddImageVet(forms.ModelForm):

	class Meta:
		model=VetementsImage
		fields=['image',]
		widgets={
			
		}


class AddImageDesign(forms.ModelForm):

	class Meta:
		model=ComposantDesignImage
		fields=['image',]
		widgets={
			
		}

class AddTopModelImage(forms.ModelForm):

	class Meta:
		model=CaoModelImage
		fields=['image',]
		widgets={
			
		}


class AddCompDesign(forms.ModelForm):

	class Meta:
		model=ComposantDesign
		fields=['details',]
		widgets={
			'details': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 10,'id':"niveau-name"}),
		}
