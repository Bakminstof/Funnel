"""Initial

Revision ID: 61351c3a3241
Revises: 
Create Date: 2024-05-09 11:50:36.861665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61351c3a3241'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('tg_id', sa.BIGINT(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('status', sa.Enum('alive', 'dead', 'finished', name='status'), nullable=False),
    sa.Column('status_updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tg_id', name='user__tg_id__uc'),
    sa.UniqueConstraint('username', name='user__username__uc')
    )
    op.create_table('message_audit',
    sa.Column('init_msg', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('msg_1_timestamp', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('msg_2_timestamp', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('msg_3_timestamp', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_audit')
    op.drop_table('user')
    # ### end Alembic commands ###
