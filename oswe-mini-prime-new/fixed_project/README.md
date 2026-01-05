# Meeting Room Booking System (Fixed Version)

## Overview

This repository contains a fixed version of the meeting room booking system where the equipment validation bug has been corrected.

## What was fixed

- **Bug**: The system previously approved bookings when the room had *any* of the required equipment items, instead of *all* required items.
- **Fix**: The `_validate_equipment_requirements` method in `src/booking_system.py` now verifies that **all** required equipment is present and returns a clear message listing missing items.

## Quick Start

1. Create a virtual environment and install dependencies:

```powershell
pip install -r requirements.txt
```

2. Run tests:

```powershell
pytest tests/ -v
```

## Test Results

All tests should pass after the fix:
- ✅ `test_bug_partial_equipment_match_should_fail`
- ✅ `test_bug_client_meeting_scenario`
- ✅ `test_correct_behavior_all_equipment_available`
- ✅ `test_successful_booking_no_equipment`

## Notes

- Only the equipment validation logic was changed.
- Original project remains unmodified; this is a fixed copy.
