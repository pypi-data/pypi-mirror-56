# from RaspberryPiMovementDetector.Watch import Watch
from MovementDetector.Watch import Watch
# def test_placeholder():
#     watch = Watch()
#     pass

class TestWatch():
    def test_trig(self):
        watch = Watch()
        assert watch.trig == 1
        # pass