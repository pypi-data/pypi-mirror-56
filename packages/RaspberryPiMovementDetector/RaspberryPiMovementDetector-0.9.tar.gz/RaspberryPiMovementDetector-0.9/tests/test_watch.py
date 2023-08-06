import pytest
import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi

try:
    from RPi.GPIO import GPIO
except:
    import RPi as RPi
    GPIO = RPi.GPIO

from MovementDetector.Watch import Watch
stack = []

def func_moved_in(arg):
    stack.append("func_in_usage_" + str(arg))

def func_moved_out(arg):
    stack.append("func_out_usage_" + str(arg))

@pytest.mark.parametrize('trig, echo, offset, func_in, func_out', [(23, 24, 10, func_moved_in, func_moved_in), (3, 4, 1, func_moved_in, func_moved_out)])     
class TestWatch():
    def test_trig(self, trig, echo, func_in, func_out, offset):
        watch = Watch(GPIO, trig, echo, func_in, func_out, offset)
        assert watch.trigger_pin() == trig
        
    def test_echo(self, trig, echo, func_in, func_out, offset):
        watch = Watch(GPIO, trig, echo, func_in, func_out, offset)
        assert watch.echo_pin() == echo

    def test_distance(self, trig, echo, func_in, func_out, offset):
        watch = Watch(GPIO, trig, echo, func_in, func_out, offset)
        assert type(watch.get_distance()) is float

    def test_observe(self, trig, echo, func_in, func_out, offset):
        watch = Watch(GPIO, trig, echo, func_in, func_out, offset)
        watch.observe()
        assert stack[-1].startswith("func_in_usage_") or stack[-1].startswith("func_out_usage_")
