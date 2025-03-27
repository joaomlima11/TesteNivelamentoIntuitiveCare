import requests
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile

def download_pdf(url, nome_arquivo):
    resposta = requests.get(url)
    if resposta .status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(resposta.content)
            print(f"Arquivo {nome_arquivo} baixado com sucesso!")
    else:
        print(f"Erro ao baixar {nome_arquivo}: {resposta.status_code}")

def compactar_em_zip(arquivos, nome_arquivo_zip):
    with ZipFile(nome_arquivo_zip, 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
            print(f"Adicionado {arquivo} ao arquivo ZIP.")
            print(f"Arquivo ZIP {nome_arquivo_zip} criado com sucesso!")
url_site = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
response = requests.get(url_site)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links_pdfs = []
    for a in soup.find_all('a', href=True):
        if "Anexo I" in a.get_text() or "Anexo_II" in a.get_text():
            links_pdfs.append(a['href'])
    if len(links_pdfs) >= 2:
        download_pdf(links_pdfs[0], "Anexo_I.pdf")
        download_pdf(links_pdfs[1], "Anexo_II.pdf")
        compactar_em_zip(["Anexo_I.pdf", "Anexo_II.pdf"], "anexos.zip")
    else:
        print("Não foram encontrados os anexos no site.")
else:
    print(f"Erro ao acessar site: {response.status_code}")






