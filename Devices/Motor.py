"""
General class for a motor
We want that only one mission at a time controls each motor, so every motor
must have a locking functionality
"""


class Motor:
    def __init__(self):
        self.locked = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def is_locked(self):
        return self.locked
