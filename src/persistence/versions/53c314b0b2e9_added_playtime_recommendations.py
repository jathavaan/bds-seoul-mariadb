"""added playtime recommendations

Revision ID: 53c314b0b2e9
Revises: afee4a5ad9c8
Create Date: 2025-05-20 15:27:51.212143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53c314b0b2e9'
down_revision: Union[str, None] = 'afee4a5ad9c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playtime_recommendations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time_interval', sa.Enum('ZERO_TO_FORTY_NINE', 'FIFTY_TO_NINETY_NINE', 'HUNDRED_TO_HUNDRED_NINETY_NINE', 'TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE', 'FIFE_HUNDRED_PLUS', name='time_interval'), nullable=False),
    sa.Column('sum_recommended', sa.Integer(), nullable=False),
    sa.Column('sum_not_recommended', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playtime_recommendations')
    # ### end Alembic commands ###
