import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db
from datetime import date
from phonenumbers import parse, is_possible_number

router = APIRouter(
    prefix="/donors",
    tags=['Donors'])

@router.get('/', response_model=list[schemas.DonorOut])
def get_donors_by_address_and_blood_group(locality:str = '',blood_group: str = '',name: str = '', db: Session = Depends(get_db)):
    if(blood_group != '' and blood_group[-1] == 'P'):
        blood_group = blood_group[:-1] + '+'
    if locality == '' and blood_group == '' and name == '':
        db_donors = db.query(models.Donor).all()
    elif locality == '' and name == '':
        db_donors = db.query(models.Donor).filter(models.Donor.blood_group == blood_group).all()
    elif blood_group == '' and name == '':
        address = locality + ', Mysuru'
        db_donors = db.query(models.Donor).filter(models.Donor.address == address).all()
    elif locality == '' and blood_group == '':
        db_donors = db.query(models.Donor).filter(models.Donor.name == name).all()
    elif name == '':
        address = locality + ', Mysuru'
        db_donors = db.query(models.Donor).filter(models.Donor.address == address, models.Donor.blood_group == blood_group).all()
    elif locality == '':
        db_donors = db.query(models.Donor).filter(models.Donor.blood_group == blood_group, models.Donor.name == name).all()
    elif blood_group == '':
        address = locality + ', Mysuru'
        db_donors = db.query(models.Donor).filter(models.Donor.address == address, models.Donor.name == name).all()
    
    return db_donors


@router.get('/addresses', response_model=list[str])
def get_donors_addresses():
    addresses = ['Yelwala','Rupanagar','Devraj Mohalla','Tilaknagar','Jayalakshmipuram','Mandi Mohalla','Kuvempunagar','TK Layout','Udaygiri']

    return addresses

@router.post('/', status_code= status.HTTP_201_CREATED)
def create_donor(request: schemas.DonorBase, db: Session = Depends(get_db)):
    db_donor = db.query(models.Donor).filter(models.Donor.name == request.name).first()

    if db_donor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donor with name {request.name} already exists")
    try:
        phone_number = parse(request.phone, "IN")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid phone number")
    if not is_possible_number(phone_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid phone number")

    donor_id = 'D0001'
    db_donor = db.query(models.Donor).order_by(models.Donor.donor_id.desc()).first()
    if db_donor:
        donor_id = 'D' + str(int(db_donor.donor_id[1:]) + 1).zfill(4)
    
    dob = request.dob.split('/') # yyyy/mm/dd
    address = request.address + ', Mysuru'
    new_donor = models.Donor(
    donor_id=donor_id, 
    name=request.name, 
    address = address,
    phone = request.phone,
    dob = date(int(dob[2]),int(dob[1]),int(dob[0])),
    gender = request.gender,
    blood_group = request.blood_group)

    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete('/{donor_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_donor(donor_id: str, db: Session = Depends(get_db)):
    db_donor = db.query(models.Donor).filter(models.Donor.donor_id == donor_id).first()
    if not db_donor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donor with id {donor_id} not found")
    db.delete(db_donor)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)