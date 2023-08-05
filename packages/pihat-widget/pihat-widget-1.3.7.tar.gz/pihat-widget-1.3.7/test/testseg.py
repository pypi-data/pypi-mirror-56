import pihat_widget.segment as ph
import  time

c = ph.LEDMultiCharacter(5)
for i in range(105):
    c.Number = i
    time.sleep(1)
c.close()
