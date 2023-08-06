Project description
Movement detector for RaspberryPi with Watch to watch objects coming into proximity.
Pass pins Trigger and Echo. Pass offset to determine boundary for the object to come in

Example

<pre>
from RPi.GPIO import GPIO
from MovementDetector.Watch import Watch

TRIG = 23
ECHO = 24

def func_moved_in(arg):
  print("process for object entering field")

def func_moved_out(arg):
  print("process for object exiting field")

OFFSET = 200 # 2m

watch = Watch(gpio=GPIO, trig=TRIG, echo=ECHO, func_in=func_moved_in, func_out=func_moved_out, offset=OFFSET)

watch.observe()

time.sleep(100) # Sleep 

watch.stop()
</pre>

Source code and more info at https://github.com/KSanthanam/RaspberryPiMovementDetector.

