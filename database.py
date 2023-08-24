from sqlalchemy import create_engine, Column, String, Integer, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv


db_url = os.getenv(DB_STRING)
engine = create_engine(db_url)

Base = declarative_base()

class WFHApplications(Base):
    __tablename__ = 'wfh_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(255))
    emp_id = Column(String(10))
    wfh_date = Column(Date)
    application_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    status = Column(String(20))
    approval_date = Column(TIMESTAMP)

Session = sessionmaker(bind=engine)

def insert_wfh_application(employee_name, emp_id, wfh_date):
    session = Session()

    application = WFHApplications(
        employee_name=employee_name,
        emp_id=emp_id,
        wfh_date=wfh_date,
        status='pending'
    )

    session.add(application)
    session.commit()
    session.close()
