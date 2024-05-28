from datetime import datetime, timedelta
from jose import JWTError,jwt

#SECRET KEY
#ALGORITHIM
#EXPIRATION TIME

SECRET_KEY= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ2YWx1ZSJ9.FG-8UppwHaFp1LgRYQQeS6EDQF7_6-bMFegNucHjmWg"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


def create_access_token(data:dict):  #token will have a payload so it will be stored in data variable
    to_encode=data.copy()
    expire= datetime.now()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


    print("noooooo")

    return token