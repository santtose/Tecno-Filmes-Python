"""atividadehistorico correto

Revision ID: bf91d9336600
Revises: dff043b26ab9
Create Date: 2020-07-10 15:35:59.392280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf91d9336600'
down_revision = 'dff043b26ab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('atividadehistorico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=500), nullable=True),
    sa.Column('atividade_id', sa.Integer(), nullable=True),
    sa.Column('acao_id', sa.Integer(), nullable=True),
    sa.Column('subacao_id', sa.Integer(), nullable=True),
    sa.Column('motivoAcao_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['acao_id'], ['acao.id'], ),
    sa.ForeignKeyConstraint(['atividade_id'], ['atividade.id'], ),
    sa.ForeignKeyConstraint(['motivoAcao_id'], ['motivoacao.id'], ),
    sa.ForeignKeyConstraint(['subacao_id'], ['subacao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('atividadeHistorico')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('atividadeHistorico',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"atividadeHistorico_id_seq1"\'::regclass)'), nullable=False),
    sa.Column('descricao', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('atividade_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('acao_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('subacao_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('motivoAcao_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['acao_id'], ['acao.id'], name='atividadeHistorico_acao_id_fkey1'),
    sa.ForeignKeyConstraint(['atividade_id'], ['atividade.id'], name='atividadeHistorico_atividade_id_fkey1'),
    sa.ForeignKeyConstraint(['motivoAcao_id'], ['motivoacao.id'], name='atividadeHistorico_motivoAcao_id_fkey1'),
    sa.ForeignKeyConstraint(['subacao_id'], ['subacao.id'], name='atividadeHistorico_subacao_id_fkey1'),
    sa.PrimaryKeyConstraint('id', name='atividadeHistorico_pkey1')
    )
    op.drop_table('atividadehistorico')
    # ### end Alembic commands ###
