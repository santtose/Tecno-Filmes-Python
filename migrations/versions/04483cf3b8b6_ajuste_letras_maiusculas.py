"""Ajuste letras maiusculas

Revision ID: 04483cf3b8b6
Revises: bf91d9336600
Create Date: 2020-07-10 15:44:22.399297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04483cf3b8b6'
down_revision = 'bf91d9336600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('atividadehistorico', sa.Column('motivoacao_id', sa.Integer(), nullable=True))
    op.drop_constraint('atividadehistorico_motivoAcao_id_fkey', 'atividadehistorico', type_='foreignkey')
    op.create_foreign_key(None, 'atividadehistorico', 'motivoacao', ['motivoacao_id'], ['id'])
    op.drop_column('atividadehistorico', 'motivoAcao_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('atividadehistorico', sa.Column('motivoAcao_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'atividadehistorico', type_='foreignkey')
    op.create_foreign_key('atividadehistorico_motivoAcao_id_fkey', 'atividadehistorico', 'motivoacao', ['motivoAcao_id'], ['id'])
    op.drop_column('atividadehistorico', 'motivoacao_id')
    # ### end Alembic commands ###
