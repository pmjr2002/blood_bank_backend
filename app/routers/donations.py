import app.schemas_ as schemas_, app.models_ as models_, app.utils_ as utils_, app.oauth2_ as oauth2_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database_ import get_db
from datetime import date

router = APIRouter(
    prefix="/donations",
    tags=['Donations'])


@router.get('/', response_model=list[schemas_.Donations])
def get_donations(db: Session = Depends(get_db)):
    db_donations = db.query(models_.Donation).all()
    return db_donations


@router.get('/{donation_id}', response_model=schemas_.Donations)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    db_donation = db.query(models_.Donation).filter(models_.Donation.donation_id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"donation with ID {donation_id} not found")
    return db_donation

@router.post('/')
def create_donation(request: schemas_.DonationsBase, db: Session = Depends(get_db)):
    donation_id = 'DON0001'

    db_donation = db.query(models_.Donation).order_by(models_.Donation.donation_id.desc()).first()
    if db_donation:
        donation_id = 'DON' + str(int(db_donation.donation_id[3:]) + 1).zfill(4)
    
    result = True if request.result == 'Positive' else False

    db_donor = db.query(models_.Donor).filter(models_.Donor.donor_id == request.donor_id).first()

    if db_donor.blood_group != request.blood_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donor's blood group {db_donor.blood_group} does not match with the blood group {request.blood_group} of the donation")

    new_donation = models_.Donation(
        donation_id=donation_id, 
        donor_id=request.donor_id, 
        staff_id=request.staff_id,
        donation_occasion=request.donation_occasion,
        blood_group=request.blood_group,
        result =result,
        donation_date=date.today())
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    if result:
        db_repository = db.query(models_.Repository).filter(models_.Repository.blood_group == request.blood_group)
        
        if not db_repository.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Blood group {request.blood_group} not available")

        db_repository.first().platelets += 1
        db_repository.first().plasma += 1
        db_repository.first().rbc += 1
        db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

