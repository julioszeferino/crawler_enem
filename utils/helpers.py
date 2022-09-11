from datetime import datetime
from settings import PATH

def logs(*args) -> None:
    '''
    Funcao para gerar logs de execucao..

    :param args: Argumentos a serem logados
    :return: None
    '''
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {args}')
    
    with open(PATH + '/logs/logs.log', 'a') as f:
        f.write(f'\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {args}')