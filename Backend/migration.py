from main import app, db, DailyObligationsModel
from models import DailyObligation


with app.app_context():
    db.create_all()
    print("Tables have been created successfully.")

    # Populating daily_obligations table with default data.
    if db.session.query(DailyObligationsModel).count() == 0:
        for obligation in DailyObligation:
            db.session.add(DailyObligationsModel(
                daily_obligation_type=obligation.name))
        db.session.commit()
        print(
            "'daily_obligations' table has been populated with default daily obligations.")
    else:
        print("'daily_obligations' table has already been populated with default data.")
