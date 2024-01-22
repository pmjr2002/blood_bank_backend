import app.schemas_ as schemas_, app.models_ as models_, app.utils_ as utils_, app.oauth2_ as oauth2_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database_ import get_db
from datetime import date

router = APIRouter(
    prefix="/staff",
    tags=['Staff'])

@router.get('/', response_model=list[schemas_.StaffOut])
def get_staffs(db: Session = Depends(get_db)):
    db_staffs = db.query(models_.Staff).all()
    return db_staffs

@router.get('/{staff_id}', response_model=schemas_.StaffOut)
def get_staff(staff_id: str, db: Session = Depends(get_db)):
    db_staff = db.query(models_.Staff).filter(models_.Staff.staff_id == staff_id).first()
    if not db_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Staff with ID {staff_id} not found")
    return db_staff

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_staff(request: schemas_.StaffIn, db: Session = Depends(get_db)):
    db_staff = db.query(models_.Staff).filter(models_.Staff.name == request.name).first()
    
    if db_staff:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Staff with name {request.name} already exists")

    staff_id = 'ST0001'
    db_staff = db.query(models_.Staff).order_by(models_.Staff.staff_id.desc()).first()
    if db_staff:
        staff_id = 'ST' + str(int(db_staff.staff_id[2:]) + 1).zfill(4)
    
    dob = request.dob.split('/') # yyyy/mm/dd

    new_staff = models_.Staff(
    staff_id=staff_id, 
    name=request.name, 
    address = request.address,
    phone = request.phone,
    staff_role = request.staff_role,
    blood_group = request.blood_group,
    gender = request.gender,
    dob = date(day=int(dob[2]),month=int(dob[1]),year=int(dob[0])),
    password=utils_.hash(request.password))
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return Response(status_code=status.HTTP_201_CREATED)