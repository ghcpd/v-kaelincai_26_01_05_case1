Fixed Meeting Room Booking System

This is the fixed version of the meeting room booking system where the
equipment validation bug has been corrected.

What was fixed
- Corrected equipment validation so a room must contain ALL required equipment
  before a booking is approved (previously allowed partial matches).

Quick start
1. Create a virtual environment and install deps:
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

2. Run tests:
   pytest tests/ -v

Verification
- All tests in `tests/test_booking.py` should pass.
