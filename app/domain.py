from abc import ABC


class Equipment(ABC):
    def __init__(self):
        self.power = 0
        self.is_on = False
        self.unit = 10

    def power_up(self):
        pass

    def power_down(self):
        pass

    def cancel(self):
        self.power = 0
        self.is_on = False

    def get_state(self):
        return {"power": self.power, "is_on": self.is_on}


class Microwave(Equipment):
    def __init__(self):
        self.counter = 0
        self.message = ""
        super().__init__()

    def power_up(self):
        if self.power == 100:
            self.message = "Power is already set to 100%"
        else:
            self.power += self.unit
            if not self.is_on:
                self.is_on = True
            self.message = f"Power increased to {self.power}%"

    def power_down(self):
        if self.power == 0:
            self.message = "Power is already set to 0%"
        else:
            self.power -= self.unit
            if self.power == 0:
                self.is_on = False
            self.message = f"Power decreased to {self.power}%"

    def counter_up(self):
        if self.counter == 3600:
            self.message = "The counter is set to one hour - it's max value."
        else:
            self.counter += self.unit
            if not self.is_on:
                self.is_on = True
            self.message = f"Counter increased to {self.counter}s"

    def counter_down(self):
        if self.counter == 0:
            self.message = "Counter is already set to 0s"
        else:
            self.counter -= self.unit
            self.message = f"Counter decreased to {self.counter}s"

    def load(self, data):
        if not data:
            pass
        else:
            self.power = data["power"]
            self.counter = data["counter"]
            self.is_on = data["is_on"]

    def cancel(self):
        if self.counter == 0 and self.power == 0 and not self.is_on:
            self.message = "The microwave is already off."
        else:
            self.counter = 0
            self.power = 0
            self.is_on = False
            self.message = "The microwave has been canceled."

    def get_message(self):
        return self.message

    def get_state(self):
        return {"power": self.power, "counter": self.counter, "is_on": self.is_on}
