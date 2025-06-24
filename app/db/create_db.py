import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from app.db.models import Base

# Use SQLite for local development (creates srx_local.db in your project root)
DATABASE_URL = "sqlite:///srx_local.db"

engine = create_engine(DATABASE_URL, echo=True)

# This will create tables if they do not exist, and will NOT drop existing data
Base.metadata.create_all(engine)

print("Database and tables created (if not already present).")