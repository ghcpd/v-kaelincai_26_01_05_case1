"""
Test cases for the meeting room booking system.

These tests now PASS with the fixed equipment validation logic.
"""

import pytest
from datetime import datetime, timedelta
from src.models import (
    MeetingRoom, Booking, BookingRequest, Priority, Equipment, RoomSize
)
from src.booking_system import MeetingRoomBookingSystem


class TestEquipmentValidationBug:
    """
    Test suite that validates the equipment validation fix.
    
    These tests now PASS because the system correctly validates equipment requirements.
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
    
    def test_partial_equipment_match_should_fail(self, booking_system):
        """
        ✅ TEST CASE 1: Validate equipment validation fix
        
        Fixed: System now correctly rejects booking when room has SOME but not ALL required equipment.
        
        Scenario:
        - Room A has: {PROJECTOR}
        - Request needs: {PROJECTOR, VIDEO_CONF}
        - Expected: Booking should FAIL (missing VIDEO_CONF)
        - Actual: Booking now correctly FAILS
        """
        # Request requiring both projector AND video conference
        request = BookingRequest(
            organizer="Zhang Manager",
            start_time=datetime(2026, 1, 6, 10, 30),
            end_time=datetime(2026, 1, 6, 11, 30),
            attendee_count=9,
            priority=Priority.P1_CLIENT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Important Client Meeting"
        )
        
        # Try to book Room A (which only has PROJECTOR, missing VIDEO_CONF)
        result = booking_system.book_room(request, preferred_room_id="ROOM_A")
        
        # This assertion now PASSES with the fix
        assert result.success is False, \
            "Booking should fail when room doesn't have all required equipment"
        assert "video_conference" in result.message.lower(), \
            "Error message should mention missing video conference equipment"
    
    def test_client_meeting_scenario(self, booking_system):
        """
        ✅ TEST CASE 2: Real-world scenario validation
        
        This is the exact scenario from the requirements:
        - Client meeting needs projector + video conference
        - Room A only has projector
        - Booking now correctly fails
        """
        # Add existing booking to Room A (10:00-11:00)
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
        
        # New high-priority client meeting request (10:30-11:30)
        # This overlaps with existing booking but has higher priority
        # However, we'll test it for a non-overlapping time to isolate equipment bug
        client_request = BookingRequest(
            organizer="Zhang Manager",
            start_time=datetime(2026, 1, 6, 14, 0),  # 2:00 PM, no conflict
            end_time=datetime(2026, 1, 6, 15, 0),
            attendee_count=9,
            priority=Priority.P1_CLIENT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Client Negotiation"
        )
        
        # Try to book Room A
        result = booking_system.book_room(client_request, preferred_room_id="ROOM_A")
        
        # This now PASSES - booking correctly fails
        assert result.success is False, \
            "Room A lacks video conference system, booking should fail"
        
        # Verify the room actually doesn't have video conference
        room_a = booking_system.get_room("ROOM_A")
        assert Equipment.VIDEO_CONF not in room_a.equipment, \
            "Room A should not have video conference equipment"
    
    def test_correct_behavior_all_equipment_available(self, booking_system):
        """
        ✅ TEST CASE 3: Verify correct behavior when all equipment IS available
        
        This test should PASS - when room has all required equipment, booking succeeds.
        """
        request = BookingRequest(
            organizer="Tech Lead",
            start_time=datetime(2026, 1, 6, 15, 0),
            end_time=datetime(2026, 1, 6, 16, 0),
            attendee_count=5,
            priority=Priority.P2_CROSS_DEPT,
            required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},
            title="Tech Review"
        )
        
        # Room C has all equipment
        result = booking_system.book_room(request, preferred_room_id="ROOM_C")
        
        # This should pass
        assert result.success is True, \
            "Booking should succeed when room has all required equipment"
        assert result.booking is not None
        assert result.booking.room_id == "ROOM_C"
    
    def test_multiple_missing_equipment(self, booking_system):
        """
        ✅ TEST CASE 4: Request multiple equipment, room has none
        
        Validation: Room has PROJECTOR, request needs VIDEO_CONF + WHITEBOARD + AUDIO
        Expected: Should fail (missing 3 items)
        Actual: Correctly fails
        """
        request = BookingRequest(
            organizer="Product Manager",
            start_time=datetime(2026, 1, 6, 9, 0),
            end_time=datetime(2026, 1, 6, 10, 0),
            attendee_count=9,
            priority=Priority.P2_CROSS_DEPT,
            required_equipment={Equipment.VIDEO_CONF, Equipment.WHITEBOARD, Equipment.AUDIO},
            title="Product Planning"
        )
        
        # Room A only has PROJECTOR, none of the required equipment
        result = booking_system.book_room(request, preferred_room_id="ROOM_A")
        
        # This correctly fails (no overlap between required and available)
        assert result.success is False, \
            "Booking should fail when room has none of the required equipment"


class TestCorrectBookingBehavior:
    """Test cases for correct booking behavior (these should pass)."""
    
    @pytest.fixture
    def booking_system(self):
        """Create a booking system with test rooms."""
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
        """Test successful booking when no equipment is required."""
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
        """Test that time slots must be on 30-minute boundaries."""
        # Invalid time slot (not on 30-minute boundary)
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


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])