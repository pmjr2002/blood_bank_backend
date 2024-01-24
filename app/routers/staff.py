import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db
from datetime import date

router = APIRouter(
    prefix="/staff",
    tags=['Staff'])

@router.get('/', response_model=list[schemas.StaffOut])
def get_staffs(db: Session = Depends(get_db)):
    db_staffs = db.query(models.Staff).all()
    return db_staffs

@router.get('/{staff_id}', response_model=schemas.StaffOut)
def get_staff(staff_id: str, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.staff_id == staff_id).first()
    if not db_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Staff with ID {staff_id} not found")
    return db_staff

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_staff(request: schemas.StaffIn, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.name == request.name).first()
    
    if db_staff:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Staff with name {request.name} already exists")

    staff_id = 'ST0001'
    db_staff = db.query(models.Staff).order_by(models.Staff.staff_id.desc()).first()
    if db_staff:
        staff_id = 'ST' + str(int(db_staff.staff_id[2:]) + 1).zfill(4)
    
    dob = str(request.dob).split('-') # yyyy-mm-dd

    new_staff = models.Staff(
    staff_id=staff_id, 
    name=request.name, 
    address = request.address,
    phone = request.phone,
    staff_role = request.staff_role,
    blood_group = request.blood_group,
    gender = request.gender,
    dob = date(day=int(dob[2]),month=int(dob[1]),year=int(dob[0])),
    password=utils.hash(request.password))
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return Response(status_code=status.HTTP_201_CREATED)