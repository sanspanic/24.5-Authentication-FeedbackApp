from models import User, Feedback, db
from app import app

def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()

#create all tables
drop_everything()
#db.drop_all()
db.create_all()

#if table isn't empty, empty it
User.query.delete() 

#add users
cat = User.register('cat', 'meow', 'cat@meow.com', 'Cat', 'Meow')
dog = User.register('dog', 'woof', 'dog@woof.com', 'Dog', 'Woof')
pig = User.register('pig', 'oink', 'pig@oink.com', 'Pig', 'Oink')

#add new objects to session, so they persist & commit
db.session.add_all([cat, dog, pig])
db.session.commit()

f1 = Feedback(title='Meow', content='Meow meow meow meoooow', username='cat')
f2 = Feedback(title='Meow meow', content='Meow meow meow meoooow', username='cat')
f3 = Feedback(title='Meow meow meow', content='Meow meow meow meoooow, and also meow', username='cat')
f4 = Feedback(title='Woof', content='Woof woof woof', username='dog')
f5 = Feedback(title='Oink', content='Oinky oink oink oink oink.', username='pig')

db.session.add_all([f1, f2, f3, f4, f5])
db.session.commit()




