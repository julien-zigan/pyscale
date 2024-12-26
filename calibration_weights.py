import tkinter as tk
from math import sqrt, log
from time import sleep



class Application:

    def __init__(self):
        self.__x_start = 10
        self.__y_start = 20

        self.__window = tk.Tk()
        self.__window.title("Gewichtssteine")
        self.__window.state('zoomed')

        self.__canvas = tk.Canvas(self.__window, background='#a9d394')
        self.__canvas.pack(fill='both', expand=True)

        self.__prompt = tk.Label(self.__canvas, text="Gewicht der Ware: ",
                                 fg='black', font='helvetica', bg='#a9d394')
        self.__prompt.place(x=self.__x_start, y=self.__y_start)

        self.__entry_var = tk.StringVar()
        self.__entry_var.set("1 kg")
        self.__entry_var.trace_add("write", self.__set_merch)

        self.__merch_weigth = tk.Entry(self.__canvas, fg='black', font='helvetica',
                                       bg='lightgreen', justify='center',
                                       textvariable=self.__entry_var)
        self.__merch_weigth.place(x=self.__x_start + 200, y=self.__y_start)

        self.__tarry_btn = tk.Button(self.__canvas, text="Wiegen", command=self.__tarry_out)
        self.__tarry_btn.place(x=self.__x_start + 100, y=self.__y_start +50)

        self.__reset_btn = tk.Button(self.__canvas, text="Reset", command=self.__reset)
        self.__reset_btn.place(x=self.__x_start + 250, y=self.__y_start + 50)

        self.__stones = self.__create_stones()
        self.__paint_all(self.__stones)

        self.__lowest_y = self.__canvas.coords(self.__stones[0].handle)[3]
        self.__merch = Merchandise(1, self.__x_start + 230, self.__lowest_y / 2 + 10)
        self.__merch.paint(self.__canvas)

        self.__equal_sign = None

        self.__window.mainloop()


    @property
    def window(self) -> tk.Tk:
        return self.__window

    @property
    def canvas(self) -> tk.Canvas:
        return self.__canvas

    @property
    def current_merch_weigth(self):
        return int(self.__entry_var.get().strip(' kg').strip())

    def __create_stones(self):
        stones = []
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

            stones.insert(0, stone)

        return stones


    def __paint_all(self, collection):
        for item in collection:
            item.paint(self.__canvas)

    def __set_merch(self, *args):
        old_weight = self.__merch.weight
        new_weight = self.current_merch_weigth
        self.__entry_var.set(str(new_weight) + ' kg')
        while old_weight != new_weight:
            difference = + 1 if old_weight < new_weight else -1
            current_weight = old_weight + difference
            offset = (sqrt(current_weight) * 15) / 2
            self.__canvas.delete(self.__merch.label)
            self.__canvas.delete(self.__merch.handle)
            self.__merch = Merchandise(current_weight, self.__x_start + 230 - offset, self.__lowest_y / 2 + offset )
            old_weight += difference
            self.__merch.paint(self.__canvas)
            factor = abs(old_weight - new_weight)
            sleep(0.2 / factor)

    def __calculate_distribution(self, weight):
        result = [[], []]
        equation = weight
        for i in range(0, 6):
            b = 3 ** i
            a = (equation / b) % 3
            if a == 0: continue
            if a == 1:
                equation -= b
                result[1].append(b)
            if a == 2:
                equation += b
                result[0].append(b)
            if equation == 0:
                break
        return result

    def __tarry_out(self):
        y = 750
        placement = self.__calculate_distribution(self.current_merch_weigth)
        self.__merch.move_to(20, y)
        last_left = self.__canvas.coords(self.__merch.handle)[2]
        self.__equal_sign = self.canvas.create_text(last_left + 75, y - 15, text="≠", fill="red", font="calibri 28")

        for stone in placement[0]:
            index = int(log(stone, 3))
            if self.__stones[index].available:
                self.__stones[index].move_to(last_left + 10, y)

            self.__stones[index].available = False
            last_left = self.__canvas.coords(self.__stones[index].handle)[2]
            self.canvas.delete(self.__equal_sign)
            self.__equal_sign = self.canvas.create_text(last_left + 75, y - 15, text="≠", fill="red", font="calibri 28")


        last_right = last_left + 150
        for stone in placement[1]:
            index = int(round(log(stone, 3)))
            if self.__stones[index].available:
                self.__stones[index].move_to(last_right + 10, y)
            self.__stones[index].available = False
            last_right = self.__canvas.coords(self.__stones[index].handle)[2]
        self.canvas.delete(self.__equal_sign)
        self.__equal_sign = self.canvas.create_text(last_left + 75, y - 15, text="=", fill="green", font="calibri 28")


    def __reset(self):
        self.canvas.delete(self.__equal_sign)
        self.__merch.move_to(self.__merch.x, self.__merch.y)

        for stone in self.__stones:
            if stone.available:
                continue
            stone.move_to(stone.x, stone.y)
            stone.available = True



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
    def x(self):
        return self.__pos_x1

    @property
    def y(self):
        return self.__pos_y2

    @property
    def properties(self) -> tuple:
        return (self.__pos_x1, self.__pos_y1, self.__pos_x2, self.__pos_y2,
                {'fill':self.__color})

    @property
    def label_properties(self) -> tuple:
        x = self.__pos_x1 + self.__sides / 2
        y = self.__pos_y1 + self.__sides / 2
        unit = ' kg' if self.__weight > 6 else ''
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

    @property
    def label(self):
        return self.__label

    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, value):
        self.__available = value

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
    def __init__(self, weight, x, y):
        super().__init__(weight, x, y)
        self.color = 'gold'



'''############ TEST ##############'''
app = Application()











