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
            "'daily_obligations' table has been populated with default daily obligations.")
    else:
        print("'daily_obligations' table has already been populated with default data.")


def generate_daily_obligations_for_dataset():
    obligation_types = DailyObligation.list()
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
    obligations_impact *= 20

    session_duration = max_session_duration - \
        (fatigue_impact + stress_impact + obligations_impact)

    return max(15, min(session_duration, 180))


def generate_dataset(num_samples):
    data: list[AgentData] = []

    for _ in range(num_samples):
        fatigue = random.choice(FatigueLevel.list())
        stress = random.choice(StressLevel.list())
        daily_obligations = generate_daily_obligations_for_dataset()
        session_duration = calculate_session_duration(
            fatigue, stress, daily_obligations)

        data.append(AgentData(fatigue, stress, sum(
            daily_obligations), session_duration))

    print("Starting to create 300.000 datasets for an agent. Please wait!")

    if db.session.query(AgentTrainedDataModel).count() == 0:
        for data_set in data:
            db.session.add(AgentTrainedDataModel(data_set.fatigue, data_set.stress,
                           data_set.daily_obligations, data_set.session_duration))
        db.session.commit()
        print(
            "'agent_trained_data' table has been populated with trained data for an agent")
    else:
        print(
            "'daily_obligations' table has already been populated with agent trained data.")

    return data


def train_model(data: list[AgentData]):
    print('Training Agent on 300.000 Datasets has started. Please wait!')

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

    print("Agent has been successfully trained and saved in a file named: trained-model.sav")


with app.app_context():
    # Creating all tables
    db.create_all()

    # # Populating daily_obligations table with default data.
    generate_daily_obligations_data()

    # Creating Agent Dataset
    generated_data = generate_dataset(300000)

    # Training agent model
    train_model(generated_data)
