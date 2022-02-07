from labocore.models import Vetements
from labocore.models import VetementsImage
from labocore.models import Composants
from labocore.models import ComposantDesign
from labocore.models import ComposantDesignImage
from django.contrib.auth.models import User
from labocore.models import CaoModelImage
from labocore.models import Cao
from labocore.models import CaoComposant
from labocore.models import CaoImageComposant
import cv2
import numpy as np
import random
import os
from django.conf import settings


def get_vetements_fem(user):
	"""Retourne la listes de vetements dans la base de donnees"""
	#les vetements qu e
	user=User.objects.get(username=user)#getting proprietaire
	#getting her vetements
	try:
		vtm=Vetements.objects.filter(auteur=user).filter(sexe='feminin').order_by('id').reverse()
		if len(vtm)>0:
			return vtm
		else:
			return []
	except:
		return []

def get_vetements_masc():
	"""Retourne la listes de vetements dans la base de donnees"""
	try:
		vtm=Vetements.objects.filter(sexe='masculin')
		if len(vtm)>0:
			return vtm
		else:
			return []
	except:
		return []

def get_vetements_tous():
	"""Retourne la listes de vetements dans la base de donnees"""
	try:
		vtm=Vetements.objects.all()
		if len(vtm)>0:
			return vtm
		else:
			return []
	except:
		return []


def get_vetement_details(id_vet):
	"""recupere tout les details sur ce vetements"""
	try:
		vtm=Vetements.objects.get(id=id_vet)
		if vtm:
			return vtm
		else:
			return []
	except:
		return []

def image_vetements(vtm):
	"""recuper les image attacher a ce vetement"""
	try:
		image=VetementsImage.objects.filter(vetement=vtm)
		print(image)
		if len(image) > 0:
			return image
		else:
			return []
	except:
		return []

def get_composants(vet):
	"""Recupere tout les composant de ce vetements"""
	try:
		cmps=Composants.objects.filter(vetement=vet)
		if len(cmps)>0:
			return cmps
		else:
			return []
	except:
		return []
def get_composants_details(id_cmps):
	"""Recupere les details de ce composants"""
	try:
		cmps=Composants.objects.get(id=id_cmps)
		if cmps:
			return cmps
		else:
			return []
	except:
		return []

def get_design_liste(cmps):
	try:
		cmpss=ComposantDesign.objects.filter(composant=cmps).order_by('id').reverse()
		data_retour=[]
		for design in cmpss:
			image=ComposantDesignImage.objects.filter(composant_design=design)
			if len(image)>0:
				has_image=True
				illustration=image[0]
			else:
				has_image=False
				illustration=''
			data_retour.append({
				"composant":design.composant.nom,
				"date":design.date,
				"images":image,
				"ullistration":illustration,
				"has_image":has_image,
				"details":design.details,
				"id_design":design.id
				})
		return data_retour
	except:
		return []


def get_cao_vetement(vetement):
	vetement, sexe=vetement.split(":")
	vetement=vetement.strip()
	sexe=sexe.strip()

	try:
		vet=Vetements.objects.filter(nom=vetement).filter(sexe=sexe)[0]
		return {
			"vetement":vet.nom.capitalize(),
			"sex":vet.sexe
		}
	except Exception as exc:
		print(exc)
		return []

def get_composants_cao(vetement):
	vetement, sexe=vetement.split(":")
	vetement=vetement.strip()
	sexe=sexe.strip()
	data_retour=[]
	try:
		vet=Vetements.objects.filter(nom=vetement).filter(sexe=sexe)[0]
		composants=Composants.objects.filter(vetement=vet)

		for comp in composants:
			data_retour.append({
				"nom":comp.nom,
				"id":comp.id,
				"has_composant":True if len(composants)>0 else False
				})
		return data_retour
	except Exception as exc:
		print(exc)
		return []


def remove_background(imggg):
	try:
		#load image
		imggg="."+imggg
		
		img=cv2.imread(imggg)
		#conver to gray
		gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#threshold input image as mask
		mask=cv2.threshold(gray,250,255, cv2.THRESH_BINARY)[1]
		#negate the mask
		mask=255-mask
		#apply morphologie to remove isolated extraneaousnoise
		#use borderconstant of black since foreground touches the edges
		kernel=np.ones((3,3), np.uint8)
		mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		#anti-alias the mask -- blur then strecth
		#blur alpha channel
		mask=cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)
		#linear stretch so that 127.5 goes to 0 , but 255 stay 255
		mask=(2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)
		#put mask to alpha channel
		result=img.copy()
		result=cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
		result[:,:,3]=mask

		#save resulting masked image
		if "/" in imggg:
			im_name=os.path.dirname(imggg)+"/"+str(random.randint(0,1000000))+".png"
		else:
			im_name=os.path.dirname(imggg)+"\\"+str(random.randint(0,1000000))+".png"
		cv2.imwrite(im_name, result)
		
		return im_name[1:]

	except Exception as exc:
		print(exc)
		return imggg

def create_conception_instance(vetement,sexe,auteur):
	vetement=vetement.upper().strip()
	sexe=sexe.lower().strip()
	auteur=auteur.strip()
	c=Cao(vetement=vetement, sexe=sexe, auteur=auteur, top_model="---")
	c.save()
	#save composant
	vtm=Vetements.objects.filter(nom=vetement).filter(sexe=sexe)[0]
	compp=Composants.objects.filter(vetement=vtm)
	cao_composantsLis=[]
	for cmpp in compp:
		try:
			#recuperer les design de ce composant
			tmp_cmp=Composants.objects.get(id=cmpp.id)

			cmpdesignlist=ComposantDesign.objects.filter(composant=tmp_cmp)
			#pour chaque design, extraction de ses images
			for cmdesign in cmpdesignlist:
				try:
					imageliste=ComposantDesignImage.objects.filter(composant_design=cmdesign)
					image_url=[]
					for img in imageliste:
						image_url.append(img.image.url)
					cao_composantsLis.append({
						"composant_name":cmpp.nom,
						"imageliste":image_url
						})
				except Exception as exc:
					print(exc)
					return 2
		except Exception as exc:
			print(exc)
			return 1
		
		caocomp=CaoComposant(cao=c, nom=cmpp.nom)
		caocomp.save()
		for cmppp in cao_composantsLis:
			for imggg in cmppp['imageliste']:
				image_transparent=remove_background(imggg)
				ckey=CaoImageComposant(caocomposant=caocomp, image_url=image_transparent)
				ckey.save()
	return c.id



def get_header_cao(cao_id):
	try:
		c=Cao.objects.get(id=cao_id)
		print("image model", c.top_model)
		return {
		"vetement":c.vetement.lower(),
		"top_model":c.top_model,
		"sexe":c.sexe,
		"cao_id":cao_id,
		"has_topmodel":True if c.top_model != "---" else False
		}
	except:
		return {}

def set_cao_model(url, coa_id):
	c=Cao.objects.get(id=coa_id)
	c.top_model=url
	c.save()


def get_composants_caoList(coa_id):#[{'name':'col', "images":['url1',url2]}, ]
	c=Cao.objects.get(id=coa_id)
	data_retour=[]
	composants=CaoComposant.objects.filter(cao=c)
	print(len(composants))
	for comp in composants:
		images=CaoImageComposant.objects.filter(caocomposant=comp)
		imageliste=[]
		for img in images:
			imageliste.append(img.image_url)
		data_retour.append({
			"mom_compo":comp.nom,
			"images":imageliste
			})

	return data_retour


def get_all_conceptions_from_auteur(auteur):
	auteur=auteur.strip()
	c=Cao.objects.filter(auteur=auteur)
	if len(c)>0:
		return c
	else:
		return []

