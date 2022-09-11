from email.policy import default
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime, time

Base = declarative_base()
metadata = Base.metadata

class Enem(Base):

    __tablename__: str = 'enem'

    incricao: int= sa.Column(sa.BigInteger, primary_key=True)
    ano: int= sa.Column(sa.Integer, nullable=False)
    sexo: str= sa.Column(sa.String(1), nullable=False)
    nome_municipio_escola: str= sa.Column(sa.String(100), nullable=False)
    sigla_uf_escola: str= sa.Column(sa.String(2), nullable=False)
    nota_cn: float= sa.Column(sa.DECIMAL(15, 2), nullable=False)
    nota_ch: float= sa.Column(sa.DECIMAL(15, 2), nullable=False)
    nota_lc: float= sa.Column(sa.DECIMAL(15, 2), nullable=False)
    nota_mt: float= sa.Column(sa.DECIMAL(15, 2), nullable=False)
    lingua_estrangeira: str= sa.Column(sa.String(25), nullable=False)
    faixa_etaria: str= sa.Column(sa.String(100), nullable=False)
    tipo_escola: str= sa.Column(sa.String(25), nullable=False)
    q_tv_assinatura: str= sa.Column(sa.String(3), nullable=True)
    q_micro_ondas: int= sa.Column(sa.String(2), nullable=True)
    q_escolaridade_mae: str= sa.Column(sa.String(100), nullable=True)
    q_escolaridade_pai: str= sa.Column(sa.String(100), nullable=True)
    q_qtde_moraddor_residencia: int= sa.Column(sa.Integer, nullable=True)
    q_renda_mensal: str= sa.Column(sa.String(100), nullable=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    def __repr__(self):
        return f'<Inscricao: {self.incricao}>'





