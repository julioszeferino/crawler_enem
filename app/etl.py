from settings import PATH
from utils.helpers import logs
import dask.dataframe as dd
import pandas as pd
from pandas import DataFrame
from settings import BD
import pandera as pa
import sqlalchemy
from sqlalchemy.engine.base import Engine


class ETL:

    def __init__ (self) -> None:
        self.__path_data: str = PATH + '/data/DADOS/MICRODADOS_ENEM_2020.csv'
        self.__conn: str = self._conecta_banco()


    def _extract(self) -> DataFrame:
        '''
        Funcao que extrai os dados do arquivo csv e retorna um dataframe

        :return: df com os dados do crawler
        '''
        # recuperando os dados
        df_temp: DataFrame = dd.read_csv(self.__path_data, sep=';', encoding='iso-8859-1')
        
        # filtrando colunas
        mask: list = [
            'NU_INSCRICAO', 
            'NU_ANO', 
            'TP_SEXO',
            'NO_MUNICIPIO_ESC',
            'SG_UF_ESC',
            'NU_NOTA_CN',
            'NU_NOTA_CH',
            'NU_NOTA_LC',
            'NU_NOTA_MT',
            'Q021',
            'Q016',
            'Q001',
            'Q002',
            'Q005',
            'Q006',
            'TP_LINGUA',
            'TP_FAIXA_ETARIA',
            'TP_ESCOLA'
        ]
        
        df_temp1: DataFrame = df_temp[mask]

        dataset_bronze: DataFrame = df_temp1.loc[df_temp1['SG_UF_ESC'] == 'MG'].compute() 

        if dataset_bronze.shape[0] > 0:
            return dataset_bronze
        else:
            logs('Dados nao foram extraidos..')
            exit()


    def _transform(self, dataset: DataFrame) -> DataFrame:
        
        dataset_silver: DataFrame = dataset.copy()

        # tratando colunas
        dataset_silver['Q021'] = dataset_silver['Q021'].replace({'A': 'NAO', 'B': 'SIM'})
        dataset_silver['Q016'] = dataset_silver['Q016'].replace({'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4+'})
        dataset_silver['Q001'] = dataset_silver['Q001'].replace({
            'A': 'Nunca estudou',
            'B': '5º ano do Ensino Fundamental incompleto',
            'C': '5º ano do Ensino Fundamental completo',
            'D': '9º ano do Ensino Fundamental completo',
            'E': 'Ensino Médio completo',
            'F': 'Faculdade completo',
            'G': 'Pós-graduação completo',
            'H': pd.NA
        })
        dataset_silver['Q002'] = dataset_silver['Q002'].replace({
            'A': 'Nunca estudou',
            'B': '5º ano do Ensino Fundamental incompleto',
            'C': '5º ano do Ensino Fundamental completo',
            'D': '9º ano do Ensino Fundamental completo',
            'E': 'Ensino Médio completo',
            'F': 'Faculdade completo',
            'G': 'Pós-graduação completo',
            'H': pd.NA
        })
        dataset_silver['TP_LINGUA'] = dataset_silver['TP_LINGUA'].replace({
            0: 'Inglês', 
            1: 'Espanhol'})
        dataset_silver['TP_FAIXA_ETARIA'] = dataset_silver['TP_FAIXA_ETARIA'].replace({
            1: 'Menor de 17 anos',
            2: '17 anos',
            3: '18 anos',
            4: '19 anos',
            5: '20 anos',
            6: '21 anos',
            7: '22 anos',
            8: '23 anos',
            9: '24 anos',
            10: '25 anos',
            11: 'Entre 26 e 30 anos',
            12: 'Entre 31 e 35 anos',
            13: 'Entre 36 e 40 anos',
            14: 'Entre 41 e 45 anos',
            15: 'Entre 46 e 50 anos',
            16: 'Entre 51 e 55 anos',
            17: 'Entre 56 e 60 anos',
            18: 'Entre 61 e 65 anos',
            19: 'Entre 66 e 70 anos',
            20: 'Maior de 70 anos'
        })
        dataset_silver['TP_ESCOLA'] = dataset_silver['TP_ESCOLA'].replace({
            1: pd.NA,
            2: 'Pública',
            3: 'Privada',
            4: 'Exterior'
        })
        dataset_silver['Q006'] = dataset_silver['Q006'].replace({
            'A': 'Nenhum',
            'B': 'Até R$ 1.045,00',
            'C': 'R$ 1.045,01 até R$ 1.567,50',
            'D': 'R$ 1.567,51 até R$ 2.090,00',
            'E': 'R$ 2.090,01 até R$ 2.612,50',
            'F': 'R$ 2.612,51 até R$ 3.135,00',
            'G': 'R$ 3.135,01 até R$ 4.180,00',
            'H': 'R$ 4.180,01 até R$ 5.225,00',
            'I': 'R$ 5.225,01 até R$ 6.270,00',
            'J': 'R$ 6.270,01 até R$ 7.315,00',
            'K': 'R$ 7.315,01 até R$ 8.360,00',
            'L': 'R$ 8.360,01 até R$ 9.405,00',
            'M': 'R$ 9.405,01 até R$ 10.450,00',
            'N': 'R$ 10.450,01 até R$ 12.540,00',
            'O': 'R$ 12.540,01 até R$ 15.675,00',
            'P': 'R$ 15.675,01 até R$ 20.900,00',
            'Q': 'Acima de R$ 20.900,00'
        })


        # tratando valores nulos
        dataset_silver['Q021'] = dataset_silver['Q021'].fillna('NAO')
        dataset_silver['NU_NOTA_CN'] = dataset_silver['NU_NOTA_CN'].fillna(0.00)
        dataset_silver['NU_NOTA_CH'] = dataset_silver['NU_NOTA_CH'].fillna(0.00)
        dataset_silver['NU_NOTA_LC'] = dataset_silver['NU_NOTA_LC'].fillna(0.00)
        dataset_silver['NU_NOTA_MT'] = dataset_silver['NU_NOTA_MT'].fillna(0.00)
        dataset_silver['Q005'] = dataset_silver['Q005'].fillna(0.00)

        # tipando colunas
        dataset_silver['Q005'] = dataset_silver['Q005'].astype('int64')

        # removendo espacos em branco
        dataset_silver['NO_MUNICIPIO_ESC'] = dataset_silver['NO_MUNICIPIO_ESC'].str.strip()


        # renomeando colunas
        dataset_silver = dataset_silver.rename(columns={
            'NU_INSCRICAO': 'incricao',
            'NU_ANO': 'ano',
            'TP_SEXO': 'sexo',
            'NO_MUNICIPIO_ESC': 'nome_municipio_escola',
            'SG_UF_ESC': 'sigla_uf_escola',
            'NU_NOTA_CN': 'nota_cn',
            'NU_NOTA_CH': 'nota_ch',
            'NU_NOTA_LC': 'nota_lc',
            'NU_NOTA_MT': 'nota_mt',
            'Q021': 'q_tv_assinatura',
            'Q016': 'q_micro_ondas',
            'Q001': 'q_escolaridade_pai',
            'Q002': 'q_escolaridade_mae',
            'Q005': 'q_qtde_moraddor_residencia',
            'Q006': 'q_renda_mensal',
            'TP_LINGUA': 'lingua_estrangeira',
            'TP_FAIXA_ETARIA': 'faixa_etaria',
            'TP_ESCOLA': 'tipo_escola'
        })


        return dataset_silver

    def _load(self, dataset: DataFrame) -> DataFrame:

        # avaliando a estrutura
        schema = pa.DataFrameSchema(
            columns={
                'incricao': pa.Column(pa.Int, required=True, nullable=False),
                'ano': pa.Column(pa.Int, nullable=False),
                'sexo': pa.Column(pa.String, nullable=False),
                'nome_municipio_escola': pa.Column(pa.String, nullable=False),
                'sigla_uf_escola': pa.Column(pa.String, nullable=False),
                'nota_cn': pa.Column(pa.Float, nullable=False),
                'nota_ch': pa.Column(pa.Float, nullable=False),
                'nota_lc': pa.Column(pa.Float, nullable=False),
                'nota_mt': pa.Column(pa.Float, nullable=False),
                'q_tv_assinatura': pa.Column(pa.String, nullable=True),
                'q_micro_ondas': pa.Column(pa.String, nullable=True),
                'q_escolaridade_pai': pa.Column(pa.String, nullable=True),
                'q_escolaridade_mae': pa.Column(pa.String, nullable=True),
                'q_qtde_moraddor_residencia': pa.Column(pa.Int, nullable=True),
                'q_renda_mensal': pa.Column(pa.String, nullable=True),
                'lingua_estrangeira': pa.Column(pa.String, nullable=False),
                'faixa_etaria': pa.Column(pa.String, nullable=False),
                'tipo_escola': pa.Column(pa.String, nullable=False)
            }) 

        try:
            # validando a estrutura
            schema.validate(dataset)

            dataset_golden: DataFrame = dataset

            return dataset_golden
            
        except Exception as e:
            print(e)
            exit()


    def _conecta_banco(self) -> Engine:
        """
        Função para conectar ao banco de dados.
        """
        conn = f"postgresql://{BD['user']}:{BD['password']}@{BD['host']}/{BD['database']}"
        engine = sqlalchemy.create_engine(conn)
        return engine


    def input_bd(self, df: DataFrame, engine: Engine) -> None:
        
        if df.shape[0] > 0:
            res = df.to_sql('enem', con=engine, if_exists='replace', index=False)
            
            if res > 0:
                logs(f"{res} dados inputados com sucesso!")
            else:
                logs("Nenhum dado foi inserido no banco.")

            engine.dispose()

        else:
            print("Nenhum dados para inserir")
            engine.dispose()

    def run_etl(self) -> None:

        logs('Extraindo os dados..')
        dataset_bronze: DataFrame = self._extract()
        logs('Transformando os dados..')
        dataset_silver: DataFrame = self._transform(dataset_bronze)
        dataset_golden: DataFrame = self._load(dataset_silver)
        logs('ETL concluido..')

        logs('Inserindo os dados no banco de dados..')
        self.input_bd(dataset_golden, self.__conn)
        
