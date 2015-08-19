"""empty message

Revision ID: 4c6d24c7bea1
Revises: 21bb1980d045
Create Date: 2015-08-12 10:47:32.119696

"""

# revision identifiers, used by Alembic.
revision = '4c6d24c7bea1'
down_revision = '21bb1980d045'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('captures', sa.Column('returns', sa.TEXT(), nullable=True))
    op.create_table('collector',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('payload_id', sa.INTEGER(), nullable=True),
    sa.Column('javascript_name', sa.VARCHAR(length=500), nullable=False),
    sa.Column('data', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['payload_id'], [u'payloads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###