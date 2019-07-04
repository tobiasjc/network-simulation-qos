import generators as gens
# from dataclasses import dataclass # for python3.7 only, I will not use this here but could

# simply labels for identifying process, so by defining them we might have no problem with the program
# while running, so be free to name the events as you like, as long as they are different
_VOIP = "\"VoIP Arrival\""
_CBR = "\"CBR\""
_WEB = "\"Web Packet\""
_SERVICE = "\"System Service\""


class Packet:

    def __init__(self, time_arrival, size):
        self.time_arrival = time_arrival
        self.size = size

    def delay(self, time_actual):
        return time_actual - self.time_arrival

    def __lt__(self, other):
        return self.time_arrival < other.time_arrival

    def __str__(self):
        return f"Packet arrival at {self.arrival} with a size of {self.size}"

    __repr__ = __str__


class EventService:

    def __init__(self, case, time):
        self.case = case
        self.next_event = time

    def __lt__(self, other):
        return self.next_event < other.next_event

    def __str__(self):
        return f"Event of type {self.case} on {self.next_event}"

    __repr__ = __str__


class EventArrival:

    def __init__(self, ep, sp, case):
        self.ep = ep
        self.sp = sp
        self.case = case
        self.next_event = ep.time_actual

    def next_event_update(self):
        # tweak needed, since this same class will test two different arrival events
        # namely for web and for voip connections
        if self.case == _WEB:
            self.next_event = self.ep.time_actual + gens.gen_exp(self.sp.web_packet_rate)
        elif self.case == _VOIP:
            self.next_event = self.ep.time_actual + gens.gen_exp(self.sp.voip_connection_rate)

    def __lt__(self, other):
        return self.next_event < other.next_event

    def __str__(self):
        return f"Event of type {self.case} with next event on {self.next_event}"

    __repr__ = __str__


class EventConnection:

    def __init__(self, ep, sp, case, duration, cbr_interval):
        self.ep = ep
        self.sp = sp
        self.case = case
        self.next_event = ep.time_actual
        self.end = ep.time_actual + duration
        self.cbr_interval = cbr_interval

    def is_over(self):
        return self.next_event >= self.end

    def next_event_update(self):
        self.next_event = self.next_event + self.cbr_interval

    def __lt__(self, other):
        return self.next_event < other.next_event

    def __str__(self):
        return f"Event of type {self.case} with next event on {self.next_event}"

    __repr__ = __str__
