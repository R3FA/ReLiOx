from enum import Enum
from flask_restful import reqparse, fields

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
user_gaming_session_args = reqparse.RequestParser()
user_gaming_session_args.add_argument('user_id', type=int, required=True,
                                      help="User ID can't be blank.")
user_gaming_session_args.add_argument('event_date', type=str,
                                      required=True, help="Event Date can't be blank.")
user_gaming_session_args.add_argument('start_time', type=str,
                                      required=True, help="Start Time can't be blank.")
user_gaming_session_args.add_argument('end_time', type=str,
                                      required=True, help="End Time can't be blank.")
user_gaming_session_args.add_argument('session_duration', type=float,
                                      required=True, help="Session Duration can't be blank.")
user_gaming_session_args.add_argument('fatigue_level', type=str,
                                      required=True, help="Fatigue Level can't be blank.")
user_gaming_session_args.add_argument('stress_level', type=str,
                                      required=True, help="Stress Level can't be blank.")


# Response Types (JSON format)

# User response
user_fields = {
    'id': fields.Integer,
    'nick_name': fields.String,
    'age': fields.Integer,
    'email': fields.String
}

# Gaming Session response
gaming_session_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'event_date': fields.String,  # TODO: Format string to DATE only
    'start_time': fields.String,  # TODO: Format string to TIME only
    'end_time': fields.String,  # TODO: Format string to TIME only
    'session_duration': fields.Float,
    'fatigue_level': fields.String,
    'stress_level': fields.String
}
