import app.schemas_ as schemas_, app.models_ as models_, app.utils_ as utils_, app.oauth2_ as oauth2_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database_ import get_db

router = APIRouter(
    prefix="/requests",
    tags=['Requests'])

@router.get('/blood_rate',response_model=dict())
def get_blood_rate():
    blood_rate = dict()
    blood_rate['platelets'] = 400
    blood_rate['plasma'] = 400
    blood_rate['RBC'] = 1450
    blood_rate['whole_blood'] = 1450
    return blood_rate

# Pending Request

@router.get('/pending_request_process/{request_id}', response_model=list[schemas_.Request])
def process_request_by_ID(db: Session = Depends(get_db), request_id: str = None):
    request = db.query(models_.Request).filter(models_.Request.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Request not found")
    
    return Response(status_code = status.HTTP_200_OK, content = f"Blood request {request.request_id} processed successfully") if process_blood(request,db) else Response(status_code = status.HTTP_400_BAD_REQUEST, content = f"Blood request {request.request_id} could not be processed")

@router.get('/pending_request/')
def get_pending_requests(db: Session = Depends(get_db)):
    requests = db.query(models_.Request).filter(models_.Request.status == 'Pending').all()
    return requests

@router.get('/pending_request/{hospital_id}/', response_model=list[schemas_.Request])
def get_pending_requests_by_hospital_ID(hospital_id: str,db: Session = Depends(get_db)):
    requests = db.query(models_.Request).filter(models_.Request.hospital_id == hospital_id).filter(models_.Request.status == 'Pending').all()
    return requests

# Successful Request

@router.get('/successful_request/{hospital_id}/', response_model=list[schemas_.Request])
def get_successful_requests(hospital_id: str,db: Session = Depends(get_db)):
    requests = db.query(models_.Request).filter(models_.Request.hospital_id == hospital_id).filter(models_.Request.status == 'Success').all()
    return requests

@router.get('/{hospital_id}', response_model=list[schemas_.Request])
def get_requests_by_hospital_id(hospital_id: str, db: Session = Depends(get_db)):
    requests = db.query(models_.Request).filter(models_.Request.hospital_id == hospital_id).all()
    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Requests not found")
    return requests

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_request(request: schemas_.RequestBase, db: Session = Depends(get_db)):
    db_request = db.query(models_.Hospital).filter(models_.Hospital.hospital_id == request.hospital_id).first()

    if not db_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with ID {request.hospital_id} does not exist")

    request_id = generate_id(request.blood_group, db)

    db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == request.blood_group)
    
    req_status = 'Success'
    if request.blood_component == 'Platelets' and db_blood.first().platelets < request.quantity:
            req_status = 'Pending'
    
    if request.blood_component == 'Plasma' and db_blood.first().plasma < request.quantity:
            req_status = 'Pending'

    if request.blood_component == 'Power Red' and db_blood.first().rbc < request.quantity:
            req_status = 'Pending'
    
    if request.blood_component == 'Whole Blood' and (db_blood.first().platelets < request.quantity or db_blood.first().plasma < request.quantity or db_blood.first().rbc < request.quantity):
            req_status = 'Pending'
    
    new_request = models_.Request(
        request_id=request_id, 
        hospital_id=request.hospital_id,
        patient_case=request.patient_case,
        blood_group=request.blood_group, 
        blood_component=request.blood_component,
        quantity=request.quantity,
        status = req_status)

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    
    return Response(status_code=status.HTTP_201_CREATED,content=f"Request {request_id} created successfully") if process_blood(new_request,db) else Response(status_code=status.HTTP_404_NOT_FOUND,content=f"Request {request_id} could not be processed")
    

def generate_id(blood_group: str,db: Session):
    if blood_group == 'A+':
        request_id = 'RAP001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RAP')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RAP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'A-':
        request_id = 'RAN001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RAN')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RAN' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'B+':
        request_id = 'RBP001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RBP')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RBP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'B-':
        request_id = 'RBN001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RBN')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RBN' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    elif blood_group == 'AB+':
        request_id = 'RABP001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RABP')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RABP' + str(int(db_request.request_id[4:]) + 1).zfill(3)
    elif blood_group == 'AB-':
        request_id = 'RABN001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RABN')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RABN' + str(int(db_request.request_id[4:]) + 1).zfill(3)
    elif blood_group == 'O+':
        request_id = 'ROP001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('ROP')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'ROP' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    else:
        request_id = 'RON001'
        db_request = db.query(models_.Request).filter(models_.Request.request_id.startswith('RON')).order_by(models_.Request.request_id.desc()).first()
        if db_request:
            request_id = 'RON' + str(int(db_request.request_id[3:]) + 1).zfill(3)
    return request_id

def process_blood(request: str, db: Session):
    db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == request.blood_group)
    if db_blood is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blood group not found")
    
    blood_receive_group = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'AB-': ['A-', 'B-', 'AB-', 'O-'],
        'O+': ['O+', 'O-'],
        'O-': ['O-']
    }

    if request.blood_component == 'Platelets':
        for blood_group in blood_receive_group[request.blood_group]:
            db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == blood_group).first()
            if db_blood.platelets >= request.quantity:
                db_blood.platelets -= request.quantity

                request.status = 'Success'
                db.commit()
                db.refresh(request)
                return True

    elif request.blood_component == 'Plasma':
        for blood_group in blood_receive_group[request.blood_group]:
            db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == blood_group).first()
            if db_blood.plasma >= request.quantity:
                db_blood.plasma -= request.quantity

                request.status = 'Success'
                db.commit()
                db.refresh(request)
                return True

    elif request.blood_component == 'Power Red':
        for blood_group in blood_receive_group[request.blood_group]:
            db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == blood_group).first()
            if db_blood.rbc >= request.quantity:
                db_blood.rbc -= request.quantity

                request.status = 'Success'
                db.commit()
                db.refresh(request)
                return True
    else:
        for blood_group in blood_receive_group[request.blood_group]:
            db_blood = db.query(models_.Repository).filter(models_.Repository.blood_group == blood_group).first()
            if db_blood.platelets >= request.quantity and db_blood.plasma >= request.quantity and db_blood.rbc >= request.quantity:
                db_blood.platelets -= request.quantity
                db_blood.plasma -= request.quantity
                db_blood.rbc -= request.quantity
                
                request.status = 'Success'
                db.commit()
                db.refresh(request)
                return True

    return False