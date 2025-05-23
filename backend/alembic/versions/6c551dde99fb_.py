"""empty message

Revision ID: 6c551dde99fb
Revises: 069f8af0c42b
Create Date: 2025-05-12 01:17:06.404827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c551dde99fb'
down_revision: Union[str, None] = '069f8af0c42b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('tickets', sa.Column('assignee_id', sa.Integer(), nullable=True))
    op.drop_constraint('tickets_author_fkey', 'tickets', type_='foreignkey')
    op.drop_constraint('tickets_assignee_fkey', 'tickets', type_='foreignkey')
    op.create_foreign_key(None, 'tickets', 'users', ['assignee_id'], ['id'])
    op.create_foreign_key(None, 'tickets', 'users', ['author_id'], ['id'])
    op.drop_column('tickets', 'author')
    op.drop_column('tickets', 'assignee')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('assignee', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tickets', sa.Column('author', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.create_foreign_key('tickets_assignee_fkey', 'tickets', 'users', ['assignee'], ['id'])
    op.create_foreign_key('tickets_author_fkey', 'tickets', 'users', ['author'], ['id'])
    op.drop_column('tickets', 'assignee_id')
    op.drop_column('tickets', 'author_id')
    # ### end Alembic commands ###
