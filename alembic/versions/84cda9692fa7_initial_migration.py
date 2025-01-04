"""Initial migration

Revision ID: 84cda9692fa7
Revises: 
Create Date: 2025-01-04 15:46:34.174432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '84cda9692fa7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Добавляем только индексы, чтобы не ломать существующую БД
    op.create_index(op.f('ix_category_category_id'), 'category', ['category_id'], unique=False)
    op.create_index(op.f('ix_city_city_id'), 'city', ['city_id'], unique=False)
    op.create_index(op.f('ix_excursion_excursion_id'), 'excursion', ['excursion_id'], unique=False)
    op.create_index(op.f('ix_organizer_organizer_id'), 'organizer', ['organizer_id'], unique=False)

def downgrade() -> None:
    # Откат удаляет только индексы
    op.drop_index(op.f('ix_organizer_organizer_id'), table_name='organizer')
    op.drop_index(op.f('ix_excursion_excursion_id'), table_name='excursion')
    op.drop_index(op.f('ix_city_city_id'), table_name='city')
    op.drop_index(op.f('ix_category_category_id'), table_name='category')
