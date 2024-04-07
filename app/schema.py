from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR, INT, DateTime
from app.database import Base


class Members(Base):
    __tablename__ = "Members"
    memberId = Column(INT, primary_key=True, nullable = False)
    memberName = Column(VARCHAR(45), nullable = False)
    memberEmail = Column(VARCHAR(45), nullable = False)
    CIRCULATIONHISTORY = relationship("CirculationHistory", uselist=True, backref="Members")


class Books(Base):
    __tablename__ = "Books"
    bookId     = Column(INT, primary_key=True, nullable = False)
    bookName = Column(VARCHAR(45), nullable = False)
    numberOfCopies = Column(INT)
    remainingCopies = Column(INT)
    CIRCULATIONHISTORY = relationship("CirculationHistory", uselist=True    , backref="Books")
    

class CirculationHistory(Base):
    __tablename__ = "CirculationHistory"
    id              =  Column(INT, primary_key=True, nullable = False, autoincrement = True)
    bookId          = Column(ForeignKey("Books.bookId"))
    memberId        = Column(ForeignKey("Members.memberId"))
    issuedDate      = Column(DateTime)
    returnedDate    = Column(DateTime)
    status          = Column(VARCHAR(45))

class ReservationQueue(Base):
    __tablename__ = "ReservationQueue"
    id              =  Column(INT, primary_key=True, nullable = False, autoincrement = True)
    bookId          = Column(ForeignKey("Books.bookId"))
    memberId        = Column(ForeignKey("Members.memberId"))
    reservationTime = Column(DateTime)
    status          = Column(VARCHAR(45))
