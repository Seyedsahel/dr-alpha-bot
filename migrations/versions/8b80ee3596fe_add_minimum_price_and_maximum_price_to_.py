"""add minimum_price and maximum_price to services

Revision ID: 8b80ee3596fe
Revises: df268da43f58
Create Date: 2026-07-20 00:56:23.538889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b80ee3596fe'
down_revision = 'df268da43f58'
branch_labels = None
depends_on = None



def upgrade():

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('minimum_price', sa.BigInteger(), nullable=True))
        batch_op.add_column(sa.Column('maximum_price', sa.BigInteger(), nullable=True))

    # data migration: backfill minimum_price از فیلد قدیمی price
    services_table = sa.table(
        "services",
        sa.column("id", sa.Integer),
        sa.column("price", sa.BigInteger),
        sa.column("minimum_price", sa.BigInteger)
    )

    connection = op.get_bind()

    connection.execute(
        services_table.update()
        .where(services_table.c.price.isnot(None))
        .values(minimum_price=services_table.c.price)
    )


def downgrade():

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_column('maximum_price')
        batch_op.drop_column('minimum_price')