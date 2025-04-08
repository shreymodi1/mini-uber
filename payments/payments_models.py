from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class PaymentRecord(Base):
    """
    Represents a record of a payment made by a user.
    """
    __tablename__ = "payment_records"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount: float = Column(Float, nullable=False)
    status: str = Column(String(50), nullable=False)  # e.g., 'pending', 'completed', 'failed'
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    # TODO: Add foreign key relationship to user if needed
    # user = relationship("User", back_populates="payment_records")

    def __init__(self, user_id: int, amount: float, status: str) -> None:
        """
        Initializes a PaymentRecord instance.

        :param user_id: The ID of the user making the payment.
        :param amount: The amount being paid.
        :param status: The status of the payment.
        """
        self.user_id = user_id
        self.amount = amount
        self.status = status


class FareLog(Base):
    """
    Keeps track of fare-related actions or updates.
    """
    __tablename__ = "fare_logs"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    fare_amount: float = Column(Float, nullable=False)
    description: str = Column(String(255), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    # TODO: Add any additional relationships or constraints

    def __init__(self, user_id: int, fare_amount: float, description: Optional[str] = None) -> None:
        """
        Initializes a FareLog instance.

        :param user_id: The ID of the user associated with the fare.
        :param fare_amount: The amount for the fare.
        :param description: Additional details about the fare.
        """
        self.user_id = user_id
        self.fare_amount = fare_amount
        self.description = description


class PayoutDetail(Base):
    """
    Represents details of a payout made to a user or provider.
    """
    __tablename__ = "payout_details"

    id: int = Column(Integer, primary_key=True, index=True)
    payee_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    payout_amount: float = Column(Float, nullable=False)
    payout_method: str = Column(String(50), nullable=False)  # e.g., 'bank_transfer', 'paypal'
    processed_at: datetime = Column(DateTime, default=datetime.utcnow)

    # TODO: Add foreign key relationship to user if needed
    # payee = relationship("User", back_populates="payout_details")

    def __init__(self, payee_id: int, payout_amount: float, payout_method: str) -> None:
        """
        Initializes a PayoutDetail instance.

        :param payee_id: The ID of the payee receiving the payout.
        :param payout_amount: The amount being paid out.
        :param payout_method: The method used to complete the payout.
        """
        self.payee_id = payee_id
        self.payout_amount = payout_amount
        self.payout_method = payout_method


def create_all_tables(session: Session) -> None:
    """
    Creates all required tables in the database if they do not already exist.

    :param session: A SQLAlchemy Session to access the database engine.
    :return: None
    """
    try:
        Base.metadata.create_all(bind=session.get_bind())
    except SQLAlchemyError as error:
        # TODO: Add proper logging here
        raise error from error