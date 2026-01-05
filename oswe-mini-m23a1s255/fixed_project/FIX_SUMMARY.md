FIX SUMMARY — Equipment validation bug

Summary
-------
- Bug: _Equipment validation allowed partial matches_ — the system approved a
  booking if the room had ANY of the required equipment instead of ALL.
- Location: `src/booking_system.py` — method `_validate_equipment_requirements`
- Fix: Replace "any-overlap" logic with a subset/difference check so that the
  booking only succeeds when ALL required equipment items are present.

What I changed
--------------
- src/booking_system.py: corrected `_validate_equipment_requirements` (3-line
  logical change). No other business logic was modified.
- Added this `FIX_SUMMARY.md` and updated `README.md` for the fixed project.

Before (buggy)
---------------
src/booking_system.py: the method checked intersection and treated any
non-empty intersection as success:

    has_any_equipment = bool(required_equipment & room.equipment)
    if has_any_equipment:
        return True, "Equipment available"

After (fixed)
-------------
src/booking_system.py: compute missing equipment and fail if any required
items are absent:

    missing_equipment = required_equipment - room.equipment
    if missing_equipment:
        missing_names = ', '.join(e.value for e in missing_equipment)
        return False, f"Missing equipment: {missing_names}"
    else:
        return True, "All required equipment available"

Why this fixes the bug
----------------------
- The original code validated presence by checking intersection; that allowed
  partial matches to pass. The new logic explicitly computes the missing set
  and ensures it is empty before approving the booking.

How to verify
-------------
Run the unit tests in the `fixed_project` directory:

    pip install -r requirements.txt
    pytest tests/ -v

Expected test results
- Before: 2 failed, 2 passed
- After: 4 passed

Relevant files/lines
- src/booking_system.py: _validate_equipment_requirements (around the top of
  the file) — single focused change
- tests/test_booking.py: failing test cases demonstrating the bug

Notes
-----
- Only the equipment validation logic was changed.
- No test modifications were made.
- Change is small, clear, and unit-tested.
