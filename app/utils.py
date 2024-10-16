import pandas as pd
from .models import Candidato

def add_candidatos_from_xls(archive):
    df = pd.read_excel(archive)
    
    if df.empty:
        print("Arquivo vazio...")
    
    df.columns = df.columns.str.strip()
    print(df.columns)

    for _, row in df.iterrows():
        candidato = Candidato(
            name=row['NOME'],
            cpf=row['CPF'],
        )
        print(candidato.name, " adicionado!")

        candidato.save()