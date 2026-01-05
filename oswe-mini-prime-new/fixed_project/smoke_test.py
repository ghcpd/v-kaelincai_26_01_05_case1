from datetime import datetime
from src.models import MeetingRoom, BookingRequest, RoomSize, Equipment, Priority
from src.booking_system import MeetingRoomBookingSystem

s = MeetingRoomBookingSystem()
r = MeetingRoom('R1','Room1',RoomSize.MEDIUM,10,equipment={Equipment.PROJECTOR})
s.add_room(r)
req = BookingRequest('org', datetime(2026,1,6,14,0), datetime(2026,1,6,15,0), 9, Priority.P1_CLIENT, required_equipment={Equipment.PROJECTOR, Equipment.VIDEO_CONF}, title='smoke')
res = s.book_room(req, preferred_room_id='R1')
print('SMOKE_TEST_RESULT:', res.success, repr(res.message))
