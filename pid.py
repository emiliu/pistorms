from time import time

class PIDController:

    def __init__(self, min_out=None, max_out=None, target=0.0, kP=0.0, kI=0.0, kD=0.0):
        self.max_out = max_out
        self.min_out = min_out
        self.set_target(target, kP, kI, kD)

    def calculate(self, current):

        # time check
        now = time()
        dt = now - self.time

        # p, i, d updates
        error = self.target - current
        self.sigma += error * dt
        slope = (self.current - current) / dt

        # total and bound pid output
        output = self.kP * error + self.kI * self.sigma + self.kD * slope
        output = self.max_out if self.max_out is not None and output > self.max_out else output
        output = self.min_out if self.min_out is not None and output < self.min_out else output

        # update variables and return
        self.time = now
        self.current = current
        return output

    def set_target(self, target, kP=None, kI=None, kD=None):
        self.target = target
        self.time = time()
        self.current = 0
        self.sigma = 0
        self.kP = kP if kP is not None else self.kP
        self.kI = kI if kI is not None else self.kI
        self.kD = kD if kD is not None else self.kD

    def set_constants(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
