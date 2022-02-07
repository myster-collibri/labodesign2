from django.contrib import admin
from labocore.models import Vetements
from labocore.models import VetementsImage
from labocore.models import Composants
from labocore.models import ComposantDesign
from labocore.models import ComposantDesignImage
from labocore.models import CaoModelImage
from labocore.models import Cao
from labocore.models import CaoComposant
from labocore.models import CaoImageComposant

# Register your models here.
admin.site.register(Vetements)
admin.site.register(VetementsImage)
admin.site.register(Composants)
admin.site.register(ComposantDesign)
admin.site.register(ComposantDesignImage)
admin.site.register(CaoModelImage)
admin.site.register(Cao)
admin.site.register(CaoComposant)
admin.site.register(CaoImageComposant)
