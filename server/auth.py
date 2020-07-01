from flask import (
    Blueprint, request, session, jsonify
)
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

from server.db import db, User, Role, UserRoles, UserSchema
from server.utils import generate_random_password, email_service, get_reset_email_body, get_recipients

bp = Blueprint('auth', __name__, url_prefix='/auth')
issue_schema = UserSchema()
CORS(bp)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    resp = jsonify(register=False)

    if request.method == 'POST':
        user = User()
        user_roles = UserRoles()
        user_input = request.get_json()

        username = user_input['username']
        password = user_input['password']
        user_email = user_input['email']

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not user_email:
            error = 'E-Mail is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:

            user.username = username
            user.password = generate_password_hash(password)
            user.user_email = user_email
            db.session.add(user)
            db.session.commit()

            user_roles.user_id = user.id

            if user_email == 'support@info-spectrum.com':
                user_roles.role_id = 1
            else:
                user_roles.role_id = 2

            db.session.add(user_roles)
            db.session.add(user)
            db.session.commit()
            resp = jsonify(register=True)
            return resp

        resp = jsonify(error=error)
    return resp


@bp.route('/login', methods=('GET', 'POST'))
def login():
    resp = jsonify(login=False)

    if request.method == 'POST':
        user_input = request.get_json()

        username = user_input['username']
        password = user_input['password']

        error = None
        try:
            user = User.query.filter_by(username=username).first_or_404()
        except Exception as e:
            print(e)
            user = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            response = User.query.get(user.id)
            user_json_data = issue_schema.dump(response)

            user_role = UserRoles.query.filter_by(user_id=user.id).first()
            role = Role.query.get(user_role.role_id)
            user_json_data["role"] = role.name
            token = create_access_token(identity=user_json_data)

            return jsonify(token=token), 200

        resp = jsonify(error=error)
    return resp


@bp.route('/password-change', methods=('GET', 'POST'))
@jwt_required
def password_change():
    resp = jsonify(password_change=False)

    if request.method == 'POST':
        error = None

        identity = get_jwt_identity()
        user_input = request.get_json()

        username = identity['username']
        old_password = user_input['old_password']
        new_password = user_input['new_password']

        user = User.query.filter_by(username=username).first()

        if not check_password_hash(user.password, old_password):
            error = 'Incorrect Old Password'
        elif not new_password:
            error = 'Password is required.'

        if error is None:
            user.password = generate_password_hash(new_password)
            db.session.add(user)
            db.session.commit()

            resp = jsonify(password_change=True)
            return resp

        resp = jsonify(error=error)

    return resp


@bp.route('/password-reset', methods=('GET', 'POST'))
def password_reset():
    resp = jsonify(password_reset=False)

    if request.method == 'POST':
        error = None
        reset = False
        user_input = request.get_json()
        reset_email = user_input['email_to']

        user = User.query.filter_by(user_email=reset_email).first()

        if user is None:
            error = 'Invalid Email-ID. Try again'

        if error is None:
            new_password = generate_random_password()
            user.password = generate_password_hash(new_password)

            email_body = get_reset_email_body(new_password)
            recipient = get_recipients(reset_email)
            reset = email_service(recipient, email_body, 'PASSWORD RESET ALERT')

        if reset:
            db.session.add(user)
            db.session.commit()
            resp = jsonify(password_reset=True)
            return resp
        else:
            error = 'Password Reset Failed'

        resp = jsonify(error=error)

    return resp


@bp.route('/logout')
def logout():
    session.clear()
    resp = jsonify(login=False)
    return resp
