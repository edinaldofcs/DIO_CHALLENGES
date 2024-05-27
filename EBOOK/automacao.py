import pandas as pd
from sqlalchemy import create_engine, Integer, String, Float, Date
from config import server,database,driver

def subir_para_o_banco_de_dados():
    try:
        # Lembre de adaptar a url para a pasta e nome do seu arquivo
        base_url = "https://raw.githubusercontent.com/"
        user = "edinaldofcs"
        repo_branch = "/DIO_CHALLENGES/desenvolvimento/EBOOK/"
        url = base_url + user + repo_branch + 'tabela_vendas.csv'
        
        # Criar a string de conexão usando as informações do arquivo config.py
        connection_string = f'mssql+pyodbc://{server}/{database}?driver={driver}'
        
        # Criar o objeto de conexão com o banco de dados
        engine = create_engine(connection_string)
        
        # Nome da tabela
        table_name = 'tabela_vendas'
        
        # Ler os dados do arquivo CSV diretamente da URL para um DataFrame
        df = pd.read_csv(url, dtype=str)
        
        # Remover espaços nos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Substituir espaços por underscores nos nomes das colunas
        df.columns = df.columns.str.replace(' ', '_')
        
        # Converter nomes das colunas para letras minúsculas
        df.columns = df.columns.str.lower()
        
        # Converter a coluna de datas para o formato adequado do SQL Server
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y').dt.date
        tipos_de_dados = {
            'id_venda': Integer(),
            'data': Date(),
            'cliente': String(100),
            'produto': String(100),
            'quantidade': Integer(),
            'preco_unitario': Float(),
            'valor_total': Float()
        }
        
        # Converter as colunas de valores para formato numérico adequado (float)
        df['preco_unitario'] = df['preco_unitario'].str.replace(',', '.').astype(float)
        df['valor_total'] = df['valor_total'].str.replace(',', '.').astype(float)
        
        # Subir os dados para a tabela no SQL Server
        print("Subindo para o Banco de dados...Aguarde")
        df.to_sql(table_name, engine, index=False, if_exists='replace',
        dtype = tipos_de_dados)
        print("Processo finalizado")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


subir_para_o_banco_de_dados()