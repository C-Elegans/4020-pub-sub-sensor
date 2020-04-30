import Adafruit_BBIO.PWM as PWM
import time

PWM.start("P8_13", 25, 1000)
time.sleep(3)
PWM.stop("P8_13")
PWM.cleanup()
print("Done buzzin")
