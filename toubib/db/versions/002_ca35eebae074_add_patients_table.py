"""patients

Revision ID: ca35eebae074
Revises: 001
Create Date: 2023-10-28 08:40:17.823644

"""
import sqlalchemy as sa
from alembic import op
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ca35eebae074'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('patients',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False, primary_key=True),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=320), nullable=False),
    sa.Column('sex_at_birth', postgresql.ENUM('FEMALE', 'MALE', name='gender_types'), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.UniqueConstraint('email')
    )


def downgrade():
    op.execute("DROP TYPE gender_types;")
    op.drop_table('patients')
