from main import app, db, DailyObligationsModel, AgentTrainedDataModel
from models import DailyObligation, StressLevel, FatigueLevel, AgentData
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import random
import pickle


def generate_daily_obligations_data():
    if db.session.query(DailyObligationsModel).count() == 0:
        for obligation in DailyObligation:
            db.session.add(DailyObligationsModel(obligation.name))
        db.session.commit()
        print(
            "The 'daily_obligations' table has been successfully populated with default obligations.")
    else:
        print("The 'daily_obligations' table is already populated with default entries.")


def selected_session_impact(enum_name):
    match enum_name:
        # Daily Obligations
        case 'JOB_OBLIGATION':
            return 8
        case 'SCHOOL_OBLIGATION':
            return 6
        case 'GYM_OBLIGATION':
            return 4
        case 'PAPERWORK_OBLIGATION':
            return 6
        case 'INDEPENDENT_OBLIGATION':
            return 5
        case 'SOCIAL_OUTINGS_OBLIGATION':
            return 2

        # Fatigue Levels
        case 'VERY_LOW_FATIGUE':
            return 1
        case 'LOW_FATIGUE':
            return 3
        case 'MODERATE_FATIGUE':
            return 5
        case 'HIGH_FATIGUE':
            return 8
        case 'VERY_HIGH_FATIGUE':
            return 10

        # Stress Levels
        case 'VERY_LOW_STRESS':
            return 1
        case 'LOW_STRESS':
            return 3
        case 'MODERATE_STRESS':
            return 5
        case 'HIGH_STRESS':
            return 8
        case 'VERY_HIGH_STRESS':
            return 10


def generate_daily_obligations_for_dataset():
    obligation_types_name = DailyObligation.list()

    obligation_types = []
    for obligation_type_name in obligation_types_name:
        obligation_types.append(selected_session_impact(obligation_type_name))

    count = random.randint(1, len(obligation_types))

    generated_obligations = []
    for _ in range(count):
        generated_obligations.append(random.choice(obligation_types))

    return generated_obligations


def calculate_session_duration(fatigue_level, stress_level, daily_obligations):
    max_session_duration = 240

    fatigue_impact = (fatigue_level / 10) * 90
    stress_impact = (stress_level / 10) * 90
    obligations_impact = 0

    for obligation in daily_obligations:
        obligations_impact += (obligation / 10)
    obligations_impact *= 10

    session_duration = max_session_duration - \
        (fatigue_impact + stress_impact + obligations_impact)

    return max(15, min(session_duration, 240))


def generate_dataset(num_samples):
    data: list[AgentData] = []

    if db.session.query(AgentTrainedDataModel).count() != 0:
        print(
            "The 'agent_trained_data' table is already populated with the agent's training data.")
        return []
    else:
        print("Initiating the generation of 300,000 datasets for the agent. Please wait!")

        for _ in range(num_samples):
            fatigue_name = random.choice(FatigueLevel.list())
            stress_name = random.choice(StressLevel.list())

            fatigue = selected_session_impact(fatigue_name)
            stress = selected_session_impact(stress_name)

            daily_obligations = generate_daily_obligations_for_dataset()
            session_duration = calculate_session_duration(
                fatigue, stress, daily_obligations)

            data.append(AgentData(fatigue, stress, sum(
                daily_obligations), session_duration))

        for data_set in data:
            db.session.add(AgentTrainedDataModel(data_set.fatigue, data_set.stress,
                                                 data_set.daily_obligations, data_set.session_duration))
        db.session.commit()
        print(
            "The 'agent_trained_data' table has been populated with the generated training data.")

        return data


def train_model(data: list[AgentData]):
    if len(data) != 0:
        print('Training the agent on 300,000 datasets has begun. Please wait!')

        model = MLPRegressor(hidden_layer_sizes=(
            10,), max_iter=500, random_state=42)
        X = []
        Y = []

        for data_set in data:
            X.append([data_set.fatigue, data_set.stress,
                      data_set.daily_obligations])
            Y.append(data_set.session_duration)

        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2, random_state=42)

        model.fit(X_train, Y_train)

        with open('trained-model.sav', 'wb') as F:
            pickle.dump(model, F)

        print("The agent has been successfully trained and saved to the file: trained-model.sav")
    else:
        print("Agent training is not required as the dataset is already populated and the agent has been previously trained.")


with app.app_context():
    # Initialize all database tables
    db.create_all()

    # Populate the daily_obligations table with default entries
    generate_daily_obligations_data()

    # Generate a dataset of 300,000 records for the agent
    generated_data = generate_dataset(300000)

    # Train the agent model using the generated dataset
    train_model(generated_data)
