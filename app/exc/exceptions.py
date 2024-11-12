from fastapi import HTTPException, status


class BookingException(HTTPException):
    
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    
    def __init__(self):
        super().__init__(self.status_code, self.detail)
        
class UserAlreadyExistException(BookingException):
    
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"
    
class IncorrectEmailOrPassword(BookingException):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"
    
class TokenExpiredException(BookingException):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"
    
class TokenAbsentException(BookingException):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"
    
class IncorrectFormatTokenException(BookingException):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"
    
class UserIsNotPresentException(BookingException):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    
class RoomCannotBeBooked(BookingException):
    
    status_code = status.HTTP_409_CONFLICT
    detail = "There are no available rooms left"
    
class HotelNotFound(BookingException):
    
    status_code = status.HTTP_409_CONFLICT
    detail = "Hotel not found"
    
class DateFromCannotBeAfterDateTo(BookingException):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Date from must be less then date to"

class CannotBookHotelForLongPeriod(BookingException):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Cannot book hotel longer then 30 days"
    
class CannotAddDataToDatabase(BookingException):
    
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Cannot add data to database"
    
class CannotProcessCSV(BookingException):
    
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Cannot process csv to database format"