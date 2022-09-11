import os 

# Defininfo o diretorio de trabalho
PATH: str = os.getcwd()
DATADIR: str = os.path.join(PATH, 'data')

# Configurando o database
BD: dict = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'pgenem',
    'port': '5432',
    'database': 'enem'
}


