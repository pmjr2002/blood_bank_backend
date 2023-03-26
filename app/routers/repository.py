import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db

router = APIRouter(
    prefix="/repository",
    tags=['Repository'])

@router.get('/initialize', response_model=list[schemas.Repository])
def repository_initialize(db: Session = Depends(get_db)):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

    for blood_group in blood_groups:
        new_repository = models.Repository(blood_group=blood_group,plasma=0,platelets=0,rbc=0)

        db.add(new_repository)
        db.commit()
        db.refresh(new_repository)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get('/')
def get_repository(db: Session = Depends(get_db)):
    repository = db.query(models.Repository).all()
    return repository