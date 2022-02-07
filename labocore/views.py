from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.views import View
from labocore.fonctions import *
from labocore.forms import AddVetements,AddComposants,AddImageVet,AddCompDesign,ComposantDesign,AddImageDesign,AddTopModelImage
from labocore.models import Vetements
from django.contrib.auth.models import User
import time

# Create your views here.

class IndexView(LoginRequiredMixin, View):
	sex=''
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				return render(request, 'index.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request):
		if request.method == "POST":
			try:
				if request.session['username']:
					sex=request.POST.get('sexe')
					request.session['sex_tmp']=sex.lower()
					if sex == "Feminin":
						return redirect("home_fem")
					elif sex == "Masculin":
						return redirect("home_masc")
					elif sex == "Tous":
						return redirect("toutgenre")

				else:
					return redirect('login')
			except:
				return redirect('login')
		return redirect('home')

class SceneView(LoginRequiredMixin, View):
	sex=''
	def get(self, request,coa_id):
		try:
			if request.session['username']:
				data={}
				data['header_cao']=get_header_cao(coa_id)#topmodel et titre vetetment
				data['topmodel_image_form']=AddTopModelImage
				data['composant_list']=get_composants_caoList(coa_id)#[{'name':'col', "images":['url1',url2]}, ]
				return render(request, 'scene.html', data)
			else:

				return redirect('login')
		except Exception as exc:
			print(exc)
			return redirect('login')

	def post(self,request,coa_id):
		if request.method == "POST":
			try:
				if request.session['username']:
					form=AddTopModelImage(request.POST or None, request.FILES or None)

					if form.is_valid():
						mdl=form.save(commit=False)
						mdl.save()
						set_cao_model(mdl.image.url, coa_id)


						return redirect('scene', coa_id)

				else:
					return redirect('login')
			except Exception as exc:
				print(exc)
				return redirect('login')
			return redirect('home')

class CAOConfigView(LoginRequiredMixin, View):
	sex=''
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				data['vetements']=get_vetements_tous()
				return render(request, 'configcao.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request):
		if request.method == "POST":
			data={}
			try:
				if request.session['username']:
					if(request.POST.get('is_ceo_get_info')):
						vetement=request.POST.get('vetement')

						data['success']=True
						data['success_message']="success"
						data['vetement']=get_cao_vetement(vetement) 
						data['composants']=get_composants_cao(vetement)
						data['has_composant']=True if len(data['composants'])>0 else False
						return JsonResponse(data, safe=False)
					elif(request.POST.get('is_validate_cao')):
						vetement=request.POST.get('vetement')
						sexe=request.POST.get('sexe')
						#creation de la conception
						res=create_conception_instance(vetement,sexe, request.session['username'])
						data['cao_id']=res
						data['success']=True
						data['success_message']="success"
						return JsonResponse(data, safe=False)

					else:
						data['error_message']="Quelque chose s'est mal passer! reessayer svp"
						return JsonResponse(data, safe=False)

				else:
					return redirect('login')
			except:
				return redirect('login')
		return redirect('home')

class ComposantView(LoginRequiredMixin, View):
	sex=''
	def get(self, request, id_cmps):
		try:
			if request.session['username']:
				data={}
				cmps=get_composants_details(id_cmps)
				data['id_cmps']=id_cmps
				data['vetement']=cmps.vetement.nom.capitalize()
				data['composant']=cmps.nom.lower()
				data['details']=cmps.details
				data['design']=get_design_liste(cmps)
				data['composants']=get_composants(cmps.vetement)
				data['has_modele']=True if len(data['design']) > 0 else False
				return render(request, 'composants.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request, id_cmps):
		if request.method == "POST":
			try:
				if request.session['username']:
					pass
			except:
				return redirect('login')
		return redirect('home')

class AddVtmView(LoginRequiredMixin, View):
	sex=''
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				data['form']=AddVetements
				return render(request, 'addvtm.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request):
		if request.method == "POST":
			try:
				if request.session['username']:
					user=User.objects.get(username=request.session['username'])
					form=AddVetements(request.POST or None, request.FILES or None)

					if form.is_valid():
						mdl=form.save(commit=False)
						nom=mdl.nom.upper()
						mdl.nom=nom
						sex=request.session['sex_tmp']
						#teste si ce vetements existe pas encore
						try:
							vtm=Vetements.objects.filter(nom=nom).filter(sexe=mdl.sexe.lower())
						except:
							if sex == mdl.sexe.lower():
								mdl.auteur=user
								mdl.save()
						
						
						if sex == "feminin":
							return redirect("home_fem")
						elif sex == "masculin":
							return redirect("home_masc")
						else:
							return redirect("toutgenre")
						return redirect('home')
			except Exception as exc:
				print(exc)
				return redirect('login')
		return redirect('home')

class AddCmpView(LoginRequiredMixin, View):
	sex=''
	def get(self, request,id_vet):
		try:
			if request.session['username']:
				data={}
				vet=Vetements.objects.get(id=id_vet)
				data['form']=AddComposants
				data['id_vet']=id_vet
				data['vetement']=vet.nom.lower()
				return render(request, 'addcmp.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request,id_vet):
		if request.method == "POST":
			try:
				if request.session['username']:
					user=User.objects.get(username=request.session['username'])
					vetement=Vetements.objects.get(id=id_vet)
					form=AddComposants(request.POST or None, request.FILES or None)
					if form.is_valid():
						mode_ins=form.save(commit=False)
						mode_ins.auteur=user
						mode_ins.vetement=vetement
						mode_ins.save()
						return redirect('vetement', id_vet=id_vet)
			except:
				return redirect('login')
		return redirect('home')

class AddImageVetView(LoginRequiredMixin, View):
	sex=''
	def get(self, request,id_vet):
		try:
			if request.session['username']:
				data={}
				vet=Vetements.objects.get(id=id_vet)
				data['form']=AddImageVet
				data['id_vet']=id_vet
				data['vetement']=vet.nom.lower()
				return render(request, 'addimgvet.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request,id_vet):
		if request.method == "POST":
			try:
				if request.session['username']:
					vetement=Vetements.objects.get(id=id_vet)
					form=AddImageVet(request.POST or None, request.FILES or None)
					if form.is_valid():
						print("valide form")
						mode_ins=form.save(commit=False)
						mode_ins.vetement=vetement
						mode_ins.save()
						return redirect('vetement', id_vet=id_vet)
					else:
						print("pas valide")
			except:
				return redirect('login')
		return redirect('home')


class AddImageDesignView(LoginRequiredMixin, View):
	sex=''
	def get(self, request,id_design):
		try:
			if request.session['username']:
				data={}
				dsn=ComposantDesign.objects.get(id=id_design)
				data['form']=AddImageDesign
				data['id_cmp']=dsn.composant.id
				data['id_design']=id_design
				data['design']=dsn.composant.nom
				return render(request, 'addimdesign.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request,id_design):
		try:
			if request.method == "POST":
				if request.session['username']:
					dsn=ComposantDesign.objects.get(id=id_design)
					form=AddImageDesign(request.POST or None, request.FILES or None)
					if form.is_valid():
						mode_ins=form.save(commit=False)
						mode_ins.composant_design=dsn
						mode_ins.save()
						return redirect('composants', id_cmps=dsn.composant.id)
					else:
						pass
			return redirect('home')
		except:
			return redirect('login')


class AddDesignView(LoginRequiredMixin, View):
	sex=''
	def get(self, request,id_cmp):
		try:
			if request.session['username']:
				data={}
				cmpp=Composants.objects.get(id=id_cmp)
				data['form']=AddCompDesign
				data['id_cmp']=id_cmp
				data['nom']=cmpp.nom.lower()
				data['vetement']=cmpp.vetement.nom.lower()
				return render(request, 'adddesign.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')

	def post(self,request,id_cmp):
		if request.method == "POST":
			try:
				if request.session['username']:
					cmpp=Composants.objects.get(id=id_cmp)
					form=AddCompDesign(request.POST or None, request.FILES or None)
					if form.is_valid():
						mode_ins=form.save(commit=False)
						mode_ins.composant=cmpp
						mode_ins.save()
						return redirect('composants', id_cmps=id_cmp)
					else:
						print("pas valide")
			except:
				return redirect('login')

		return redirect('home')

class VetementsView(LoginRequiredMixin, View):
	sex=''
	def get(self, request, id_vet):
		try:
			if request.session['username']:
				data={}
				vet=get_vetement_details(id_vet)
				data['nom']=vet.nom.lower()
				data['details']=vet.description
				data['id_vet']=vet.id
				data['images']=image_vetements(vet)
				data['composants']=get_composants(vet)
				if len(data['images']) >0:
					data['image_bannere']=data['images'][0]
					data['has_image']=True

				else:
					data['has_image']=False
				return render(request, 'vetements.html', data)
			else:
				return redirect('login')
		except Exception as exc:
			print(exc)
			return redirect('login')

	def post(self,request, id_vet):
		if request.method == "POST":
			try:
				if request.session['username']:
					pass
			except:
				return redirect('login')
		return redirect('home')


class ImageView(LoginRequiredMixin, View):
	sex=''
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				return render(request, 'galleri.html', data)
			else:
				return redirect('login')
		except:
			return redirect('login')


	def post(self,request):
		if request.method == "POST":
			try:
				if request.session['username']:
					pass
			except:
				return redirect('login')
		return redirect('home')


class HomeFemView(LoginRequiredMixin,View):
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				data['vetements']=get_vetements_fem(request.session['username'])
				data['mes_conceptios']=get_all_conceptions_from_auteur(request.session['username'])
				return render(request, 'home_f.html', data)
		except Exception as exc:
			print(exc)
			return redirect('login')

	def post(self,request):
		pass

class HomMascView(LoginRequiredMixin,View):
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				data['vetements']=get_vetements_masc()
				data['mes_conceptios']=get_all_conceptions_from_auteur(request.session['username'])
				return render(request, 'home_m.html', data)
		except:
			return redirect('login')

	def post(self,request):
		pass

class HomeToutView(LoginRequiredMixin,View):
	def get(self, request):
		try:
			if request.session['username']:
				data={}
				data['vetements']=get_vetements_tous()
				data['mes_conceptios']=get_all_conceptions_from_auteur(request.session['username'])
				return render(request, 'home_tout.html', data)
		except:
			return redirect('login')

	def post(self,request):
		pass

class LoginView(View):
	username = [];
	def get(self,request):
		greeting={}
		try:
			if 'username' in request.session:
				return redirect('home')
			else:
				#greeting['form'] = UserLoginForm
				return render(request,'login.html',greeting)
		except:
			return redirect('login')

	def post(self,request):
		data={}
		if(request.method == "POST"):
			try:
				username = request.POST.get('username')
				username=username.strip()
				password = request.POST.get('password')
				user_log=auth.authenticate(username=username, password=password)
				if user_log is not None:
					request.session['username']=username
					auth.login(request, user_log)
					#request.session.set_expiry(300)
					LoginView.username.append(username)
					data['success']=True
					data['success_message']="Vous etes connecté!"
				else:
					data['error_message']="Mot de passe incorrecte!"
			except Exception as exc:
				print(exc)
				data['error_message']="Quelque chose s'est mal passer! reessayer svp"
			return JsonResponse(data, safe=False)
		else:
			return redirect('login')


class InscriptionView(View):
	username = [];
	def get(self,request):
		greeting={}
		try:
			if 'username' in request.session:
				return redirect('home')
			else:
				#greeting['form'] = UserLoginForm
				return render(request,'inscription.html',greeting)
		except:
			return redirect('login')

	def post(self,request):
		data={}
		if(request.method == "POST"):
			try:
				username = request.POST.get('username')
				username=username.strip()
				password = request.POST.get('password')
				mail=request.POST.get('mail')
				print(password)
				try:
					user = User.objects.create_user(username, mail, password)
					data['success']=True
					data['success_message']="Compte creer avec success, vous pouvez maintenant vous connecté"
				except:
					data['error_message']="Ce nom d'utilisateur existe deja, choisi un autre, ou melange le avec des chiffres."
				#else:
					#data['error_message']="Mot de passe incorrecte!"
			except Exception as exc:
				print(exc)
				data['error_message']="Quelque chose s'est mal passer! reessayer svp"
			return JsonResponse(data, safe=False)
		else:
			return redirect('login')

# Logout
def logout(request):
    auth.logout(request)
    return redirect('login')