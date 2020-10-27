from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from datetime import datetime
from app import db
from app.models import UserProfileForm, Ticket, TicketStatus, TicketForm
from flask.helpers import flash

main_blueprint = Blueprint("main", __name__, template_folder="templates")


# The Home page is accessible to anyone
@main_blueprint.route("/")
def home_page():
    return render_template("main/home_page.html")


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route("/user", methods=["GET", "POST"])
@login_required  # Limits access to authenticated users
def user_page():
    ticket = Ticket(
        requester_id=current_user.id,
        status=TicketStatus.OPEN,
        create_date=datetime.now(),
    )
    form = TicketForm(request.form, obj=ticket)

    print(current_user)
    print(current_user.__dict__)
    print(current_user.id)
    if form.validate_on_submit():
        # Copy form fields to user_profile fields
        form.populate_obj(ticket)

        # Save ticket
        db.session.add(ticket)
        db.session.commit()

        # reset form and      flash success

        flash("Successfully created ticket", "success")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in the %s field - %s"
                    % (getattr(form, field).label.text, error),
                    "error",
                )

    # Pull all tickets requested by this user for display
    tickets = current_user.requested_tickets

    return render_template("main/user_page.html", form=form, tickets=tickets)


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route("/admin")
@roles_required("admin")  # Limits access to users with the 'admin' role
def admin_page():
    return render_template("main/admin_page.html")


@main_blueprint.route("/main/profile", methods=["GET", "POST"])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if form.validate_on_submit():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for("main.home_page"))

    # Process GET or invalid POST
    return render_template("main/user_profile_page.html", form=form)


@main_blueprint.route("/ticket/<int:ticket_id>", methods=["GET"])
@login_required
def ticket_page(ticket_id):
    ticket = Ticket.query.filter(Ticket.id == ticket_id).one()
    return render_template("main/ticket_page.html", ticket=ticket)
