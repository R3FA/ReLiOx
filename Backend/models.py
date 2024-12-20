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


# Response Types (JSON format)

# User response
userFields = {
    'id': fields.Integer,
    'nick_name': fields.String,
    'age': fields.Integer,
    'email': fields.String
}
