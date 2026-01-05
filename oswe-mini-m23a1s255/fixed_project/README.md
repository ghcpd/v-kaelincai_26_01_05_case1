# Meeting Room Booking System — fixed_project

This is the fixed version of the meeting room booking system. It contains a
minimal, focused fix for the equipment-validation bug present in the original
`issue_project`.

What was fixed
- Equipment validation now requires ALL requested equipment to be present in
  the room (previously the code allowed a booking when ANY required item was
  present).

Quick start
- Create a virtualenv and install dependencies:

  pip install -r requirements.txt

- Run the tests:

  pytest tests/ -v

What to expect
- All tests should pass (4 passed). The two previously-failing tests that
  exposed the equipment-validation bug are fixed.

Files changed
- src/booking_system.py — fixed equipment validation (single small change)
- README.md, FIX_SUMMARY.md — documentation added

License: demo/project exercise
