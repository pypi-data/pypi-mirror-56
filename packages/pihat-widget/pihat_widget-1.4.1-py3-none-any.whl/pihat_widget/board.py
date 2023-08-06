from tkinter import *
import multiprocessing as mp
import multiprocessing as q

class LEDMatrix:

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.continue_proc = False
        if self.q is not None:
            self.q.close()
    def __init__(self, rows = 8, cols = 8, color = (0,0,0), origin_x=5, origin_y=5,ledWidth =2, ledHeight=1, ledPadx=2,ledPady=2):

        self.origin_x = origin_x
        self.origin_y = origin_y
        self.__root = None
        self.continue_proc = True
        self.__rows = rows
        self.__cols = cols
        self.__ledWidth =ledWidth
        self.q = q.Queue()
        self.__ledHeight = ledHeight
        self.__ledPadx = ledPadx
        self.__ledPady = ledPady
        self.__p = None
        self.__ledColor = self.__from_rgb(color)
        self.__matrix = [[0 for x in range(cols)] for y in range(rows)]
        self.__show()

    def __from_rgb(self, rgb):

        if type(rgb) is not tuple:
            if type(rgb) is int:
                rgb = rgb, 0, 0

        return "#%02x%02x%02x" % rgb

    def __show(self):

        self.__p = mp.Process(target=self._create_matrix, args=(self.q,))

        self.__p.start()

    def _create_matrix(self, q):
        row = 0
        col = 0
        self.__root = Tk()
        self.__root.overrideredirect(True)
        #self.__root.title = "LED Matrix"
        new_row = None

        def on_closing():
            self.continue_proc=False

        self.__root.protocol("WM_DELETE_WINDOW", on_closing)

        for color in range(self.__rows*self.__cols):

            e = Label(self.__root, text="", background=self.__ledColor,font=(None, -10))
            e.config(height=self.__ledHeight, width=self.__ledWidth)
            e.grid(row=row, column=col, padx=self.__ledPadx,pady=self.__ledPady)
            self.__matrix[row][col]=e
            #e.pack(expand=YES, fill=BOTH)
            col += 1
            if (col == self.__cols):
                row+=1
                col = 0

        self.__root.geometry('+%d+%d' % (self.origin_x, self.origin_y))
        while self.continue_proc:
            self.__root.update_idletasks()
            if q.qsize() > 0:
                action, *params = q.get(block=True)
                # Do Work
                if action == "set_pixel":
                    self.__matrix[params[1]][params[0]].config(background=self.__from_rgb(params[2]))
                elif action=="set_pixels":
                    matrix = params[0]

                    for r, row in enumerate(matrix):
                        for c, column in enumerate(row):

                            self.__matrix[r][c].config(background=self.__from_rgb(column))

                elif action=="set_pixels_color":
                    matrix = params[0]
                    color = params[1]
                    for r, row in enumerate(matrix):
                        for c, column in enumerate(row):
                            if bool(column):
                                self.__matrix[r][c].config(background=self.__from_rgb(color))
                elif action=="clear":
                    self.__clear()
                elif action=="close":
                    self.continue_proc = False

                    self.q.close()
                    self.__root.destroy()
                    break

            self.__root.update()
    def set_pixels_color(self, matrix, color):

        self.q.put(("set_pixels_color",matrix, color))

    def set_pixels(self, matrix, color):

        self.q.put(("set_pixels",matrix))


    def set_pixel(self, x, y, color):

        self.q.put(("set_pixel",x,y,color))

    def close(self):
        self.continue_proc = False
        if self.q is not None:
            self.q.put(("close",[]))

    def clear(self):

        self.q.put(("clear",(0,)))

    def __clear(self):
        for row in range(self.__rows):
            for col in range(self.__cols):
                self.__matrix[row][col].config(background=self.__ledColor)
                #self.__matrix[row][col].config(background=self.__ledColor)

if __name__ == "__main__":
    import time

    matrix = [
        [255, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, (255,255,0)]
    ]

    with LEDMatrix(cols=8, rows=8) as b:

        b.set_pixels(matrix, (255,0,0))
        time.sleep(5)
