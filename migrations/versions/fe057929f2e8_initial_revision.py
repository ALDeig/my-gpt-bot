"""Initial revision

Revision ID: fe057929f2e8
Revises: 
Create Date: 2024-12-27 14:12:45.220244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe057929f2e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ai_models',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('model', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dialogs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tts_voice', sa.Text(), nullable=True),
    sa.Column('image_style', sa.Text(), nullable=False),
    sa.Column('image_format', sa.Text(), nullable=False),
    sa.Column('gpt_model_id', sa.Integer(), nullable=True),
    sa.Column('dalle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dalle_id'], ['ai_models.id'], ),
    sa.ForeignKeyConstraint(['gpt_model_id'], ['ai_models.id'], ),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    op.drop_table('dialogs')
    op.drop_table('users')
    op.drop_table('ai_models')
    # ### end Alembic commands ###
