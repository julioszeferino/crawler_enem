"""Primeira migration

Revision ID: 2377e3cfbea7
Revises: 
Create Date: 2022-09-10 22:42:58.224624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2377e3cfbea7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enem',
    sa.Column('incricao', sa.BigInteger(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('sexo', sa.String(length=1), nullable=False),
    sa.Column('nome_municipio_escola', sa.String(length=100), nullable=False),
    sa.Column('sigla_uf_escola', sa.String(length=2), nullable=False),
    sa.Column('nota_cn', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('nota_ch', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('nota_lc', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('nota_mt', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('lingua_estrangeira', sa.String(length=25), nullable=False),
    sa.Column('faixa_etaria', sa.String(length=100), nullable=False),
    sa.Column('tipo_escola', sa.String(length=25), nullable=False),
    sa.Column('q_tv_assinatura', sa.String(length=3), nullable=True),
    sa.Column('q_micro_ondas', sa.String(length=2), nullable=True),
    sa.Column('q_escolaridade_mae', sa.String(length=100), nullable=True),
    sa.Column('q_escolaridade_pai', sa.String(length=100), nullable=True),
    sa.Column('q_qtde_moraddor_residencia', sa.Integer(), nullable=True),
    sa.Column('q_renda_mensal', sa.String(length=100), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('incricao')
    )
    op.create_index(op.f('ix_enem_data_criacao'), 'enem', ['data_criacao'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_enem_data_criacao'), table_name='enem')
    op.drop_table('enem')
    # ### end Alembic commands ###
