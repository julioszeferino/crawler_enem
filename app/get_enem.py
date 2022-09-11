from settings import PATH
import requests
from requests.exceptions import ConnectionError
import os
from io import BytesIO
import zipfile
from utils.helpers import logs

class Crawler:

    def __init__(self) -> None:
        self.__url: str = 'https://download.inep.gov.br/microdados/microdados_enem_2020.zip'
        self.__certificado: str = PATH + '/cert_inep.pem'
        self.__path_data: str = PATH + '/data'

    def download_file(self) -> None:
        
            logs('Criando o diretorio de dados..')
            
            os.makedirs(self.__path_data, exist_ok=True)
            os.system(f'rm -rf {self.__path_data}/*')

            try:
                logs('Requisitando os dados..')
                response = requests.get('https://download.inep.gov.br/microdados/microdados_enem_2020.zip', verify=self.__certificado)
                
                logs('Requisicao bem sucedida..')
                filebytes = BytesIO(response.content)

                logs('Descompactando o arquivo zip..')
                myzip = zipfile.ZipFile(filebytes)
                myzip.extractall(self.__path_data)

                logs('Arquivo descompactado com sucesso!')
            
            except ConnectionError:
                logs('Erro de conexao.. Limpano o diretorio de dados..')
                os.system(f'rm -rf {self.__path_data}')
                exit()
            
    
                    
                

            