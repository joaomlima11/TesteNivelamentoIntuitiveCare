import pdfplumber
import pandas as pd
import zipfile
import os
pdf_file = "Anexo_I.pdf"
csv_file = "Teste_JoaoVictor.csv"
zip_file = "Teste_JoaoVictor.zip"
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}
def extrair_dados(pdf_file=pdf_file):
    dados = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                dados.extend(table)
    return dados
dados_extraidos = extrair_dados(pdf_file)
df = pd.DataFrame(dados_extraidos)
df.rename(columns=substituicoes, inplace=True)
df.to_csv(csv_file, index=False, encoding='utf-8')
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file)
    os.remove(csv_file)

    print(f"Processo concluído! Arquivo gerado: {zip_file}")