"""
Contains classes for
    LEDCharacter        - Single character number display
    LEFMultiCharacter   - Multicharacter display
"""
from pihat_widget import image
import time

class LEDCharacter(image.ImageLoader):
    """
    Display as single numeric character
    """
    def __init__(self, x, y):
        super().__init__(origin_x=x, origin_y=y, origin_width=45, origin_height=77, offsetx=0, offsety=0)
        self.__number = None

    @property
    def Number(self):
        """
        Returns the current displayed number
        :return: Displayed number
        """
        return self.__number
    @Number.setter
    def Number(self, number):
        """
        Allows the displayed value to be set
        :param number: Number to be set
        :return: None
        """
        if type(number) is int:
            self.q.put(("load",str(number)))
            self.__number = number
        else:
            raise ValueError("Number must be an int")


class LEDMultiCharacter:
    """
    Displays a multi character numeric character
    """
    def __del__(self):
        self.close()

    def __init__(self, digits = 2, x = 10, y = 10):
        """
        Initialises the class
        :param digits: Number of numeric digits to display
        """
        self.__digits = digits
        self.__chars = [LEDCharacter(x+(i*45),y) for i in range(digits)]
        self.__number = None
        for z in self.__chars:
            z.Number =0

    @property
    def Number(self):
        return self.__number

    @Number.setter
    def Number(self, number):
        if type(number) is int:

            num = f"{number:0{self.__digits}d}"
            for c,n in enumerate(num):
                self.__chars[c].Number = int(n)

        else:
            raise ValueError("Number must be an int")
    def close(self):
        for c in self.__chars:
            c.close()

if __name__ == "__main__":

    c = LEDCharacter(x = 150, y = 150)
    for i in range(10):
        c.Number = i
        time.sleep(0.5)
    time.sleep(3)
    c.close()

    c = LEDMultiCharacter(digits = 3, y=120)
    for i in range(105):
        c.Number =i
    c.close()

