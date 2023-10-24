import requests
from bs4 import BeautifulSoup
import re
import discord
import discord.ext
import json
import os

def tratamento_preco(preco_string):
    preco_rege = re.sub('[^0-9]', '', preco_string)
    preco_int = int(preco_rege) / 100
    return preco_int
def mostra_item(item_list):

    for item in item_list:
        print(f"{item[0]}\nPreço atual:{item[1]} \nPreço antigo:{item[2]}\nDesconto: {round(item[2] - item[1], 2)}\n")
def salvar_produtos_antigos(lista):
    with open('produtos_antigos.json', 'w', encoding='utf8') as arquivo:
        json.dump(lista, arquivo, indent=2)
def salvar_produtos_novos(lista):
    with open('produtos_novos.json', 'w', encoding='utf8') as arquivo:
        json.dump(lista, arquivo, indent=2)
def produtos_novos():
    with open('produtos_antigos.json', 'r', encoding='utf8') as arquivo:
        itens_js_antigos = json.load(arquivo)
        lista_antigos = list(itens_js_antigos)

    with open('produtos_novos.json', 'r', encoding='utf8') as arquivo:
        itens_js2_novos = json.load(arquivo)
        lista_novos = list(itens_js2_novos)

    produtos_novos = [x for x in lista_novos if x not in lista_antigos]

    return produtos_novos
def verificar_arquivo(lista):
    if(os.path.exists('produtos_antigos.json')):
        print('Arquivo existente')
    else:
        salvar_produtos_antigos(lista)
        print('Arquivo criado')

nome_produto = []
preco_produto_list = []
preco_original_list = []

ofertas_do_dia = "https://www.magazineluiza.com.br/selecao/ofertasdodia/?page="
def scrap(pagina):
    page_number = 0
    for i in range (3):
        page_number +=1
        response = requests.get(f'{pagina}{page_number}')
        content = response.content

        site = BeautifulSoup(content, 'html.parser')

        # Localização item e preço
        iten_html = site.findAll('li', class_=re.compile('sc-APcvf'))
        title = site.findAll('h2', class_=re.compile('sc-eWzREE'))
        preco_atual_string = site.findAll('p', class_=re.compile('sc-kpDqfm eC'))
        preco_original_string = site.findAll(class_=re.compile('sc-kpDqfm ef'))

        for titulos in title:
            produto = titulos.string
            nome_produto.append(produto)

        for preco in preco_atual_string:
            preco_produto = preco.string
            preco_tratado = tratamento_preco(preco_produto)
            preco_produto_list.append(preco_tratado)

        for preco_original in preco_original_string:
            preco_original_produto = preco_original.string
            preco_original_tratado = tratamento_preco(preco_original_produto)
            preco_original_list.append(preco_original_tratado)

scrap(ofertas_do_dia)
itens = list(zip(nome_produto ,preco_produto_list ,preco_original_list))

verificar_arquivo(itens)
salvar_produtos_novos(itens)
mostra_item(produtos_novos())
salvar_produtos_antigos(itens)

