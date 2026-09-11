from sqlalchemy.orm import Session
from typing import Optional
from app.models.trip import Trip
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.plan import Plan
from app.models.place import Place
from app.schemas.trip import TripResponse
from app.models.itinerary_version import ItineraryVersion

def create_trip_for_user(db: Session, trip_data: TripResponse, user_id: int):
    trip = Trip(
        city=trip_data.city,
        days=trip_data.days,
        user_id=user_id,
    )

    for plan in trip_data.itinerary:
        dp = Plan(day=plan.day)
        for place in plan.places:
            dp.places.append(
                Place(name=place.name, type=place.type)
            )
        trip.plans.append(dp)

    db.add(trip)
    db.commit()
    db.refresh(trip)

    conversation = Conversation(trip_id=trip.id, user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    db.add(Message(
    conversation_id=conversation.id,
    role="user",
    content=f"Plan a {trip.days}-day trip to {trip.city}",
    is_valid_topic=1,
    ))
    db.commit()

    append_assistant_message(
        db=db,
        conversation_id=conversation.id,
        content="Initial itinerary generated.",
        itinerary=[
            {
                "day": plan.day,
                "places": [
                    {
                        "name": place.name,
                        "type": place.type,
                    }
                    for place in plan.places
                ],
            }
            for plan in trip_data.itinerary
        ],
    )
    db.commit()

    return trip, conversation

def get_or_create_conversation(db: Session, trip_id: int, user_id: int):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.trip_id == trip_id, Conversation.user_id == user_id)
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation(trip_id=trip_id, user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def update_trip_itinerary(db: Session, trip: Trip, new_itinerary: list):
    trip.plans.clear()
    db.flush()

    for day_item in new_itinerary:
        dp = Plan(day=day_item["day"])
        for place in day_item["places"]:
            dp.places.append(
                Place(name=place["name"], type=place["type"])
            )
        trip.plans.append(dp)

    db.commit()
    db.refresh(trip)
    return trip

from app.models.itinerary_version import ItineraryVersion


def serialize_itinerary(itinerary):
    return [
        {
            "day": day.day,
            "places": [
                {
                    "name": place.name,
                    "type": place.type,
                }
                for place in day.places
            ],
        }
        for day in itinerary
    ]


def get_next_version_number(db, conversation_id: int) -> int:
    latest_version = (
        db.query(ItineraryVersion)
        .join(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(ItineraryVersion.version_number.desc())
        .first()
    )

    return (
        latest_version.version_number + 1
        if latest_version
        else 1
    )


def append_message(
    db,
    conversation_id: int,
    role: str,
    content: str,
    is_valid_topic: int = 1,
):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        is_valid_topic=is_valid_topic,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def append_assistant_message(
    db,
    conversation_id: int,
    content: str,
    itinerary: list,
    is_valid_topic: int = 1,
):
    message = append_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=content,
        is_valid_topic=is_valid_topic,
    )

    version = ItineraryVersion(
        message_id=message.id,
        version_number=get_next_version_number(
            db,
            conversation_id,
        ),
        itinerary=itinerary,
    )

    db.add(version)
    db.commit()
    db.refresh(message)

    return message