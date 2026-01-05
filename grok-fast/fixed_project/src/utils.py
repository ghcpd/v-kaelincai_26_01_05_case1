"""Utility functions for the booking system."""

from datetime import datetime, time
from src.models import RoomSize, Priority


def is_lunch_time(dt: datetime) -> bool:
    """
    Check if a datetime falls within lunch time (12:00-13:30).
    
    Args:
        dt: Datetime to check
    
    Returns:
        True if within lunch time
    """
    lunch_start = time(12, 0)
    lunch_end = time(13, 30)
    return lunch_start <= dt.time() < lunch_end


def check_capacity_fit(attendee_count: int, room_capacity: int, room_size: RoomSize) -> tuple[bool, str]:
    """
    Check if attendee count fits room capacity (60%-90% utilization).
    
    Args:
        attendee_count: Number of attendees
        room_capacity: Room capacity
        room_size: Size category of the room
    
    Returns:
        Tuple of (is_valid, reason)
    """
    min_utilization = 0.6
    max_utilization = 0.9
    
    min_attendees = int(room_capacity * min_utilization)
    max_attendees = int(room_capacity * max_utilization)
    
    if attendee_count < min_attendees:
        return False, f"Room underutilized ({attendee_count}/{room_capacity})"
    elif attendee_count > max_attendees:
        return False, f"Room over capacity ({attendee_count}/{room_capacity})"
    else:
        return True, "Capacity fits well"


def can_book_during_lunch(priority: Priority) -> bool:
    """
    Check if a meeting priority allows booking during lunch time.
    
    Args:
        priority: Meeting priority level
    
    Returns:
        True if allowed to book during lunch
    """
    return priority in [Priority.P0_EXECUTIVE, Priority.P1_CLIENT]


def is_time_slot_valid(start_time: datetime, end_time: datetime) -> tuple[bool, str]:
    """
    Validate time slot follows 30-minute increment rule.
    
    Args:
        start_time: Start time
        end_time: End time
    
    Returns:
        Tuple of (is_valid, reason)
    """
    # Check if times are on 30-minute boundaries
    if start_time.minute not in [0, 30] or end_time.minute not in [0, 30]:
        return False, "Time slots must be on 30-minute boundaries (00 or 30)"
    
    # Check if duration is in 30-minute increments
    duration_minutes = (end_time - start_time).total_seconds() / 60
    if duration_minutes % 30 != 0:
        return False, "Duration must be in 30-minute increments"
    
    return True, "Time slot valid"