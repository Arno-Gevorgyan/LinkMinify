"""002_add_user short link

Revision ID: 54070fbe97b4
Revises: c4ee861ea43b
Create Date: 2024-01-06 16:43:12.097847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54070fbe97b4'
down_revision = 'c4ee861ea43b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_links',
    sa.Column('short_url', sa.String(length=25), nullable=False),
    sa.Column('full_url', sa.String(length=2000), nullable=False),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('uuid_generate_v7()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_short_links')),
    sa.UniqueConstraint('uuid', name=op.f('uq_short_links_uuid'))
    )
    op.create_index(op.f('ix_short_links_full_url'), 'short_links', ['full_url'], unique=True)
    op.create_index(op.f('ix_short_links_short_url'), 'short_links', ['short_url'], unique=True)
    op.create_table('user_short_links',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('short_link_id', sa.UUID(), nullable=False),
    sa.Column('uuid', sa.UUID(), server_default=sa.text('uuid_generate_v7()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['short_link_id'], ['short_links.uuid'], name=op.f('fk_user_short_links_short_link_id_short_links'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], name=op.f('fk_user_short_links_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_user_short_links')),
    sa.UniqueConstraint('uuid', name=op.f('uq_user_short_links_uuid'))
    )
    op.create_unique_constraint(op.f('uq_users_uuid'), 'users', ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_uuid'), 'users', type_='unique')
    op.drop_table('user_short_links')
    op.drop_index(op.f('ix_short_links_short_url'), table_name='short_links')
    op.drop_index(op.f('ix_short_links_full_url'), table_name='short_links')
    op.drop_table('short_links')
    # ### end Alembic commands ###
