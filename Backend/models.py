from enum import Enum
from flask_restful import reqparse, fields
from datetime import datetime

# Enums


class DailyObligation(Enum):
    JOB_OBLIGATION = 1
    SCHOOL_OBLIGATION = 2
    GYM_OBLIGATION = 3
    PAPERWORK_OBLIGATION = 4
    INDEPENDENT_OBLIGATION = 5
    SOCIAL_OUTINGS_OBLIGATION = 6


class FatigueLevel(Enum):
    VERY_LOW_FATIGUE = 1
    LOW_FATIGUE = 2
    MODERATE_FATIGUE = 3
    HIGH_FATIGUE = 4
    VERY_HIGH_FATIGUE = 5


class StressLevel(Enum):
    VERY_LOW_STRESS = 1
    LOW_STRESS = 2
    MODERATE_STRESS = 3
    HIGH_STRESS = 4
    VERY_HIGH_STRESS = 5

# REST Arguments


# User arguments for POST
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('nick_name', type=str, required=True,
                            help="Nickname can't be blank.")
user_post_args.add_argument('age', type=int, required=True,
                            help="Age can't be blank.")
user_post_args.add_argument('email', type=str, required=True,
                            help="Email can't be blank.")

# User arguments for PATCH
user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument('nick_name', type=str, required=False)
user_patch_args.add_argument('age', type=str, required=False)
user_patch_args.add_argument('email', type=str, required=False)

# Gaming Session Arguments for POST


def parse_date(date_string: str):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD")


def parse_time(time_string: str):
    try:
        return datetime.strptime(time_string, '%H:%M').time()
    except ValueError:
        raise ValueError("Invalid time format. Expected HH:MM.")


def parse_fatigue_level(fatigue_level: FatigueLevel):
    try:
        return FatigueLevel[fatigue_level]
    except KeyError:
        raise ValueError(
            f"Invalid fatigue level: '{fatigue_level}'. Must be one of {[level.name for level in FatigueLevel]}")


def parse_stress_level(stress_level: StressLevel):
    try:
        return StressLevel[stress_level]
    except KeyError:
        raise ValueError(
            f"Invalid stress level: '{stress_level}'. Must be one of {[level.name for level in StressLevel]}")


def parse_daily_obligations(daily_obligations: DailyObligation):
    try:
        return DailyObligation[daily_obligations]
    except KeyError:
        raise ValueError(
            f"Invalid daily obligation: '{daily_obligations}'. Must be one of {[level.name for level in DailyObligation]}")


user_gaming_session_args = reqparse.RequestParser()
user_gaming_session_args.add_argument('user_id', type=int, required=True,
                                      help="User ID can't be blank.")
user_gaming_session_args.add_argument('event_date', type=parse_date,
                                      required=True, help="Event date is required in format YYYY-MM-DD.")
user_gaming_session_args.add_argument('start_time', type=parse_time,
                                      required=True, help="Start time is required in format HH:MM.")
user_gaming_session_args.add_argument('end_time', type=parse_time,
                                      required=True, help="End time is required in format HH:MM.")
user_gaming_session_args.add_argument('session_duration', type=float,
                                      required=True, help="Session Duration can't be blank.")
user_gaming_session_args.add_argument('fatigue_level', type=parse_fatigue_level,
                                      required=True, help="Invalid or missing fatigue level.")
user_gaming_session_args.add_argument('stress_level', type=parse_stress_level,
                                      required=True, help="Invalid or missing stress level.")
user_gaming_session_args.add_argument('daily_obligations', action='append', type=parse_daily_obligations,
                                      required=True, help="Invalid or missing daily obligation.")

# Agent Arguments for POST
agent_fields_array_args = reqparse.RequestParser()
agent_fields_array_args.add_argument('data', type=list, location='json', required=True,
                                     help="Data should be a list of agent fields.")

# Response Types (JSON format)

# User response
user_fields = {
    'id': fields.Integer,
    'nick_name': fields.String,
    'age': fields.Integer,
    'email': fields.String
}

# Gaming Session response
daily_obligation_fields = {
    'id': fields.Integer,
    'daily_obligation_type': fields.String
}

gaming_session_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'event_date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'session_duration': fields.Float,
    'fatigue_level': fields.String,
    'stress_level': fields.String,
    'daily_obligations': fields.List(fields.Nested(daily_obligation_fields))
}

agent_fields = {
    "predicted_session_duration": fields.String,
}
