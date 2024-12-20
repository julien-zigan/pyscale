from math import sqrt
import tkinter as tk
from time import sleep

class WeightStone:

    def __init__(self, weight: int, lower_left_x, lower_left_y):
        self.__weight = weight
        self.__sides = int(sqrt(weight)) * 15
        self.__pos_x1 = lower_left_x
        self.__pos_y1 = lower_left_y - self.__sides
        self.__pos_x2 = lower_left_x + self.__sides
        self.__pos_y2 = lower_left_y
        self.__in_use = False
        self.__color = 'black'
        self.__handle = None
        self.__canvas = None
        self.__label = None

    @property
    def properties(self) -> tuple:
        return (self.__pos_x1, self.__pos_y1, self.__pos_x2, self.__pos_y2,
                {'fill':self.__color})

    @property
    def label_properties(self) -> tuple:
        x = self.__pos_x1 + self.__sides / 2
        y = self.__pos_y1 + self.__sides / 2
        text = f"{self.__weight} kg"
        fill = 'white'
        font = 'Arial 14'
        return x, y, {'text': text, 'fill': fill, 'font': font}

    def draw_on(self, canvas: tk.Canvas):
        self.__canvas = canvas
        self.__handle = canvas.create_rectangle(*self.properties)
        self.__label = canvas.create_text(*self.label_properties)
        self.__canvas.update()

    def move(self, x, y):

        max_val = max([x, y], key=abs)

        for i in range(abs(max_val)):

            if i < abs(x):
                move_x = 1 if x > 0 else -1
            else: move_x = 0
            if i < abs(y):
                move_y = 1 if y > 0 else -1
            else: move_y = 0

            self.__canvas.move(self.__handle, move_x, move_y)
            self.__canvas.move(self.__label, move_x, move_y)
            self.__canvas.update()
            sleep(0.002)

    def move_to(self, x, y):
        current_position = self.__canvas.coords(self.__handle)
        destination_x = int(x -current_position[0])
        destination_y = int((y - current_position[1]) - self.__sides)
        self.move(destination_x, destination_y)


    def __str__(self):
        info = f"{self.__weight} kg Stone, " \
             + f"Position: ({self.__pos_x1}, {self.__pos_y1}, " \
             + f"{self.__pos_x2}, {self.__pos_y2}), " \
             + f"{'on scale' if self.__in_use else 'available'}"
        return info



class Application:


    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title("Gewichtssteine")
        self.__window.state('zoomed')
        self.__canvas = tk.Canvas(self.__window, background='DarkSeaGreen2')
        self.__canvas.pack(fill='both', expand=True)
        self.__window.update()
        self.__prompt = tk.Label(self.__canvas, text="Gewicht der Ware: ",
                                 fg='black', font='helvetica', bg='DarkSeaGreen2')
        self.__prompt.place(x=100, y=200)
        self.__entry_var = tk.StringVar()

    @property
    def window(self) -> tk.Tk:
        return self.__window

    @property
    def canvas(self) -> tk.Canvas:
        return self.__canvas

'''##########################'''

app = Application()
stone = WeightStone(81, 100, 200)
stone.draw_on(app.canvas)
sleep(1)
stone.move_to(1000, 800)
app.window.mainloop()







