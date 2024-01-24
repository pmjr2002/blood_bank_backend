import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db

router = APIRouter(
    prefix="/hospital",
    tags=['Hospitals'])

@router.get('/', response_model=list[schemas.HospitalOut])
def get_hospitals(db: Session = Depends(get_db)):
    db_hospitals = db.query(models.Hospital).all()
    return db_hospitals


@router.get('/{hospital_id}', response_model=schemas.HospitalOut)
def get_hospital(hospital_id: str, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(models.Hospital.hospital_id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with ID {hospital_id} not found")
    return db_hospital


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_hospital(request: schemas.HospitalIn, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(models.Hospital.name == request.name).first()
    
    if db_hospital:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with name {request.name} already exists")

    db_hospital = db.query(models.Hospital).order_by(models.Hospital.hospital_id.desc()).first()

    hospital_id = 'H001'
    if db_hospital:
        hospital_id = 'H' + str(int(db_hospital.hospital_id[1:]) + 1).zfill(3)
        

    new_hospital = models.Hospital(
    hospital_id=hospital_id, 
    name=request.name, 
    address = request.address,
    phone = request.phone,
    password=utils.hash(request.password))
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete('/{hospital_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital(hospital_id: str, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(models.Hospital.hospital_id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with ID {hospital_id} not found")
    db.delete(db_hospital)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)