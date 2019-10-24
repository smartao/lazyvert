#!/usr/bin/python3
import urllib.request
import urllib.parse
import re
import os.path

arq_gmail = "gmail_mensagens.txt"


def youtube_search():
    print('\n### Iniciando youtube_search.py ###\n')
    urls = []  # Lista para armazenar os URLs dos videos

    if os.path.exists(arq_gmail):
        with open(arq_gmail) as arquivo:
            for registro in arquivo:
                # print('\n{}'.format(registro.rstrip()))  # Teste impresssao

                # Preparando a query para a pesquisa
                query_string = urllib.parse.urlencode(
                    {"search_query": registro.rstrip()})

                # Fazendo a pesquisa no youtube e pegando o resultado
                html_content = urllib.request.urlopen(
                    "http://www.youtube.com/results?" + query_string)

                # Pegando o identificador de 11 caracteres do youtube
                search_results = re.findall(
                    r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                # Imprimindo o resultado na tela
                # print("http://www.youtube.com/watch?v=" + search_results[0])

                # Anexando a lista os resultando da pesquisa
                urls.append("http://www.youtube.com/watch?v=" +
                            search_results[0])

        # Gravando os resultados em um arquivo texto
        with open('youtube_urls.txt', 'w') as saida:
            for url in urls:
                saida.write('{}\n'.format(url))

        print('Videos processados com sucesso')

    else:
        print('Warning! Nao encontrando o arquivo {}!!!'.format(arq_gmail))


if __name__ == '__main__':
    youtube_search()
