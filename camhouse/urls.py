
from django.urls import path
from . import views

app_name = 'camer_house'


urlpatterns = [
    path('home_ch', views.home_ch, name = 'home_ch'),
    path('liste_category/<int:category>/',views.liste_category, name = 'liste_category'),
    path('sugestion/',views.sugestion, name = 'sugestion'),
    path('message/',views.globaltchat, name = 'message'),
    path('',views.liste_category_un, name = 'liste_category_un'),
    path('detail_category/<int:id>/', views.detail_category, name = 'detail_category'),
    path('dupliquer_cam/<int:id>/', views.dupliquer_cam, name = 'dupliquer_cam'),
    path('supprimer_cam/<int:id>/', views.supprimer_cam, name = 'supprimer_cam'),
    path('supprimer_Reserv_cam/<int:id>/', views.supprimer_Reserv_cam, name = 'supprimer_Reserv_cam'),
    path('supprimer_Reserv_univ/<int:id>/', views.supprimer_Reserv_univ, name = 'supprimer_Reserv_univ'),
    path('Confirmer_Reservation_univ/<int:id>/', views.confirmer_Reserv_univ, name = 'Confirmer_Reservation_univ'),
    path('Confirmer_Reservation_cam/<int:id>/', views.confirmer_Reserv_cam, name = 'Confirmer_Reservation_cam'),
    path('supprimer_com/<int:id>/', views.supprimer_com, name = 'supprimer_com'),
    path('proprieter_ch', views.proprieter, name = 'proprieter_ch'),
    path('search_ch', views.search, name = 'search_ch'),
    path('donnee/', views.don, name = 'donnee'),
    path('CAD/', views.CAD, name = 'CAD'),
    path('notif/', views.notification, name = 'notif'),
    path('consultation/', views.consultation, name = 'consultation'),
    path('location/', views.locataire, name = 'location'),
    path('location_univ/', views.locataireUniv, name = 'location_univ'),
    path('rapid_search_ch', views.rapid_search, name = 'rapid_search_ch'),
    path('enregistrement_ch', views.enregistrement, name = 'enregistrement_ch'),
    path('enregistrement2_ch', views.enregistrement2, name = 'enregistrement2_ch'),
    path('enregistrement22_ch/<int:id>/', views.enregistrement22, name = 'enregistrement22_ch'),
    path('enregistrement3_ch', views.enregistrement3, name = 'enregistrement3_ch'),
    path('Apicategory/', views.allCategori),
    path('Apicategory/<int:id>/', views.ListeCategori),
    path('ApiInfrastructure/<int:id>/', views.DetailInfrastructure),
    path('ApidetailCh/<int:id>/', views.DetailHouseCh),
    path('ApidetailCc/<int:id>/', views.DetailHouseCc),
    path('ApidetailS/<int:id>/', views.DetailHouseS),
    path('ApidetailD/<int:id>/', views.DetailHouseD),
    path('Apihouse/<int:id>/', views.Maison),
    path('LoginUser/<username>/<password>', views.connexion),
]
