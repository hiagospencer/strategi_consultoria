import dotenv
import os
import hashlib
import requests
import pandas as pd
from sqlalchemy import create_engine


dotenv.load_dotenv(dotenv.find_dotenv())

def get_hash():
    '''
        Função para fazer a integração com a API da MArvel.
        Retornando o ts, apikey( Minha chave publica) e o hash.
    '''
    ts = 1
    pvt = os.getenv('PRIVATE_KEY')
    apikey = os.getenv('PUBLIC_KEY')

    cripto = str(ts) + pvt + apikey

    hash_marvel = hashlib.md5(cripto.encode()).hexdigest()

    return ts, apikey, hash_marvel

def buscar_herois():
    '''
        Função para fazer a busca dos personagens da API da MArvel.
        Chamando a função get_hash, para passar os parâmetros necessário da API.
        O parâmetro name_starts_with, se deixar ele vazio, ele buscar os 100 primeiros personagens.
        se colocar qualquer letra, ele busca por os 100 primeiro personagens da letra selecionada.

        Função retornando o resultados da API 
    '''

    info_hash = get_hash()

    params = {
        "nameStartsWith": '', 
        "limit": 100,
        "ts": info_hash[0],
        "apikey": info_hash[1],
        "hash": info_hash[2],
    }
    resp = requests.get('https://gateway.marvel.com:443/v1/public/characters', params)
    characters = resp.json()['data']['results'] 
    return characters




def lista_herois():
    '''
    Função para criar uma lista com os resultados da API, chamando e instanciando a função buscar_herois()
    Foi definido uma lista vazia, onde foi feito um " for ", para pecorrer todos os personagens,
    e adicionando o nome, descrição e o link da imagem.

    a variável " imagem", peguei o link, concatenei com um ".", e concatenei com a extenção do link.

    Função retornando a lista com todos os nomes, descrições e links da imagens dos heróis.
    '''
    lista_herois = []
    personagem = buscar_herois()

    for heroi in personagem:
        imagem = heroi['thumbnail']['path'] + "." + heroi['thumbnail']['extension']
        lista_herois.append([heroi['name'],heroi['description'], [imagem]])

    return lista_herois


heroi = lista_herois()

# Usando a Biblioteca Pandas, eu criei um DataFrame com a lisa de heróis retornado na função
df_herois = pd.DataFrame(heroi, columns=['nome', 'descricao', 'img'])

# fazendo a integração com o banco de dados postgresql, Criando um banco de dados, com a lista de herois da DataFrame
db_connection = f"postgresql://{os.getenv('USERNAME')}:{os.getenv('SENHA')}@localhost:5432/marvel"
db_connection = create_engine(db_connection)
df_herois.to_sql(con=db_connection, name='marvel_heroi', if_exists='append', index=True)


print("Dados gravado com sucesso!")
