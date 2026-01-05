"""
Meeting Room Booking System - Core booking logic.

This module contains the main booking system with the equipment validation bug FIXED.
"""

from datetime import datetime
from typing import List, Optional, Dict, Set
from src.models import (
    MeetingRoom, Booking, BookingRequest, Priority, Equipment, RoomSize
)
from src.utils import (
    check_capacity_fit, is_lunch_time, can_book_during_lunch, is_time_slot_valid
)


class BookingResult:
    """Result of a booking attempt."""
    
    def __init__(self, success: bool, message: str, booking: Optional[Booking] = None,
                 conflicting_bookings: Optional[List[Booking]] = None):
        self.success = success
        self.message = message
        self.booking = booking
        self.conflicting_bookings = conflicting_bookings or []


class MeetingRoomBookingSystem:
    """Main booking system that manages meeting room reservations."""
    
    def __init__(self):
        self.rooms: Dict[str, MeetingRoom] = {}
        self.bookings: List[Booking] = []
        self._next_booking_id = 1
    
    def add_room(self, room: MeetingRoom) -> None:
        """Add a meeting room to the system."""
        self.rooms[room.room_id] = room
    
    def add_booking(self, booking: Booking) -> None:
        """Add a booking directly (for initial setup/testing)."""
        self.bookings.append(booking)
    
    def get_room(self, room_id: str) -> Optional[MeetingRoom]:
        """Get a room by ID."""
        return self.rooms.get(room_id)
    
    def get_bookings_for_room(self, room_id: str) -> List[Booking]:
        """Get all bookings for a specific room."""
        return [b for b in self.bookings if b.room_id == room_id]
    
    def _check_room_availability(self, room_id: str, request: BookingRequest) -> tuple[bool, str, List[Booking]]:
        """
        Check if a room is available for the requested time slot.
        
        Returns:
            Tuple of (is_available, reason, conflicting_bookings)
        """
        room_bookings = self.get_bookings_for_room(room_id)
        
        conflicting = []
        for booking in room_bookings:
            if booking.overlaps_with(request):
                conflicting.append(booking)
        
        if conflicting:
            # Check if we can bump lower priority bookings
            can_bump = all(request.priority.value < b.priority.value for b in conflicting)
            if can_bump:
                # Remove conflicting bookings
                for booking in conflicting:
                    self.bookings.remove(booking)
                return True, "Conflicting lower priority bookings removed", []
            else:
                return False, "Room unavailable - higher or equal priority booking exists", conflicting
        
        return True, "Room available", []
    
    def _validate_equipment_requirements(self, room: MeetingRoom, 
                                        required_equipment: Set[Equipment]) -> tuple[bool, str]:
        """
        Validate that room has all required equipment.
        
        ✅ FIXED: Now correctly checks that ALL required equipment is available.
        
        Args:
            room: The meeting room to check
            required_equipment: Set of required equipment
        
        Returns:
            Tuple of (is_valid, reason)
        """
        if not required_equipment:
            return True, "No equipment required"
        
        # ✅ FIXED: Check if ALL required equipment is available
        # Previous buggy logic: bool(required_equipment & room.equipment) - checks ANY overlap
        # Correct logic: required_equipment.issubset(room.equipment) - checks ALL required items present
        
        has_all_equipment = required_equipment.issubset(room.equipment)
        
        if has_all_equipment:
            return True, "All required equipment available"
        else:
            missing = required_equipment - room.equipment
            return False, f"Missing equipment: {', '.join(e.value for e in missing)}"
    
    def _validate_capacity(self, room: MeetingRoom, attendee_count: int) -> tuple[bool, str]:
        """Validate that attendee count fits room capacity."""
        return check_capacity_fit(attendee_count, room.capacity, room.size)
    
    def _validate_time_constraints(self, request: BookingRequest) -> tuple[bool, str]:
        """Validate time-related constraints."""
        # Check 30-minute increment rule
        is_valid, reason = is_time_slot_valid(request.start_time, request.end_time)
        if not is_valid:
            return False, reason
        
        # Check lunch time restriction
        if is_lunch_time(request.start_time) or is_lunch_time(request.end_time):
            if not can_book_during_lunch(request.priority):
                return False, "Only P0/P1 meetings can be booked during lunch time (12:00-13:30)"
        
        return True, "Time constraints satisfied"
    
    def book_room(self, request: BookingRequest, preferred_room_id: Optional[str] = None) -> BookingResult:
        """
        Attempt to book a meeting room.
        
        Args:
            request: The booking request
            preferred_room_id: Optional preferred room ID
        
        Returns:
            BookingResult with success status and details
        """
        # Validate time constraints
        is_valid, reason = self._validate_time_constraints(request)
        if not is_valid:
            return BookingResult(False, f"Time validation failed: {reason}")
        
        # If preferred room specified, try that first
        if preferred_room_id:
            room = self.get_room(preferred_room_id)
            if not room:
                return BookingResult(False, f"Room {preferred_room_id} not found")
            
            # Check all requirements
            available, avail_reason, conflicts = self._check_room_availability(preferred_room_id, request)
            if not available:
                return BookingResult(False, f"Room {preferred_room_id}: {avail_reason}", 
                                   conflicting_bookings=conflicts)
            
            # ✅ Equipment validation now works correctly
            equipment_ok, equip_reason = self._validate_equipment_requirements(room, request.required_equipment)
            if not equipment_ok:
                return BookingResult(False, f"Room {preferred_room_id}: {equip_reason}")
            
            capacity_ok, cap_reason = self._validate_capacity(room, request.attendee_count)
            if not capacity_ok:
                return BookingResult(False, f"Room {preferred_room_id}: {cap_reason}")
            
            # All checks passed, create booking
            booking = Booking(
                booking_id=self._generate_booking_id(),
                room_id=preferred_room_id,
                organizer=request.organizer,
                start_time=request.start_time,
                end_time=request.end_time,
                attendee_count=request.attendee_count,
                priority=request.priority,
                required_equipment=request.required_equipment,
                title=request.title
            )
            self.bookings.append(booking)
            return BookingResult(True, f"Successfully booked {room.name}", booking)
        
        # Try to find suitable room automatically
        return BookingResult(False, "Automatic room selection not implemented yet")
    
    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings in the system."""
        return self.bookings.copy()
    
    def _generate_booking_id(self) -> str:
        """Generate a unique booking ID."""
        booking_id = f"BK{self._next_booking_id:04d}"
        self._next_booking_id += 1
        return booking_id