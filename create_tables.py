from database.db_connection import engine, Base
from database import models

Base.metadata.create_all(bind=engine)

print("All Database Tables Created Successfully!")