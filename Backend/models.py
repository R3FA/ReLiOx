from enum import Enum
from flask_restful import reqparse, fields
from datetime import datetime

# Enums


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class DailyObligation(ExtendedEnum):
    JOB_OBLIGATION = 8
    SCHOOL_OBLIGATION = 6
    GYM_OBLIGATION = 4
    PAPERWORK_OBLIGATION = 10
    INDEPENDENT_OBLIGATION = 6
    SOCIAL_OUTINGS_OBLIGATION = 2


class FatigueLevel(ExtendedEnum):
    VERY_LOW_FATIGUE = 1
    LOW_FATIGUE = 3
    MODERATE_FATIGUE = 5
    HIGH_FATIGUE = 8
    VERY_HIGH_FATIGUE = 10


class StressLevel(ExtendedEnum):
    VERY_LOW_STRESS = 1
    LOW_STRESS = 3
    MODERATE_STRESS = 5
    HIGH_STRESS = 8
    VERY_HIGH_STRESS = 10


class AgentData:
    fatigue: int
    stress: int
    daily_obligations: int
    session_duration: int

    def __init__(self, fatigue: int, stress: int, daily_obligations: int, session_duration: int):
        self.fatigue = fatigue
        self.stress = stress
        self.daily_obligations = daily_obligations
        self.session_duration = session_duration


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
user_gaming_session_args.add_argument('fatigue_level', type=parse_fatigue_level,
                                      required=True, help="Invalid or missing fatigue level.")
user_gaming_session_args.add_argument('stress_level', type=parse_stress_level,
                                      required=True, help="Invalid or missing stress level.")
user_gaming_session_args.add_argument('daily_obligations', action='append', type=parse_daily_obligations,
                                      required=True, help="Invalid or missing daily obligation.")

# Agent Arguments for POST
agent_fields_array_args = reqparse.RequestParser()
agent_fields_array_args.add_argument('fatigue_level', type=parse_fatigue_level,
                                     required=True, help="Invalid or missing fatigue level.")
agent_fields_array_args.add_argument('stress_level', type=parse_stress_level,
                                     required=True, help="Invalid or missing stress level.")
agent_fields_array_args.add_argument('daily_obligations', action='append', type=parse_daily_obligations,
                                     required=True, help="Invalid or missing daily obligation.")

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
    'fatigue_level': fields.String,
    'stress_level': fields.String,
    'daily_obligations': fields.List(fields.Nested(daily_obligation_fields))
}

agent_fields = {
    "predicted_session_duration": fields.String,
}
