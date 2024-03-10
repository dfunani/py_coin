"""_summary_"""
from models import ENGINE
from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from models.user.users import User

def main():
    with Session(ENGINE) as session:
        try:
            user = User('dfunani@test13.com', 'password1@12345')
            session.add(user)
            session.commit()
        except (UniqueViolation, IntegrityError) as error:
            print(str(error))
        
if __name__ == "__main__":
    main()
