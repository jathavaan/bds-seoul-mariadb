"""Fixed typo in enum value

Revision ID: f7adc547ceca
Revises: fd594a98230b
Create Date: 2025-05-21 13:44:11.010154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f7adc547ceca'
down_revision: Union[str, None] = 'fd594a98230b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recommendations', 'time_interval',
               existing_type=mysql.ENUM('ZERO_TO_FORTY_NINE', 'FIFTY_TO_NINETY_NINE', 'HUNDRED_TO_HUNDRED_NINETY_NINE', 'TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE', 'FIFE_HUNDRED_PLUS'),
               type_=sa.Enum('ZERO_TO_FORTY_NINE', 'FIFTY_TO_NINETY_NINE', 'HUNDRED_TO_HUNDRED_NINETY_NINE', 'TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE', 'FIVE_HUNDRED_PLUS', name='time_interval'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recommendations', 'time_interval',
               existing_type=sa.Enum('ZERO_TO_FORTY_NINE', 'FIFTY_TO_NINETY_NINE', 'HUNDRED_TO_HUNDRED_NINETY_NINE', 'TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE', 'FIVE_HUNDRED_PLUS', name='time_interval'),
               type_=mysql.ENUM('ZERO_TO_FORTY_NINE', 'FIFTY_TO_NINETY_NINE', 'HUNDRED_TO_HUNDRED_NINETY_NINE', 'TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE', 'FIFE_HUNDRED_PLUS'),
               existing_nullable=False)
    # ### end Alembic commands ###
