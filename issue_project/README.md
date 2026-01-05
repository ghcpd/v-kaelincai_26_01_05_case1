# Meeting Room Booking System (Bug Reproduction Project)

## Overview

This is a minimal implementation of an enterprise meeting room booking system with a **deliberately planted bug** for testing and demonstration purposes. The system manages meeting room reservations with complex business rules including priority levels, equipment requirements, capacity constraints, and time slot validation.

## 🐛 Known Issue

**Bug Type**: Functional Bug - Feature doesn't behave as specified (ignores constraints)

**Category**: Model gives wrong output or ignores constraints

**Description**: The equipment validation logic incorrectly approves bookings even when the room doesn't have all required equipment. It only checks if there's ANY overlap between required and available equipment, rather than ensuring ALL required equipment is available.

## Project Structure

```
meeting-room-booking/
├── src/
│   ├── __init__.py
│   ├── models.py              # Data models (Room, Booking, etc.)
│   ├── booking_system.py      # Core booking logic (contains bug)
│   └── utils.py               # Helper functions
├── tests/
│   ├── __init__.py
│   └── test_booking.py        # Test cases that expose the bug
├── data/
│   └── sample_data.json       # Sample test data
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md            # Detailed bug analysis
```

## Quick Start

### Installation and Running Tests

Run this single command to install dependencies and execute tests:

```powershell
pip install -r requirements.txt; pytest tests/ -v
```

Or step by step:

```powershell
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_booking.py -v

# Run with detailed output
pytest tests/test_booking.py -v --tb=short
```

### Expected Test Results

When you run the tests, **2 tests will FAIL** (exposing the bug) and **2 tests will PASS**:

- ❌ `test_bug_partial_equipment_match_should_fail` - **FAILS** (exposes bug)
- ❌ `test_bug_client_meeting_scenario` - **FAILS** (real-world scenario)
- ✅ `test_correct_behavior_all_equipment_available` - PASSES
- ✅ `test_successful_booking_no_equipment` - PASSES

## Business Rules

### Meeting Room Types
- **Small**: 2-6 people
- **Medium**: 7-15 people
- **Large**: 16-30 people

### Priority Levels (High to Low)
- P0: Executive/Board meetings
- P1: Client meetings
- P2: Cross-department collaboration
- P3: Internal department meetings
- P4: Casual discussions

### Key Constraints
1. **Capacity**: Attendee count should be 60%-90% of room capacity
2. **Time slots**: Must be on 30-minute boundaries
3. **Buffer time**: 15 minutes before/after each meeting
4. **Equipment**: Room must have ALL required equipment (🐛 bug here)
5. **Lunch restriction**: Only P0/P1 can book 12:00-13:30

## Bug Details

### Location
- **File**: `src/booking_system.py`
- **Method**: `MeetingRoomBookingSystem._validate_equipment_requirements()`
- **Line**: ~103-120

### Buggy Code
```python
def _validate_equipment_requirements(self, room: MeetingRoom, 
                                    required_equipment: Set[Equipment]) -> tuple[bool, str]:
    if not required_equipment:
        return True, "No equipment required"
    
    # 🐛 BUG: Only checks if ANY equipment matches, not ALL
    has_any_equipment = bool(required_equipment & room.equipment)
    
    if has_any_equipment:
        return True, "Equipment available"  # Wrong!
    else:
        missing = required_equipment - room.equipment
        return False, f"Missing equipment: {', '.join(e.value for e in missing)}"
```

### Trigger Condition
1. Request a booking with multiple equipment requirements (e.g., projector + video conference)
2. Select a room that has SOME but not ALL required equipment (e.g., only projector)
3. System incorrectly approves the booking

### Expected vs Actual Behavior

**Expected**: Booking fails with message "Missing equipment: video_conference"

**Actual**: Booking succeeds with message "Equipment available"

## Example Usage

```python
from datetime import datetime
from src.models import MeetingRoom, BookingRequest, Equipment, RoomSize, Priority
from src.booking_system import MeetingRoomBookingSystem

# Create system
system = MeetingRoomBookingSystem()

# Add room with only projector
room_a = MeetingRoom(
    room_id="ROOM_A",
    name="Conference Room A",
    size=RoomSize.MEDIUM,
    capacity=10,
    equipment={Equipment.PROJECTOR}  # Only has projector
)
system.add_room(room_a)

# Request booking needing projector AND video conference
request = BookingRequest(
    organizer="Manager",
    start_time=datetime(2026, 1, 6, 14, 0),
    end_time=datetime(2026, 1, 6, 15, 0),
    attendee_count=9,
    priority=Priority.P1_CLIENT,
    required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF},  # Needs both!
    title="Client Meeting"
)

# This will INCORRECTLY succeed due to the bug
result = system.book_room(request, preferred_room_id="ROOM_A")
print(f"Success: {result.success}")  # True (wrong!)
print(f"Message: {result.message}")  # "Equipment available" (wrong!)
```

## Test Cases

See `tests/test_booking.py` for detailed test cases:

1. **test_bug_partial_equipment_match_should_fail**: Core bug exposure
2. **test_bug_client_meeting_scenario**: Real-world scenario from requirements
3. **test_correct_behavior_all_equipment_available**: Validates correct behavior
4. **test_successful_booking_no_equipment**: Baseline functionality

## Fix Hint

The fix involves changing the equipment validation logic from checking "ANY overlap" to checking "ALL required items present". See `KNOWN_ISSUE.md` for the complete fix approach.

## Technology Stack

- **Language**: Python 3.8+
- **Testing**: pytest
- **OS**: Windows 11 (cross-platform compatible)

## License

This is a demonstration project for bug reproduction and testing purposes.
