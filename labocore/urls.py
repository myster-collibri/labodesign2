#from django.contrib import admin
from django.urls import path,include
from labocore import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('model_feminin', views.HomeFemView.as_view(), name="home_fem"),
    path('home_masculin', views.HomMascView.as_view(), name="home_masc"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('composants/<int:id_cmps>', views.ComposantView.as_view(), name="composants"),
    path('vetements/<int:id_vet>', views.VetementsView.as_view(), name="vetement"),
    path('gallerie/', views.ImageView.as_view(), name="gallerie"),
    path('toutsgenre/', views.HomeToutView.as_view(), name="toutgenre"),
    path('addvtm/', views.AddVtmView.as_view(), name="addvtm"),
    path('addcmp/<int:id_vet>', views.AddCmpView.as_view(), name="addcmp"),
    path('add_image_vet/<int:id_vet>', views.AddImageVetView.as_view(), name="addimgvet"),
    path('add_design/<int:id_cmp>', views.AddDesignView.as_view(), name="adddesign"),
    path('add_design_image/<int:id_design>', views.AddImageDesignView.as_view(), name="addimgdesign"),
    path('inscription/', views.InscriptionView.as_view(), name="inscription"),
    path('cao_config/', views.CAOConfigView.as_view(), name="caoconf"),
    path('scene/<int:coa_id>', views.SceneView.as_view(), name="scene"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)