from datetime import datetime

STARTING_COUNTER_THRESHOLD = 3
COUNTER_THRESHOLD_INCREMENT_AMOUNT = 1
COUNTER_THRESHOLD_MAX = 5
STARTING_TIMER_THRESHOLD = 20  # seconds
TIMER_THRESHOLD_INCREMENT_AMOUNT = 10
TIMER_THRESHOLD_MAX = 90


class HelpTimerCounter:

    def __init__(self) -> None:
        self.enabled = False
        self.dynamic_counter_threshold = STARTING_COUNTER_THRESHOLD
        self.counter = 0
        self.start_time = datetime.now()
        self.dynamic_timer_threshold = STARTING_TIMER_THRESHOLD

    def update_counter(self) -> bool:
        self.counter = self.counter + 1
        print("Count: " + str(self.counter))
        return self.counter >= self.dynamic_counter_threshold

    def hit_counter(self):
        print("Hit counter")
        self.counter = 0
        if self.dynamic_counter_threshold < COUNTER_THRESHOLD_MAX:
            self.dynamic_counter_threshold += COUNTER_THRESHOLD_INCREMENT_AMOUNT

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
        if self.enabled and (datetime.now() - self.start_time).total_seconds() >= self.dynamic_timer_threshold:
            print("Hit timer")
            if self.dynamic_timer_threshold < TIMER_THRESHOLD_MAX:
                self.dynamic_timer_threshold += TIMER_THRESHOLD_INCREMENT_AMOUNT
            return True
        else:
            return False

    def stop_timer(self):
        print("Stopping timer")
        self.enabled = False
