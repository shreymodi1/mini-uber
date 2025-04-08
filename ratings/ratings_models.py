"""
Module for storing ratings and reviews for the application.

This module contains:
    - Pydantic model definitions for ratings and reviews data validation.
    - SQLAlchemy ORM models for persisting ratings and reviews in the database.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RatingBase(BaseModel):
    """
    Pydantic base class for ratings.
    Defines shared fields and validation logic.
    """

    rating_value: conint(ge=1, le=5) = Field(
        ...,
        description="Value of the rating on a scale of 1 (lowest) to 5 (highest)."
    )
    review_text: Optional[str] = Field(
        None,
        description="Optional text review accompanying the rating."
    )


class RatingCreate(RatingBase):
    """
    Pydantic model for creating a new rating.
    Extends RatingBase with fields needed at creation (if any).
    """
    reviewer_id: Optional[int] = Field(
        None,
        description="Identifier for the user posting the rating."
    )


class RatingInDB(RatingBase):
    """
    Pydantic model representing a rating as stored in the database.
    Extends RatingBase with ID and timestamp.
    """

    id: int
    timestamp: datetime


class RatingORM(Base):
    """
    SQLAlchemy ORM model for ratings.
    Maps Python objects to database records in the 'ratings' table.
    """

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating_value = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # TODO: Define relationship to User if needed in the future
    reviewer = relationship("User", back_populates="ratings", lazy="joined", uselist=False)

    # TODO: Add error handling or custom validation if necessary for complex logic


class ReviewBase(BaseModel):
    """
    Pydantic base class for reviews.
    Defines shared fields and validation logic.
    """

    title: str = Field(..., description="Title of the review.")
    content: Optional[str] = Field(None, description="Main text of the review.")


class ReviewCreate(ReviewBase):
    """
    Pydantic model for creating a new review.
    Extends ReviewBase with fields needed at creation (if any).
    """
    reviewer_id: Optional[int] = Field(
        None,
        description="Identifier for the user posting the review."
    )


class ReviewInDB(ReviewBase):
    """
    Pydantic model representing a review as stored in the database.
    Extends ReviewBase with ID and timestamp.
    """

    id: int
    timestamp: datetime


class ReviewORM(Base):
    """
    SQLAlchemy ORM model for reviews.
    Maps Python objects to database records in the 'reviews' table.
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # TODO: Define relationship to User if needed in the future
    reviewer = relationship("User", back_populates="reviews", lazy="joined", uselist=False)

    # TODO: Add error handling or custom validation if necessary for complex logic

    # TODO: Implement methods for CRUD operations if required in future development