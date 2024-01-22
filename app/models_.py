from sqlalchemy import Column,Integer, String, Date, ForeignKey, Boolean
from datetime import datetime, timedelta

from app.database_ import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    
    hospital_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String, index=True,nullable=False)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    password = Column(String,nullable = False)

class Staff(Base):
    __tablename__ = "staffs"
    
    staff_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=True)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    staff_role = Column(String,nullable=True)
    password = Column(String,nullable = False)

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=False)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)

class Donor(Base):
    __tablename__ = "donors"
    
    donor_id = Column(String, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=False)
    dob = Column(Date,nullable=True)
    address = Column(String,nullable=True)
    phone = Column(String,nullable=True)
    gender = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)

class Repository(Base):
    __tablename__ = "repository"

    blood_group = Column(String,primary_key = True,nullable=False)
    plasma = Column(Integer,nullable=True)
    platelets = Column(Integer,nullable=True)
    rbc = Column(Integer,nullable=True)

class Request(Base):
    __tablename__ = "requests"

    request_id = Column(String, primary_key=True, index=True,nullable=False)
    hospital_id = Column(String, ForeignKey("hospitals.hospital_id"),nullable=True)
    patient_case = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    blood_component = Column(String,nullable=True)
    quantity = Column(Integer,nullable=True)
    status = Column(String,nullable=True)

class Donation(Base):
    __tablename__ = "donations"

    donation_id = Column(String, primary_key=True, index=True,nullable=False)
    donor_id = Column(String,ForeignKey("donors.donor_id"),nullable=False)
    staff_id = Column(String,ForeignKey("staffs.staff_id"),nullable=False)
    donation_occasion = Column(String,nullable=True)
    blood_group = Column(String,nullable=True)
    donation_date = Column(Date,nullable=True)
    result = Column(Boolean,nullable=True)

# class BloodComponents(Base):
#     __tablename__ = "blood_components"

#     packet_id = Column(String, primary_key=True, index=True,nullable=False)
#     component_type = Column(String)
#     blood_group = Column(String,nullable=True)
#     ext_date = Column(Date,default=datetime.today())

#     if component_type == "Plasma":
#         exp_date = Column(Date,default=datetime.today() + timedelta(days=365))
#     elif component_type == "Platelets":
#         exp_date = Column(Date,default=datetime.today() + timedelta(days=5))
#     else:
#         exp_date = Column(Date,default=datetime.today() + timedelta(days=42))