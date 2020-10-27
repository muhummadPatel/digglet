from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    DateTimeField,
    SelectField,
    validators,
    widgets,
)
from markupsafe import escape
from enum import Enum
from app import db


class TicketStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In-Progress"
    CLOSED = "Closed"

    @classmethod
    def choices(cls):
        return [(status.name, escape(status)) for status in TicketStatus]

    @classmethod
    def coerce(cls, val):
        if isinstance(val, TicketStatus):
            return val.name
        try:
            return TicketStatus[val]
        except KeyError:
            raise ValueError(val)

    def __str__(self):
        return self.name  # value string

    def __html__(self):
        return self.value  # label string


# Define the Ticket data model
class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Unicode(50), nullable=False)
    description = db.Column(db.Unicode(255), nullable=False)
    status = db.Column(db.Enum(TicketStatus), nullable=False, index=True)
    requester_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), nullable=False, index=True
    )
    assignee_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), nullable=True, index=True
    )
    create_date = db.Column(db.DateTime(), nullable=False, index=True)

    # Relationships
    requester = db.relationship(
        "User", back_populates="requested_tickets", foreign_keys="Ticket.requester_id"
    )
    assignee = db.relationship(
        "User", back_populates="assigned_tickets", foreign_keys="Ticket.assignee_id"
    )

    def __str__(self):
        return f"{self.title} - {self.status} - {self.create_date}"


# Define the Ticket form
class TicketForm(FlaskForm):
    title = StringField(
        "Title", validators=[validators.DataRequired("Title is required")]
    )
    description = TextAreaField(
        "Description", validators=[validators.DataRequired("Description is required")]
    )
    status = SelectField(
        "Status", choices=TicketStatus.choices(), coerce=TicketStatus.coerce
    )
    create_date = DateTimeField("create_date", widget=widgets.HiddenInput())
    requester_id = IntegerField("requester_id", widget=widgets.HiddenInput())
    assignee_id = IntegerField(
        "assignee_id", validators=[validators.Optional()], widget=widgets.HiddenInput()
    )
    submit = SubmitField("Save")
