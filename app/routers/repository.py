import app.schemas_ as schemas_, app.models_ as models_, app.utils_ as utils_, app.oauth2_ as oauth2_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database_ import get_db

router = APIRouter(
    prefix="/repository",
    tags=['Repository'])

@router.get('/initialize', response_model=list[schemas_.Repository])
def repository_initialize(db: Session = Depends(get_db)):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

    for blood_group in blood_groups:
        new_repository = models_.Repository(blood_group=blood_group,plasma=0,platelets=0,rbc=0)

        db.add(new_repository)
        db.commit()
        db.refresh(new_repository)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get('/')
def get_repository(db: Session = Depends(get_db)):
    repository = db.query(models_.Repository).all()
    return repository