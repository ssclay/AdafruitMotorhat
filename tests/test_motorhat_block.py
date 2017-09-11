from unittest.mock import MagicMock, patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from motorhat_block import Motorhat


class TestMotorhat(NIOBlockTestCase):
    def test_process_signals(self):
        """."""

        with patch(Motorhat.__module__ + '.Adafruit_MotorHAT') as mock_MotorHAT, \
                patch(Motorhat.__module__ + '.Adafruit_DCMotor') as mock_DCMotor:
            mock_MotorHAT.return_value.getMotor = MagicMock()
            fwd = mock_MotorHAT.FORWARD = MagicMock()
            rev = mock_MotorHAT.BACKWARD = MagicMock()
            input_signal = {'a': 205,
                            'b': 43,
                            'c': 0,
                            'd': 0}
            blk = Motorhat()
            self.configure_block(blk, {'motor1_speed': '{{$a}}',
                                       'motor2_speed': '{{$b}}',
                                       'motor3_speed': '{{$c}}',
                                       'motor4_speed': '{{$d}}'})
            blk.start()
            blk.process_signals([Signal(input_signal)])
            self.assertEqual(mock_MotorHAT.return_value.getMotor.return_value.run.call_count, len(input_signal))
            self.assertEqual(mock_MotorHAT.return_value.getMotor.return_value.setSpeed.call_count,4)
            for key in input_signal:
                mock_MotorHAT.return_value.getMotor.return_value.setSpeed.assert_any_call(abs(input_signal[key]))
                mock_MotorHAT.return_value.getMotor.return_value.run.assert_any_call(fwd if input_signal[key] >= 0 else rev)
            blk.stop()
            mock_MotorHAT.return_value.getMotor().setSpeed.assert_called_with(0)
            self.assertEqual(mock_MotorHAT.return_value.getMotor.return_value.run.call_count, len(input_signal) * 2)
            self.assertEqual(mock_MotorHAT.return_value.getMotor.return_value.setSpeed.call_count,len(input_signal) * 2)
