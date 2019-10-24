#!/usr/bin/python3
import requests
import json
import errno
import sys


apigoogle = 'https://www.googleapis.com/youtube/v3/videos'
youtube_url = 'https://www.youtube.com/watch?v='
tipo = 'snippet,contentDetails'  # relacionado ao retono em json da api

# Localizacao do arquivo que contem a chave API para requisicoes no youtube
keyfile = 'lazyvert.key'
videosfile = 'youtube_urls.txt'


def validaarquivo(file):
    try:
        openfile = open(file)
        return openfile
    except Exception:
        print(f'\narquivo: {file} nao encontrado!\n')
        sys.exit(errno.ENOENT)


def lazyvert():
    print('\n### Iniciando lazyvert.py ###\n')
    keytemp = validaarquivo(keyfile)  # Validando e lendo o arquivo
    key = keytemp.read()  # Passando o conteudo do arquivo para a variavel

    videostemp = validaarquivo(videosfile)  # Validando e lendo o arquivo

    print('Gerando acoes no padrao Todoist:')
    # Lendo todas as linhas do arquivo usando o loop
    with open(videostemp.name) as the_file:
        for line in the_file:
            # Removendo linha em branco do arquivo
            templine = line.rstrip()

            # Cortando para armazenar valor exato  do ID do video
            videoid = templine[31:43]

            # Carregando parametros para o payload
            payload = {'id': videoid, 'key': key.rstrip(), 'part': tipo}

            # Fazendo a requisicao para a API
            r = requests.get(apigoogle, params=payload)

            # Convertendo o retoron em json
            data = json.loads(r.text)

            # Extraindo o conteudo do formato json e armazenando
            # as informacoes do video nas variaveis, canal, titulo, duracao
            canal = data["items"][0]["snippet"]["channelTitle"]
            titulo = data["items"][0]["snippet"]["title"]
            duracao = data["items"][0]["contentDetails"]["duration"]

            # Dividindo a duracao em minutos (M) e corrigindo formatado
            # -2 pequando penultimo elemento e apenas do caractere 2 a 4
            minutos = duracao.split('M')[-2][2:4]

            # Formando a URL completa do video
            urlfull = youtube_url+videoid

            # Imprimindo na tela o formatado final para o Todoist
            print(f'{canal} `{minutos}:00` - [{titulo.title()}]({urlfull})')


if __name__ == '__main__':
    lazyvert()
