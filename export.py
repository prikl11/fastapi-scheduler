from ics import Calendar, Event as ICSEvent
from io import StringIO

def generate_ics(events):
    c = Calendar()

    for e in events:
        ev = ICSEvent()
        ev.name = e.title
        ev.begin = e.start_time
        ev.end = e.end_time
        c.events.add(ev)

    f = StringIO(str(c))
    f.seek(0)
    return f