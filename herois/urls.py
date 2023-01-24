from django.urls import path
from .views import (    cadastro_user, login_user, logout_user, tabela_equipe, time_herois,
                        HomeList, HeroisDetail, 
  )

app_name = 'herois'
urlpatterns = [
    path('', HomeList.as_view(), name='home'),
    path('detalhes/<int:pk>', HeroisDetail.as_view(), name='detalhes'),
    
    # urls tabela equipe   
    path('equipe/', tabela_equipe, name='equipe_herois'),
    path('equipe/herois', time_herois, name='time_herois'),
    
    # Urls de Login e Register
    path('login/', login_user, name="login"),
    path('login/cadastro/', cadastro_user, name="cadastro"),
    path('sair/', logout_user, name="sair"),


]