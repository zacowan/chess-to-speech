from datetime import datetime

STARTING_COUNTER_THRESHOLD = 2
TIMER_THRESHOLD = 20  # seconds


class HelpTimerCounter:

    def __init__(self) -> None:
        self.enabled = False
        self.dynamic_counter_threshold = STARTING_COUNTER_THRESHOLD
        self.counter = 0
        self.start_time = datetime.now()

    def update_counter(self) -> bool:
        self.counter = self.counter + 1
        print("Count: " + str(self.counter))
        return self.counter >= self.dynamic_counter_threshold

    def hit_counter(self):
        print("Hit counter")
        self.counter = 0
        self.dynamic_counter_threshold += 1

    def reset_counter(self):
        print("Resetting counter")
        self.counter = 0

    def start_timer(self):
        print("Starting timer")
        self.enabled = True
        self.start_time = datetime.now()

    def update_timer(self):
        print("Updating timer")
        self.start_time = datetime.now()

    def check_timer(self) -> bool:
        print("Checking timer")
        if self.enabled:
            return (datetime.now() - self.start_time).total_seconds() >= TIMER_THRESHOLD
        else:
            return False

    def stop_timer(self):
        print("Stopping timer")
        self.enabled = False
