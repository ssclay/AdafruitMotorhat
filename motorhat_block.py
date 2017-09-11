from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty, FloatProperty
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Motorhat(Block):

    version = VersionProperty('0.1.0')
    motor1_speed = FloatProperty(title='DC Motor 0 Speed', default=0)
    motor2_speed = FloatProperty(title='DC Motor 1 Speed', default=0)
    motor3_speed = FloatProperty(title='DC Motor 2 Speed', default=0)
    motor4_speed = FloatProperty(title='DC Motor 3 Speed', default=0)

    def configure(self, context):
        super().configure(context)
        self.MotorHAT = Adafruit_MotorHAT(addr=0x60)

    def process_signals(self, signals):
        for signal in signals:
            for r in range(1, 5):
                speed = getattr(self, 'motor{}_speed'.format(r))(signal)
                direction = Adafruit_MotorHAT.FORWARD if speed >= 0 \
                                    else Adafruit_MotorHAT.BACKWARD
                Adafruit_DCMotor(0, r).run(direction)
                Adafruit_DCMotor(0, r).getMotor.setSpeed(abs(speed))

    def stop(self):
        for r in range(4):
            direction = Adafruit_MotorHAT.FORWARD
            Adafruit_DCMotor(0, r).run(direction)
            Adafruit_DCMotor(0, r).setSpeed(0)
        super().stop()
