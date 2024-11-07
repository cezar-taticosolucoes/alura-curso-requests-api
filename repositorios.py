import requests
import pandas as pd
import os
import base64


class Repositorios:

    def __init__(self, username):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.token = os.getenv("TOKEN_API_GITHUB")
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'X-GitHub-Api-Version':'2022-11-28'}
        
    def cria_repo(self, nome_repo):
        data = {
            'name': nome_repo,
            'description': 'Repositório com as linguagens de programação de algumas empresas',
            'private': False,
            'auto_init': True  # Inicializa com um README.md
        }

        response = requests.post(f'{self.api_base_url}/user/repos', json=data, headers=self.headers)
        
        print(f'status_code criação do repositório: {response.status_code}')
        print(response.text)  # Exibe o corpo da resposta com detalhes sobre o erro

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):

        # Codificando arquivo
        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        # Realizando upload
        url_put = f'{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}'
        data = {
            'message': 'Upload dados csv',
            'content': encoded_content
        }

        response = requests.put(url_put, json=data, headers=self.headers)

        print(f'status_code criação do repositório: {response.status_code}')
        print(response.text)  # Exibe o corpo da resposta com detalhes sobre o erro


# Instanciando objeto
novo_repositorio = Repositorios('cezar-taticosolucoes')

# Criando o repositório
nome_repo = 'linguagens-repositorios-empresas'
novo_repositorio.cria_repo(nome_repo)
print('Repositório criado com sucesso!')

# Upload dos arquivos
novo_repositorio.add_arquivo(nome_repo, 'github_amazon.csv', 'data/github_amazon.csv')
novo_repositorio.add_arquivo(nome_repo, 'github_netflix.csv', 'data/github_netflix.csv')
novo_repositorio.add_arquivo(nome_repo, 'github_spotify.csv', 'data/github_spotify.csv')
print('Arquivos enviados com sucesso!')