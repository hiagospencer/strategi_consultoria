from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import HeroiMarvel, EquipeHeroi

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ================ FUNCÕE DE LOGIN E REGISTER ====================
def login_user(request):
    if request.method == 'GET':
        return render(request, 'autenticacao/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/')

        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'autenticacao/login.html')

    


def cadastro_user(request):
    if request.method == 'GET':
        return render(request, 'autenticacao/register.html')
    else:
        # pegando as informações dos inputs
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf-password')

        # Verificando se a senha e confirmação de senha são iguais
        if password != conf_password:
            messages.error(request, 'Senha e confirmação de  senha diferentes')
            return render(request, 'autenticacao/register.html')

        # Verificando se o tamanho da senha é maior que 8
        elif len(password) < 8:
            messages.error(request, 'A senha contém menos de 8 caracteres')
            return render(request, 'autenticacao/register.html')

        # Verificando se existe usuario com o mesmo nome no banco de dados
        user = User.objects.filter(username=username).first()
        if user:            
            messages.error(request, f'Já existe usuário com o nome "{username}" cadastrado')
            return render(request, 'autenticacao/register.html')

        email_user = User.objects.filter(email=email)
        if email_user:
            messages.error(request,f'Já existe um email cadastrado com {email}')
            return render(request, 'autenticacao/register.html')

        # Salvando usuário no banco de dados 
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            
    return render(request, 'autenticacao/register.html')



def logout_user(request):
    logout(request)
    return redirect('/')
   


# ==================== Função Equipe ============================

@login_required(login_url='/login/')
def tabela_equipe(request):

    #Essa views ela faz a integração com a seleção da equipe do diretor.

    context = {}
    heroi_id = request.POST.get('heroi_id') # instanciando o ID do personagem na pagina de detalhes.
    
    if heroi_id is not None:
        '''
            Esse if, pega o nome a descrição do personagem, e atribui ao usuário logado.
        '''
        heroi_obj = HeroiMarvel.objects.get(id=heroi_id)
        usuario = request.user
        nome_heroi = heroi_obj
        descricao_heroi = heroi_obj.descricao
       
        # Verificando se o o personagem selecionado já existe no bando de Dados, e retornando uma mensagem de erro.
        lista_equipe = EquipeHeroi.objects.filter(nome=nome_heroi)
        if lista_equipe:
            messages.error(request,f'{nome_heroi} já adicionado a equipe')
            return redirect('herois:home')
                 
        # Adicionando o nome, descrição, e o usuario logado para fazer as integrações com os personagens no admin.
        equipe_herois = EquipeHeroi.objects.create(user=usuario, nome=nome_heroi, descricao=descricao_heroi)  
        lista_equipe = EquipeHeroi.objects.filter(user=usuario)  # Filtrando somente os personagens selecionado pelo o usuário logado, e retornando no context.
        context['equipe'] = lista_equipe 
        
    return render(request,'equipe.html', context)


@login_required(login_url='/login/')
def time_herois(request):
    context = {}
    usuario = request.user
    lista_equipe = EquipeHeroi.objects.filter(user=usuario)
    context['time_herois'] = lista_equipe

    return render(request, 'time_herois.html', context)

# ============================ CLASS =============================


class HomeList(ListView):
    queryset = HeroiMarvel.objects.all()
    model = HeroiMarvel
    paginate_by = 20
    template_name = 'home.html'

    def get_queryset(self):
        '''
            Fazendo a função de busca de pesquisa
        '''
        txt_nome = self.request.GET.get('nome')

        if txt_nome:
            heroi_pesquisa = HeroiMarvel.objects.filter(nome__icontains=txt_nome)
        else:
            heroi_pesquisa = HeroiMarvel.objects.all()

        return heroi_pesquisa


class HeroisDetail(DetailView):
    template_name = 'detalhes.html'
    model = HeroiMarvel


