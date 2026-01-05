"""
Test cases for the meeting room booking system (fixed project).

These are copied from the original project and should all pass after the fix.
"""

import pytest
from datetime import datetime, timedelta
from src.models import (
    MeetingRoom, Booking, BookingRequest, Priority, Equipment, RoomSize
)
from src.booking_system import MeetingRoomBookingSystem


class TestEquipmentValidationBug:
    """
    Test suite that exposes the equipment validation bug.
    """
    
    @pytest.fixture
    def booking_system(self):
        """Create a booking system with test rooms."""
        system = MeetingRoomBookingSystem()
        
        # Room A: Medium, only has projector
        room_a = MeetingRoom(
            room_id="ROOM_A",
            name="Conference Room A",
            size=RoomSize.MEDIUM,
            capacity=10,
            equipment={Equipment.PROJECTOR}  # Only projector!
        )
        
        # Room B: Large, has projector and video conference
        room_b = MeetingRoom(
            room_id="ROOM_B",
            name="Conference Room B",
            size=RoomSize.LARGE,
            capacity=25,
            equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF}
        )
        
        # Room C: Small, has all equipment
        room_c = MeetingRoom(
            room_id="ROOM_C",
            name="Conference Room C",
            size=RoomSize.SMALL,
            capacity=6,
            equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF, 
                      Equipment.WHITEBOARD, Equipment.AUDIO}
        )
        
        system.add_room(room_a)
        system.add_room(room_b)
        system.add_room(room_c)
        
        return system
    
    def test_bug_partial_equipment_match_should_fail(self, booking_system):
        """
        Test: booking should fail when room has only some required equipment.
        """
        request = BookingRequest(
            organizer="Zhang Manager",
            start_time=datetime(2026, 1, 6, 10, 30),
            end_time=datetime(2026, 1, 6, 11, 30),
            attendee_count=9,
            priority=Priority.P1_CLIENT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Important Client Meeting"
        )
        
        result = booking_system.book_room(request, preferred_room_id="ROOM_A")
        
        assert result.success is False, \
            "Booking should fail when room doesn't have all required equipment"
        assert "video_conference" in result.message.lower(), \
            "Error message should mention missing video conference equipment"
    
    def test_bug_client_meeting_scenario(self, booking_system):
        """
        Real-world scenario: client meeting requiring multiple pieces of equipment.
        """
        existing_booking = Booking(
            booking_id="BK0001",
            room_id="ROOM_A",
            organizer="Marketing Team",
            start_time=datetime(2026, 1, 6, 10, 0),
            end_time=datetime(2026, 1, 6, 11, 0),
            attendee_count=8,
            priority=Priority.P3_INTERNAL,
            title="Marketing Internal Meeting"
        )
        booking_system.add_booking(existing_booking)
        
        client_request = BookingRequest(
            organizer="Zhang Manager",
            start_time=datetime(2026, 1, 6, 14, 0),
            end_time=datetime(2026, 1, 6, 15, 0),
            attendee_count=9,
            priority=Priority.P1_CLIENT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Client Negotiation"
        )
        
        result = booking_system.book_room(client_request, preferred_room_id="ROOM_A")
        
        assert result.success is False, \
            "Room A lacks video conference system, booking should fail"
        
        room_a = booking_system.get_room("ROOM_A")
        assert Equipment.VIDEO_CONF not in room_a.equipment, \
            "Room A should not have video conference equipment"
    
    def test_correct_behavior_all_equipment_available(self, booking_system):
        request = BookingRequest(
            organizer="Tech Lead",
            start_time=datetime(2026, 1, 6, 15, 0),
            end_time=datetime(2026, 1, 6, 16, 0),
            attendee_count=5,
            priority=Priority.P2_CROSS_DEPT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Tech Review"
        )
        
        result = booking_system.book_room(request, preferred_room_id="ROOM_C")
        
        assert result.success is True, \
            "Booking should succeed when room has all required equipment"
        assert result.booking is not None
        assert result.booking.room_id == "ROOM_C"
    
    def test_bug_multiple_missing_equipment(self, booking_system):
        request = BookingRequest(
            organizer="Product Manager",
            start_time=datetime(2026, 1, 6, 9, 0),
            end_time=datetime(2026, 1, 6, 10, 0),
            attendee_count=9,
            priority=Priority.P2_CROSS_DEPT,
            required_equipment={Equipment.VIDEO_CONF, Equipment.WHITEBOARD, Equipment.AUDIO},
            title="Product Planning"
        )
        
        result = booking_system.book_room(request, preferred_room_id="ROOM_A")
        
        assert result.success is False, \
            "Booking should fail when room has none of the required equipment"


class TestCorrectBookingBehavior:
    @pytest.fixture
    def booking_system(self):
        system = MeetingRoomBookingSystem()
        
        room = MeetingRoom(
            room_id="ROOM_TEST",
            name="Test Room",
            size=RoomSize.MEDIUM,
            capacity=10,
            equipment={Equipment.PROJECTOR, Equipment.WHITEBOARD}
        )
        system.add_room(room)
        
        return system
    
    def test_successful_booking_no_equipment(self, booking_system):
        request = BookingRequest(
            organizer="Team Lead",
            start_time=datetime(2026, 1, 6, 10, 0),
            end_time=datetime(2026, 1, 6, 11, 0),
            attendee_count=8,
            priority=Priority.P3_INTERNAL,
            required_equipment=set(),  # No equipment required
            title="Team Standup"
        )
        
        result = booking_system.book_room(request, preferred_room_id="ROOM_TEST")
        
        assert result.success is True
        assert result.booking is not None
        assert result.booking.room_id == "ROOM_TEST"
    
    def test_time_slot_validation(self, booking_system):
        request = BookingRequest(
            organizer="Team Lead",
            start_time=datetime(2026, 1, 6, 10, 15),  # Invalid: 10:15
            end_time=datetime(2026, 1, 6, 11, 0),
            attendee_count=8,
            priority=Priority.P3_INTERNAL,
            title="Invalid Time Meeting"
        )
        
        result = booking_system.book_room(request, preferred_room_id="ROOM_TEST")
        
        assert result.success is False
        assert "30-minute" in result.message
