import time

class Watch:
  def __init__(self, gpio, trig, echo):
    self._gpio = gpio
    self._trig = trig
    self._echo = echo
  
  def trigger_pin(self):
    return self._trig

  def echo_pin(self):
    return self._echo

  def get_distance(self):
    print("Distance Measurement In Progress")
    self._gpio.setup(self._trig, self.gpio.OUT)
    self._gpio.setup(self._echo, self.gpio.IN)
    self._gpio.output(self._trig, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    self._gpio.output(self._trig, True)
    time.sleep(0.00001)
    self._gpio.output(self._trig, False)

    while self._gpio.input(self._echo)==0:
      pulse_start = time.time()

    while self._gpio.input(self._echo)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    print("Distance:",distance,"cm")

    self._gpio.cleanup()
    
