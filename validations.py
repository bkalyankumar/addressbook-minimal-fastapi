# Validate latitude while creating and updating address
def validate_latitude(lat):
    if float(lat) >= -90 and float(lat) <= 90:
        return True
    else: 
        return False

# Validate longitude while creating and updating address
def validate_longitude(lon):
    if float(lon) >= -180 and float(lon) <= 180:
        return True
    else: 
        return False