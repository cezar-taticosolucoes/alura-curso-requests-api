import requests
import pandas as pd
import os

class DadosRepositorios:

    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.token = os.getenv("TOKEN_API_GITHUB")
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'X-GitHub-Api-Version':'2022-11-28'}

    def lista_repositorios(self):
        repos_list = []

        for page_num in range(1, 20):
            try:
                url_page = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url_page, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list
    
    def nomes_repos(self, repos_list):
        repo_names = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except:
                    pass
        
        return repo_names
    
    def nomes_linguages(self, repos_list):
        repo_languagens = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_languagens.append(repo['language'])
                except:
                    pass
        
        return repo_languagens
    
    def cria_df_linguagens(self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguaggens = self.nomes_linguages(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['repository_language'] = linguaggens

        return dados

amazon_rep = DadosRepositorios('amzn')
df_amazon = amazon_rep.cria_df_linguagens()

netflix_rep = DadosRepositorios('netflix')
df_netflix = netflix_rep.cria_df_linguagens()

spotify_rep = DadosRepositorios('spotify')
df_spotify = spotify_rep.cria_df_linguagens()

# Salvando os dados

df_amazon.to_csv('data/github_amazon.csv')
df_netflix.to_csv('data/github_netflix.csv')
df_spotify.to_csv('data/github_spotify.csv')

print("Arquivos gerados com sucesso!")