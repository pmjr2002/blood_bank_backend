from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import app.schemas_ as schemas_,app.models_ as models_, app.utils_ as utils_,app.oauth2_ as oauth2_
from app.database_ import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/auth',response_model=schemas_.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    if user_credentials.username[0] == 'H':
        user = db.query(models_.Hospital).filter(models_.Hospital.hospital_id == user_credentials.username).first()
    else:
        user = db.query(models_.Staff).filter(models_.Staff.staff_id == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    
    if not utils_.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    
    if user_credentials.username[0] == 'H':
        access_token = oauth2_.create_access_token(data={'id':user.hospital_id})
    else:
        access_token = oauth2_.create_access_token(data={'id':user.staff_id})
    
    return {'access_token':access_token,'token_type':'bearer'}