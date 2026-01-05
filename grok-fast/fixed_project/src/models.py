"""Data models for the meeting room booking system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Set


class Priority(Enum):
    """Meeting priority levels."""
    P0_EXECUTIVE = 0  # Board/Executive meetings
    P1_CLIENT = 1     # Client meetings
    P2_CROSS_DEPT = 2 # Cross-department collaboration
    P3_INTERNAL = 3   # Department internal meetings
    P4_CASUAL = 4     # Temporary discussions


class RoomSize(Enum):
    """Room size categories."""
    SMALL = "small"   # 2-6 people
    MEDIUM = "medium" # 7-15 people
    LARGE = "large"   # 16-30 people


class Equipment(Enum):
    """Available equipment types."""
    PROJECTOR = "projector"
    VIDEO_CONF = "video_conference"
    WHITEBOARD = "whiteboard"
    AUDIO = "audio_system"


@dataclass
class MeetingRoom:
    """Represents a meeting room."""
    room_id: str
    name: str
    size: RoomSize
    capacity: int
    equipment: Set[Equipment] = field(default_factory=set)

    def __post_init__(self):
        """Validate capacity matches size category."""
        size_ranges = {
            RoomSize.SMALL: (2, 6),
            RoomSize.MEDIUM: (7, 15),
            RoomSize.LARGE: (16, 30)
        }
        min_cap, max_cap = size_ranges[self.size]
        if not (min_cap <= self.capacity <= max_cap):
            raise ValueError(
                f"Capacity {self.capacity} doesn't match size {self.size.value}"
            )


@dataclass
class Booking:
    """Represents a meeting booking."""
    booking_id: str
    room_id: str
    organizer: str
    start_time: datetime
    end_time: datetime
    attendee_count: int
    priority: Priority
    required_equipment: Set[Equipment] = field(default_factory=set)
    title: str = ""

    def __post_init__(self):
        """Validate booking data."""
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        if self.attendee_count <= 0:
            raise ValueError("Attendee count must be positive")

    def overlaps_with(self, other: 'Booking', buffer_minutes: int = 15) -> bool:
        """
        Check if this booking overlaps with another booking.
        
        Args:
            other: Another booking to check against
            buffer_minutes: Required buffer time in minutes (default: 15)
        
        Returns:
            True if bookings overlap (including buffer time)
        """
        from datetime import timedelta
        
        buffer = timedelta(minutes=buffer_minutes)
        
        # Add buffer time to both bookings
        self_start = self.start_time - buffer
        self_end = self.end_time + buffer
        other_start = other.start_time - buffer
        other_end = other.end_time + buffer
        
        # Check for overlap
        return not (self_end <= other_start or self_start >= other_end)


@dataclass
class BookingRequest:
    """Represents a request to book a meeting room."""
    organizer: str
    start_time: datetime
    end_time: datetime
    attendee_count: int
    priority: Priority
    required_equipment: Set[Equipment] = field(default_factory=set)
    title: str = ""