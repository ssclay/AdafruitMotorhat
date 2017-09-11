from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Motorhat(Block):

    version = VersionProperty('0.1.0')
    motor0_speed = IntProperty(title='DC Motor 0 Speed', default=0)
    motor1_speed = IntProperty(title='DC Motor 1 Speed', default=0)
    motor2_speed = IntProperty(title='DC Motor 2 Speed', default=0)
    motor3_speed = IntProperty(title='DC Motor 3 Speed', default=0)

    def configure(self, context):
        super().configure(context)
        self.MotorHAT = Adafruit_MotorHAT(addr=0x60)

    def process_signals(self, signals):
        for signal in signals:
            for r in range(4):
                motor = getattr(self, 'motor{}_speed'.format(r))(signal)
                direction = Adafruit_MotorHAT.FORWARD if motor >= 0 \
                                    else Adafruit_MotorHAT.BACKWARD
                Adafruit_DCMotor(r, 0).run(direction)
                Adafruit_DCMotor(r, 0).setSpeed(abs(motor))

    def stop(self):
        for r in range(4):
            direction = Adafruit_MotorHAT.FORWARD
            Adafruit_DCMotor(r, 0).run(direction)
            Adafruit_DCMotor(r, 0).setSpeed(0)
        super().stop()
