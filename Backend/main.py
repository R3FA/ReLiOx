from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import DailyObligation, FatigueLevel, StressLevel, user_post_args, user_patch_args, user_gaming_session_args, user_fields, gaming_session_fields
from flask_restful import Resource, Api, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reliox_database.db'
db = SQLAlchemy(app)
api = Api(app)

# Database Models

# User DB Model


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(40), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

    sessions = db.relationship(
        'GamingSessionsModel', backref='users', cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(id={self.id}, name={self.nick_name}, age={self.age}, email={self.email})"

# Gaming Session Database Model


class GamingSessionsModel(db.Model):
    __tablename__ = 'gaming_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    session_duration = db.Column(db.Float, nullable=False)
    fatigue_level = db.Column(db.Enum(FatigueLevel), nullable=False)
    stress_level = db.Column(db.Enum(StressLevel), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_date',
                            name='unique_user_event_date'),
    )

    # Relationship to DailyObligations through the junction table
    daily_obligations = db.relationship(
        'DailyObligationsModel',
        secondary='sessions_jt_obligations',
        backref=db.backref('gaming_sessions', lazy=True)
    )

    def __repr__(self):
        return f"GamingSessions(id={self.id}, user_id={self.user_id}, start_time={self.start_time}, end_time={self.end_time}, session_duration={self.session_duration}, fatigue_level={self.fatigue_level}, daily_obligations={self.daily_obligations}, stress_level={self.stress_level})"

# Daily Obligaiton Database Model


class DailyObligationsModel(db.Model):
    __tablename__ = 'daily_obligations'

    id = db.Column(db.Integer, primary_key=True)
    daily_obligation_type = db.Column(db.Enum(DailyObligation), nullable=False)

    def __repr__(self):
        return f"DailyObligations(id = {self.id}, daily_obligation_type{self.daily_obligation_type})"

# Sessions JT Obligations Database Model


class SessionsJTObligationsModel(db.Model):
    __tablename__ = 'sessions_jt_obligations'

    id = db.Column(db.Integer, primary_key=True)
    gaming_session_id = db.Column(
        db.Integer, db.ForeignKey('gaming_sessions.id'), nullable=False)
    daily_obligations_id = db.Column(
        db.Integer, db.ForeignKey('daily_obligations.id'), nullable=False)

    def __repr__(self):
        return f"SessionsJTObligations(id = {self.id}, gaming_session_id = {self.gaming_session_id}, daily_obligations_id = {self.daily_obligations_id})"

# REST Service

# USERS Controller


class Users(Resource):
    # GetAll
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users

    # Post
    @marshal_with(user_fields)
    def post(self):
        args = user_post_args.parse_args()
        user = UserModel(
            nick_name=args["nick_name"], age=args["age"], email=args["email"]
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "users.nick_name" in str(e.orig):
                abort(
                    409, message=f"Nickname already exists. Please choose another one.")
            elif "users.email" in str(e.orig):
                abort(
                    409, message=f"Email already exists. Please use another email.")
            else:
                abort(500, message=f"An unexpected database error occurred.")

        return user, 201


class User(Resource):
    # GetById
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with ID({id}) is not found.")
        return user

    # Patch
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_patch_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()

        if not user:
            abort(404, message=f"User with ID {id} is not found.")

        has_changes = False
        if args.get("nick_name") is not None and args["nick_name"] != user.nick_name:
            user.nick_name = args["nick_name"]
            has_changes = True
        if args.get("age") is not None and int(args["age"]) != user.age:
            user.age = int(args["age"])
            has_changes = True
        if args.get("email") is not None and args["email"] != user.email:
            user.email = args["email"]
            has_changes = True

        if not has_changes:
            return abort(400, message=f"No changes detected. Existing data matches the input.")

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "users.nick_name" in str(e.orig):
                abort(
                    409, message="Nickname already exists. Please choose another one.")
            elif "users.email" in str(e.orig):
                abort(
                    409, message="Email already exists. Please use another email.")
            else:
                abort(500, message="An unexpected database error occurred.")

        return user, 200

    # Delete
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with ID({id}) is not found.")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User has been successfully deleted"}, 200

# GAMING SESSION Controller


class GamingSessions(Resource):
    # GetAll
    @marshal_with(gaming_session_fields)
    def get(self, user_id):
        user_gaming_sessions = GamingSessionsModel.query.filter_by(
            user_id=user_id).all()
        return user_gaming_sessions

    # Post
    @marshal_with(gaming_session_fields)
    def post(self, user_id):
        args = user_gaming_session_args.parse_args()
        user_gaming_session = GamingSessionsModel(
            user_id=args["user_id"], event_date=args["event_date"], start_time=args["start_time"], end_time=args[
                "end_time"], session_duration=args["session_duration"], fatigue_level=args["fatigue_level"], stress_level=args["stress_level"]
        )

        if user_gaming_session.user_id != user_id:
            abort(
                400, message=f"User ID({user_gaming_session.user_id}) from query variable doesn't match the User ID({user_id}) from BODY.")

        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(
                404, message=f"User with ID({user_id}) is not found.")
        try:
            db.session.add(user_gaming_session)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "gaming_sessions.event_date" in str(e.orig):
                abort(
                    409, message=f"Event Date already exists. Please choose another one.")
            else:
                abort(500, message=f"An unexpected database error occurred.")

        return user_gaming_session, 201


class GamingSession(Resource):
    @marshal_with(gaming_session_fields)
    # GetById
    def get(self, id, user_id):
        user_gaming_session = GamingSessionsModel.query.filter_by(
            id=id, user_id=user_id).first()
        if not user_gaming_session:
            abort(
                404, message=f"User Gaming Session with ID({id}) and User ID({user_id}) is not found.")
        return user_gaming_session

    # DeleteById
    def delete(self, id, user_id):
        user_gaming_session = GamingSessionsModel.query.filter_by(
            id=id, user_id=user_id).first()
        if not user_gaming_session:
            abort(
                404, message=f"User Gaming Session with ID({id}) and User ID({user_id}) is not found.")
        db.session.delete(user_gaming_session)
        db.session.commit()
        return {"message": "User Gaming Session has been successfully deleted"}, 200


# Route registration


# User routes
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

# GamingSession routes
api.add_resource(
    GamingSessions, '/api/user-gaming-session/<int:user_id>')
api.add_resource(
    GamingSession, '/api/user-gaming-session/<int:id>/<int:user_id>')

if __name__ == "__main__":
    app.run(debug=True)
