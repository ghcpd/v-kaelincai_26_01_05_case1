FIX SUMMARY

Bug: Equipment validation allowed partial matches (accepted a room if it had ANY
of the required equipment).

Files changed:
- src/booking_system.py: fixed equipment validation in
  `_validate_equipment_requirements` (logic changed to require ALL items).

What was wrong
- The buggy code used an intersection check (`required_equipment & room.equipment`)
  and returned success if the intersection was non-empty.
- This allowed bookings where some required equipment items were missing.

What I changed
- Replaced the "any-overlap" check with a set difference check and
  explicit missing-equipment reporting.
- Only modified `src/booking_system.py` in `fixed_project/`.

Before (snippet, src/booking_system.py:103-111):

    has_any_equipment = bool(required_equipment & room.equipment)
    if has_any_equipment:
        return True, "Equipment available"
    else:
        missing = required_equipment - room.equipment
        return False, f"Missing equipment: {', '.join(e.value for e in missing)}"

After (snippet, src/booking_system.py:103-111):

    missing_equipment = required_equipment - room.equipment
    if missing_equipment:
        missing_names = ', '.join(e.value for e in missing_equipment)
        return False, f"Missing equipment: {missing_names}"
    else:
        return True, "All required equipment available"

How to verify
1. cd fixed_project
2. pip install -r requirements.txt
3. pytest tests/ -v

Expected test results
- Before: 2 tests failed, 2 passed
- After: 4 passed

Notes
- Only the equipment validation logic was changed.
- Tests were copied from the original project and are unchanged.
