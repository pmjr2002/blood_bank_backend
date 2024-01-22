import app.schemas_ as schemas_, app.models_ as models_, app.utils_ as utils_, app.oauth2_ as oauth2_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database_ import get_db

router = APIRouter(
    prefix="/hospital",
    tags=['Hospitals'])

@router.get('/', response_model=list[schemas_.HospitalOut])
def get_hospitals(db: Session = Depends(get_db)):
    db_hospitals = db.query(models_.Hospital).all()
    return db_hospitals


@router.get('/{hospital_id}', response_model=schemas_.HospitalOut)
def get_hospital(hospital_id: str, db: Session = Depends(get_db)):
    db_hospital = db.query(models_.Hospital).filter(models_.Hospital.hospital_id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with ID {hospital_id} not found")
    return db_hospital


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_hospital(request: schemas_.HospitalIn, db: Session = Depends(get_db)):
    db_hospital = db.query(models_.Hospital).filter(models_.Hospital.name == request.name).first()
    
    if db_hospital:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with name {request.name} already exists")

    db_hospital = db.query(models_.Hospital).order_by(models_.Hospital.hospital_id.desc()).first()

    hospital_id = 'H001'
    if db_hospital:
        hospital_id = 'H' + str(int(db_hospital.hospital_id[1:]) + 1).zfill(3)
        

    new_hospital = models_.Hospital(
    hospital_id=hospital_id, 
    name=request.name, 
    address = request.address,
    phone = request.phone,
    password=utils_.hash(request.password))
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete('/{hospital_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital(hospital_id: str, db: Session = Depends(get_db)):
    db_hospital = db.query(models_.Hospital).filter(models_.Hospital.hospital_id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with ID {hospital_id} not found")
    db.delete(db_hospital)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)