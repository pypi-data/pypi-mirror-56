# PIHAT Widgets

## About

The purpose of this module is to provide a set of programmable visual gadgets designed to make learning programming more fun.

Rather than just creating data and displaying text on the screen you can create traffic light sequences or display number countdown sequences or even create your own color pixelated grid.

The module contains three gadgets

- LedMatrix
- TrafficLight
- LEDCharacter
- LEDMultiCharacter

## Details
All control have to be called from within the scope of a main clause:

```
 def main():
       # Do something with a pihat control

if __name__ == "__main__":
    
    main()
    
```

### LedMatrix

Displays an LED grid of lights. The colour of each light can be controlled using an RGB tuple

```
if __name__ == "__main__":
    import pihat_widget as ph
    import time
    # Create the Matrix with 8 rows and columns at screen pos 5, 5 (x, y)
    matrix = ph.LEDMatrix(rows = 8, cols = 8, origin_x = 5, origin_y = 5)
    matrix.clear() # Clear all pixels
    red_color = 255, 0, 0 # RGB red
    black_color = 0, 0, 0 # RGB Black
    # Set the pixel at (x, y) pos 0, 0 the RGB color red
    matrix.set_pixel(x = 0, y = 0, color =  red_color)
    time.sleep(5) # Sleep for 5 seconds
    matrix.set_pixel(x = 0, y = 0, color =  black_color)
    matrix.set_pixel(x=0, y=1, color=red_color)
    time.sleep(3)
    matrix.close()```
```
 
### TrafficLight
 
```
if __name__ == "__main__":
    import pihat_widget as ph
    import time

    light = ph.TrafficLight()
    count =0
    while count<1:
        light.set_state("100")

        time.sleep(5)
        light.set_state("110")
        time.sleep(2.7)
        light.set_state("001")
        time.sleep(5)
        light.set_state("010")
        time.sleep(2.7)
        count+=1
    light.close()
```

### LEDCharacter

Creates a single character segmented numeric display.
 
Set the number property to display the number
 
 ```
if __name__ == "__main__":
    import pihat_widget as ph
    import time
 
    c = ph.LEDCharacter(x = 150, y = 150)
    for i in range(10):
        c.Number = i
        time.sleep(0.5)
    time.sleep(3)
    c.close()
 ```
### LEDMultiCharacter
 
 Creates a multi character segmented numeric display.
 
 Set the number property to display the number
 
 ```
if __name__ == "__main__":
    import pihat_widget as ph
    import time
 
    c = ph.LEDMultiCharacter(digits = 3, y=120)
    for i in range(105):
        c.Number =i
    c.close()
 ```