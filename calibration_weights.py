from math import sqrt
import tkinter as tk
from time import sleep

class Application:

    def __init__(self):
        self.__x_start = 30
        self.__y_start = 50
        self.__window = tk.Tk()
        self.__window.title("Gewichtssteine")
        self.__window.state('zoomed')
        self.__canvas = tk.Canvas(self.__window, background='#a9d394')
        self.__canvas.pack(fill='both', expand=True)
        self.__window.update()
        self.__prompt = tk.Label(self.__canvas, text="Gewicht der Ware: ",
                                 fg='black', font='helvetica', bg='#a9d394')
        self.__prompt.place(x=self.__x_start, y=self.__y_start)
        self.__entry_var = tk.StringVar()
        self.__merch_weigth = tk.Entry(self.__canvas, fg='black', font='helvetica',
                                       bg='lightgreen', justify='center',
                                       textvariable=self.__entry_var)
        self.__merch_weigth.place(x=self.__x_start + 200, y=self.__y_start)
        self.__stones = []
        self.__create_stones()
        self.__paint_stones()

        self.__window.mainloop()

    @property
    def window(self) -> tk.Tk:
        return self.__window

    @property
    def canvas(self) -> tk.Canvas:
        return self.__canvas

    def __create_stones(self):
        x_start = 500
        y_start = (self.__y_start + sqrt(3**5) * 15) + 172

        for i in range(5, -1, -1):
            weight = 3**i
            side = sqrt(weight )* 15
            next_greater_side = sqrt(3**(i+1)) * 15

            if i % 2 == 0:
                x = x_start + next_greater_side - side
                y = y_start
                stone = WeightStone(weight, x, y)

            else:
                x = x_start
                y = y_start - next_greater_side + side
                stone = WeightStone(weight, x, y)

            self.__stones.insert(0, stone)

    def __paint_stones(self):
        for item in self.__stones:
            item.paint(self.__canvas)

class WeightStone:

    def __init__(self, weight: int, lower_left_x, lower_left_y):
        self.__weight = weight
        self.__sides = sqrt(weight) * 15
        self.__pos_x1 = lower_left_x
        self.__pos_y1 = lower_left_y - self.__sides
        self.__pos_x2 = lower_left_x + self.__sides
        self.__pos_y2 = lower_left_y
        self.__available = True
        self.__color = '#333435'
        self.__handle = None
        self.__canvas = None
        self.__label = None


    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value
        self.__sides = sqrt(value) * 15
        self.__pos_x1 = self.__canvas.coords(self.__handle)[0]
        self.__pos_y1 = self.__canvas.coords(self.__handle)[1] - self.__sides
        self.__pos_x2 = self.__canvas.coords(self.__handle)[2] + self.__sides
        self.__pos_y2 = self.__canvas.coords(self.__handle)[3]
        self.repaint()

    @property
    def sides(self):
        return self.__sides

    @property
    def properties(self) -> tuple:
        return (self.__pos_x1, self.__pos_y1, self.__pos_x2, self.__pos_y2,
                {'fill':self.__color})

    @property
    def label_properties(self) -> tuple:
        x = self.__pos_x1 + self.__sides / 2
        y = self.__pos_y1 + self.__sides / 2
        unit = ' kg' if self.__weight > 5 else ''
        text = f"{self.__weight}{unit}"
        fill = f'{'black' if type(self) != WeightStone else '#dadce0'}'
        font = 'Arial 14'
        return x, y, {'text': text, 'fill': fill, 'font': font}

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def handle(self):
        return self.__handle

    def paint(self, canvas: tk.Canvas):
        self.__canvas = canvas
        self.__handle = self.__canvas.create_rectangle(*self.properties)
        self.__label = self.__canvas.create_text(*self.label_properties)
        self.__canvas.update()

    def repaint(self):
        self.__canvas.delete(self.__handle)
        self.paint(self.__canvas)

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
             + f"{'available' if self.__available else 'on scale'}"
        return info


class Merchandise(WeightStone):
    def __init__(self):
        super().__init__(1, 150, 600)
        self.color = 'gold'



'''############ TEST ##############'''
app = Application()










