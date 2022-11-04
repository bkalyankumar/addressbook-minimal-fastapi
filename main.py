import random
import string
import time
from fastapi import FastAPI, Depends, Request
import schemas
import models
import logging
from validations import *
from database import engine, SessionLocal
from sqlalchemy.orm import session
import geopy.distance

# Setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# Get root logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Address Book API",
    description="Adds, Updates, Deletes addresses.",
    version="1.0",
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

# Get all addresses in the database
@app.get('/addressbook/api/v1/')
def get_all(db: session = Depends(get_db)):
    logger.info("logging from the get all addresses def")
    addresses = db.query(models.Address).all()
    return addresses


# Create a new address in the database
@app.post('/addressbook/api/v1/')
def create(request: schemas.Address, db: session = Depends(get_db)):
    logger.info("logging from the create new address def")
    if not validate_latitude(request.latitude):
        return f"Invalid Latitude! {request.latitude} please check..."

    if not validate_longitude(request.longitude):
        return f"Invalid Longitude! {request.longitude} please heck"

    new_address = models.Address(name=request.name, city=request.city, 
                                 state=request.state, pincode=request.pincode,
                                 latitude=request.latitude, longitude=request.longitude)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


# Get a single address from database using id
@app.get('/addressbook/api/v1/{id}')
def get_address_by_id(db: session = Depends(get_db), id: int = None):
    logger.info("logging from the get address by id def")
    address = db.query(models.Address).filter(models.Address.id == id).first()

    if address:
        return address
    else:
        return f"No available address found with id: {id}"


# Update the coordinates of an address stored in the database
@app.put('/addressbook/api/v1/{id}')
def update_address(request: schemas.Address, db: session = Depends(get_db), id: int = None):
    logger.info("logging from the update address def")
    if not validate_latitude(request.latitude):
        return f"Invalid Latitude! {request.latitude} please check..."

    if not validate_longitude(request.longitude):
        return f"Invalid Longitude! {request.longitude} please check..."

    address = db.query(models.Address).filter(models.Address.id == id).first()
    address.latitude = request.latitude
    address.longitude = request.longitude
    db.commit()
    db.refresh(address)
    return address


# Delete an address from the database
@app.delete('/addressbook/api/v1/{id}')
def delete_address(db: session = Depends(get_db), id: int = None):
    logger.info("logging from the delete address def")
    address = db.query(models.Address).filter(models.Address.id == id).first()
    
    if address:
        db.delete(address)
        db.commit()
        return "Address Deleted Successfully"
    else:
        return f"No address found with id: {id}"


# Get distance between two coordinates
def calculate_distance(latitude1, latitude2, longitude1, longitude2):
    logger.info("logging from the calculate distance def")
    coordinates_1 = (latitude1, longitude1)
    coordinates_2 = (latitude2, longitude2)
    return geopy.distance.geodesic(coordinates_1, coordinates_2).km
        

# Return addresses in the database to a given coordinates within a given distance in Km
@app.post('/addressbook/api/v1')
def get_address_by_coordinates(lat: float, lon: float, dis: float, db: session = Depends(get_db)):
    logger.info("logging from the get address by coodinates def")
    addresses = db.query(models.Address).all()
    address_list = []
    for address in addresses:
        distance = calculate_distance(lat, float(address.latitude), lon, float(address.longitude))
        if distance < dis:
            address_list.append(address)

    return address_list