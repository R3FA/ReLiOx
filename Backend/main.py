from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from models import DailyObligation, FatigueLevel, StressLevel, user_post_args, user_patch_args, user_gaming_session_args, agent_fields_array_args, user_fields, gaming_session_fields, daily_obligation_fields, agent_fields
from flask_restful import Resource, Api, marshal_with, abort
from datetime import datetime
from sklearn.neural_network import MLPRegressor
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reliox_database.db'
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

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

    # Relationship to DailyObligations through the junction table
    daily_obligations = db.relationship(
        'DailyObligationsModel',
        secondary='sessions_jt_obligations',
        back_populates='gaming_sessions',
        cascade="save-update, merge"
    )

    def __repr__(self):
        return f"GamingSessions(id={self.id}, user_id={self.user_id}, start_time={self.start_time}, end_time={self.end_time}, session_duration={self.session_duration}, fatigue_level={self.fatigue_level}, daily_obligations={self.daily_obligations}, stress_level={self.stress_level})"

# Daily Obligaiton Database Model


class DailyObligationsModel(db.Model):
    __tablename__ = 'daily_obligations'

    id = db.Column(db.Integer, primary_key=True)
    daily_obligation_type = db.Column(db.Enum(DailyObligation), nullable=False)

    gaming_sessions = db.relationship(
        'GamingSessionsModel',
        secondary='sessions_jt_obligations',
        back_populates='daily_obligations'
    )

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

        # Validation
        if args["age"] <= 0:
            abort(400, message="Age must be a positive number.")

        if not args["nick_name"] or args["nick_name"].isspace():
            abort(400, message="Nickname cannot be empty or just whitespace.")

        if not args["email"] or args["email"].isspace():
            abort(400, message="Email cannot be empty or just whitespace.")

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
        if args.get("nick_name") is not None:
            if args["nick_name"] == "":
                abort(400, message="Nickname cannot be an empty string.")
            if args["nick_name"] != user.nick_name:
                user.nick_name = args["nick_name"]
                has_changes = True

        if args.get("age") is not None:
            if args["age"] == "":
                abort(400, message="Age cannot be empty.")
            try:
                age = int(args["age"])
                if age != user.age:
                    user.age = age
                    has_changes = True
            except ValueError:
                abort(400, message="Age must be a valid integer.")

        if args.get("email") is not None:
            if args["email"] == "":
                abort(400, message="Email cannot be an empty string.")
            if args["email"] != user.email:
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


def check_gaming_session_overlap(user_id, event_date, new_start_time, new_end_time):
    overlapping_sessions = GamingSessionsModel.query.filter(
        GamingSessionsModel.user_id == user_id,
        GamingSessionsModel.event_date == event_date,
        or_(
            and_(
                GamingSessionsModel.start_time <= new_start_time,
                GamingSessionsModel.end_time > new_start_time
            ),
            and_(
                GamingSessionsModel.start_time < new_end_time,
                GamingSessionsModel.end_time >= new_end_time
            ),
            and_(
                GamingSessionsModel.start_time >= new_start_time,
                GamingSessionsModel.end_time <= new_end_time
            )
        )
    ).all()

    if overlapping_sessions:
        abort(
            409,
            message="The selected time range overlaps with an existing gaming session."
        )


class GamingSessions(Resource):
    # Post
    @marshal_with(gaming_session_fields)
    def post(self, user_id):
        args = user_gaming_session_args.parse_args()
        user_gaming_session = GamingSessionsModel(
            user_id=args["user_id"], event_date=args["event_date"], start_time=args["start_time"], end_time=args[
                "end_time"], session_duration=args["session_duration"], fatigue_level=args["fatigue_level"], stress_level=args["stress_level"]
        )

        obligation_enums = args.get("daily_obligations", [])
        if not obligation_enums:
            abort(400, message="Daily Obligation can't be blank and must be provided.")

        if user_gaming_session.user_id != user_id:
            abort(
                400, message=f"User ID({user_gaming_session.user_id}) from query variable doesn't match the User ID({user_id}) from BODY.")

        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(
                404, message=f"User with ID({user_id}) is not found.")

        daily_obligations = DailyObligationsModel.query.filter(
            DailyObligationsModel.daily_obligation_type.in_(obligation_enums)).all()

        check_gaming_session_overlap(
            args["user_id"], args["event_date"], args["start_time"], args["end_time"])

        try:
            db.session.add(user_gaming_session)
            db.session.commit()

            for obligation in daily_obligations:
                junction_entry = SessionsJTObligationsModel(
                    gaming_session_id=user_gaming_session.id,
                    daily_obligations_id=obligation.id
                )
                db.session.add(junction_entry)

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(
                500, message=f"An unexpected database error occurred: {str(e.orig)}"
            )

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


class GamingSessionsByEventDate(Resource):
    # GetAll
    @marshal_with(gaming_session_fields)
    def get(self, event_date, user_id):
        try:
            datetime.strptime(event_date, '%Y-%m-%d')
        except ValueError:
            return abort(400, message=f'Invalid date format, use YYYY-MM-DD')

        user_gaming_sessions = GamingSessionsModel.query.filter_by(
            user_id=user_id, event_date=event_date).all()

        return user_gaming_sessions


class DailyObligations(Resource):
    # GetAll
    @marshal_with(daily_obligation_fields)
    def get(self):
        daily_obligations = DailyObligationsModel.query.all()
        return daily_obligations

# AGENT Logic


def get_fatigue_level(fatigue_string):
    try:
        return FatigueLevel[fatigue_string].value
    except KeyError:
        return abort(404, message=f"Unknown Fatigue Level: {fatigue_string}")


def get_stress_level(stress_string):
    try:
        return StressLevel[stress_string].value
    except KeyError:
        return abort(404, message=f"Unknown Stress Level: {stress_string}")


class AgentSession(Resource):
    @marshal_with(agent_fields)
    def post(self):

        args = agent_fields_array_args.parse_args()
        agent_data = args['data']

        if not agent_data:
            abort(400, message=f"Agent data for prediction is empty.")

        model = MLPRegressor(hidden_layer_sizes=(
            10,), max_iter=500, random_state=42)
        X = []
        Y = []

        fatigue_weight = 0
        stress_weight = 0
        obligations_weight = 0

        for session in agent_data:
            start_time = datetime.strptime(
                session.get("start_time"), "%H:%M:%S").time()
            end_time = datetime.strptime(
                session.get("end_time"), "%H:%M:%S").time()
            fatigue_level_string = session.get("fatigue_level")
            stress_level_string = session.get("stress_level")
            session_duration = session.get("session_duration")
            daily_obligations_count = session.get("daily_obligations_count")
            daily_obligations = session.get("daily_obligations", [])

            if not all([start_time, end_time, fatigue_level_string, stress_level_string, daily_obligations_count, daily_obligations]):
                abort(400, message=f"Not all agent data for prediction is sent.")

            fatigue_level = get_fatigue_level(fatigue_level_string)
            fatigue_weight += fatigue_level
            stress_level = get_stress_level(stress_level_string)
            stress_weight += stress_level

            obligations_impact = 0
            for obligation in daily_obligations:
                if obligation['daily_obligation_type'] == "JOB_OBLIGATION":
                    obligations_impact += 8
                elif obligation['daily_obligation_type'] == "SCHOOL_OBLIGATION":
                    obligations_impact += 6
                elif obligation['daily_obligation_type'] == "GYM_OBLIGATION":
                    obligations_impact += 4
                elif obligation['daily_obligation_type'] == "PAPERWORK_OBLIGATION":
                    obligations_impact += 10
                elif obligation['daily_obligation_type'] == "INDEPENDENT_OBLIGATION":
                    obligations_impact += 6
                elif obligation['daily_obligation_type'] == "SOCIAL_OUTINGS_OBLIGATION":
                    obligations_impact += 2

            obligations_weight += obligations_impact

            X.append([fatigue_weight, stress_weight,
                     obligations_weight])
            Y.append(session_duration)

        print(Y)
        print(fatigue_weight)
        print(stress_weight)
        print(obligations_weight)

        model.fit(X, Y)

        predicted_duration = model.predict(X)
        hours = int(predicted_duration[0])
        minutes = int((predicted_duration[0] % 1) * 60)

        responseMessage = {
            "predicted_session_duration": f"Gaming session should last for {hours} hours and {minutes} minutes."
        }

        return responseMessage, 200


# Route registration
# User routes
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

# GamingSession routes
api.add_resource(
    GamingSessions, '/api/user-gaming-session/<int:user_id>')
api.add_resource(
    GamingSession, '/api/user-gaming-session/<int:id>/<int:user_id>')

api.add_resource(GamingSessionsByEventDate,
                 '/api/user-gaming-session/<string:event_date>/<int:user_id>')

# DailyObligation routes
api.add_resource(DailyObligations, '/api/daily-obligations/')

# Agent routes
api.add_resource(AgentSession, '/api/agent-session/')

if __name__ == "__main__":
    app.run(debug=True)
