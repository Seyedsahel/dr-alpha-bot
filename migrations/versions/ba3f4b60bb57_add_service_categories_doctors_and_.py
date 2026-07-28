"""add service categories, doctors and clinic info tables

Revision ID: ba3f4b60bb57
Revises: 8b80ee3596fe
Create Date: 2026-07-28 20:39:29.481839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba3f4b60bb57'
down_revision = '8b80ee3596fe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('clinic_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('instagram', sa.String(length=200), nullable=True),
    sa.Column('bale_channel', sa.String(length=200), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_clinic_info'))
    )
    op.create_table('doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('medical_license_number', sa.String(length=50), nullable=True),
    sa.Column('photo_path', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_doctors'))
    )
    op.create_table('service_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_service_categories')),
    sa.UniqueConstraint('name', name=op.f('uq_service_categories_name'))
    )
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_appointments_slot_id'), type_='unique')

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_services_category_id_service_categories'), 'service_categories', ['category_id'], ['id'])


def downgrade():
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_services_category_id_service_categories'), type_='foreignkey')
        batch_op.drop_column('category_id')

    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_appointments_slot_id'), ['slot_id'])

    op.drop_table('service_categories')
    op.drop_table('doctors')
    op.drop_table('clinic_info')