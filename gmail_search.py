#!/usr/bin/python3
# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def gmail_search():
    print('### Iniciando gmail_search.py ###\n')
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    # SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

    '''
    gmail_token.json
        Gerando quando o gmail_search é autenticado, caso nao exista,
        sera gerado um arquivo de autenticado
    gmail_credentials.json
        Chave de acesso para o gmail, foi gerado no painel do google,
        se naoo existir o programa nao funciona

    '''
    store = file.Storage('gmail_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('gmail_credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Chamando a API e fazendo a pesquisa Videos + não lidos
    results = service.users().messages().list(
        userId='me', q='in:Videos is:unread').execute()
    messages = results.get('messages', [])

    if not messages:
        print("Nenhuma menssagem encontranda.\n")
    else:
        print("Processando emails.")
        emails = []  # Lista que contera as mensagem
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()

            # Armazenando todo o conteudo email em uma string
            msgstr = msg['snippet']

            # Caso o video seja do tipo "enviou"
            if "enviou" in msgstr:
                # Pegando apenas o nome do canal
                canal = msgstr.split('enviou')[0]

                # Cortando enviou para traz para pegar titulo do video
                titulotemp = msgstr.split('enviou')[1]

                # Pegando apenas as 7 primeiras palavras do titulo
                titulonew = titulotemp.split()[0:7]

                # Formando o titulo do video
                separator = ' '
                titulo = separator.join(titulonew)

                # Criando lista com Nome do Canal + Titulo do Video
                emails.append(canal.encode('utf-8') +
                              '' + titulo.encode('utf-8'))

            # Caso o video seja do tipo "estreia"
            elif "Ao vivo" in msgstr:
                # Pegando apenas o nome do canal
                canaltemp = msgstr.split('YouTube: ')[1]
                canal = canaltemp.split('-')[0]

                # Pegando apenas o titulo do video
                titulotemp = canaltemp.split('-')[1]
                titulonew = titulotemp.split()[0:7]

                # Formando o titulo do video
                separator = ' '
                titulo = separator.join(titulonew)

                # Criando lista com Nome do Canal + Titulo do Video
                emails.append(canal.encode('utf-8') +
                              '' + titulo.encode('utf-8'))
            else:
                print('Warning! Tipo e email nao reconhecido!\n{}'.format(
                    msgstr.encode('utf-8')))

        # Armazenando o resultado em um arquivo de texto
        with open('gmail_mensagens.txt', 'w') as saida:
            for registro in emails:
                saida.write('{}\n'.format(registro))
                print('{}'.format(registro))  # Teste de impressao


if __name__ == '__main__':
    gmail_search()
