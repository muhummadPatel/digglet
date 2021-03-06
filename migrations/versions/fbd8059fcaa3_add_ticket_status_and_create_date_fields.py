"""add_ticket_status_and_create_date_fields

Revision ID: fbd8059fcaa3
Revises: 817ffe1167a1
Create Date: 2020-10-25 10:34:19.400918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fbd8059fcaa3"
down_revision = "817ffe1167a1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tickets", sa.Column("create_date", sa.DateTime(), nullable=False))
    op.add_column(
        "tickets",
        sa.Column(
            "status",
            sa.Enum("OPEN", "IN_PROGRESS", "CLOSED", name="ticketstatus"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_tickets_assignee_id"), "tickets", ["assignee_id"], unique=False
    )
    op.create_index(
        op.f("ix_tickets_create_date"), "tickets", ["create_date"], unique=False
    )
    op.create_index(
        op.f("ix_tickets_requester_id"), "tickets", ["requester_id"], unique=False
    )
    op.create_index(op.f("ix_tickets_status"), "tickets", ["status"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tickets_status"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_requester_id"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_create_date"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_assignee_id"), table_name="tickets")
    op.drop_column("tickets", "status")
    op.drop_column("tickets", "create_date")
    # ### end Alembic commands ###
