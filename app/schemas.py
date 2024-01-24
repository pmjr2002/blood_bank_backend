from pydantic import BaseModel, EmailStr
from datetime import date

class HospitalBase(BaseModel):
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True

class HospitalIn(HospitalBase):
    password: str

class HospitalOut(HospitalBase):
    hospital_id: str

class StaffBase(BaseModel):
    name: str
    dob: date
    address: str
    phone: str
    staff_role: str
    gender: str
    blood_group: str

    class Config:
        orm_mode = True

class StaffOut(StaffBase):
    staff_id: str


class StaffIn(StaffBase):
    password: str


class Patient(BaseModel):
    patient_id: int
    name: str
    dob: str
    address: str
    phone: str

class Repository(BaseModel):
    blood_id: int
    blood_group: str
    plasma: int
    platelets: int
    rbc: int

class DonationsBase(BaseModel):
    donor_id: str
    staff_id: str
    donation_occasion: str
    blood_group: str
    result: str

    class Config:
        orm_mode = True

class Donations(DonationsBase):
    donation_date: str
    donation_id: str

class RequestBase(BaseModel):
    hospital_id: str
    patient_case: str
    blood_group: str
    blood_component: str
    quantity: int


    class Config:
        orm_mode = True

class Request(RequestBase):
    request_id: str
    status: str

class DonorBase(BaseModel):
    name: str
    gender: str
    dob: str
    blood_group: str
    phone:str
    address: str

    class Config:
        orm_mode = True

class DonorOut(DonorBase):
    donor_id: str
    dob: date

class BloodComponentBase(BaseModel):
    component_type:str
    blood_group: str
    ext_date: str
    exp_date: str

    class Config:
        orm_mode = True

class BloodComponentIn(BloodComponentBase):
    packet_id: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr