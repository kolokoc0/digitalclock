import tkinter as tk
import time
from datetime import datetime

root = tk.Tk()

canvas = tk.Canvas(root, height=800, width=800, bg="black")
canvas.pack()


class Line:
    def __init__(self, point: tuple, dx: int, dy: int, color: str, canvas):
        self.coords = point
        self.dx = dx
        self.dy = dy
        self.color = color
        self.canvas = canvas
        self.id = canvas.create_rectangle(point[0], point[1], point[0] + dx, point[1]+dy, fill = color, outline = "")
    
    def on(self):
        self.canvas.itemconfig(self.id, fill = self.color)

    def off(self):
        self.canvas.itemconfig(self.id, fill = "black")

class Oval:
    def __init__(self, point:tuple, d,color:str,canvas):
        self.coords = point
        self.d = d
        self.color = color
        self.canvas = canvas
        self.id = canvas.create_oval(point[0],point[1],point[0]+d,point[1]+d,fill=color, outline = '')

    def on(self):
        self.canvas.itemconfig(self.id, fill = self.color)
    def off(self):

        self.canvas.itemconfig(self.id,fill='black')


class Segment:
    def __init__(self, point: tuple, small: int, big: int, color: str, canvas):
        self.parts = []
        self.coords = point
        sx = point[0]
        sy = point[1]
        self.parts.append(Line((sx +small, sy), big, small, color, canvas)) # upper -
        self.parts.append(Line((sx + small+big, sy + small), small, big, color, canvas)) #  upper right >|
        self.parts.append(Line((sx + small, sy +big+small), big, small, color, canvas)) # middle -
        self.parts.append(Line((sx, sy+small), small, big, color, canvas)) #  upper left <|
        self.parts.append(Line((sx + small + big, sy + 2*small + big), small, big, color, canvas)) #lower right >|
        self.parts.append(Line((sx + small, sy + 2 * big + 2 * small), big, small, color, canvas)) #lower bottom _
        self.parts.append(Line((sx, sy + 2 * small + big), small, big, color, canvas)) #lower left <|
    
    def reset(self):
        for i in self.parts:
            i.off()
    
    def error(self):
        for i in self.parts:
            i.on()
    
    def display(self, number: int):
        match int(number):
            case 0:
                self.error()
                self.parts[2].off()
            case 1:
                self.reset()
                self.parts[1].on()
                self.parts[4].on()
            case 2:
                self.reset()
                self.parts[0].on()
                self.parts[1].on()
                self.parts[2].on()
                self.parts[6].on()
                self.parts[5].on()
            case 3:
                self.error()
                self.parts[3].off()
                self.parts[6].off()
            case 4:
                self.error()
                self.parts[0].off()
                self.parts[6].off()
                self.parts[5].off()
            case 5:
                self.error()
                self.parts[1].off()
                self.parts[6].off()
            case 6:
                self.error()
                self.parts[1].off()
            case 7:
                self.reset()
                self.parts[0].on()
                self.parts[1].on()
                self.parts[4].on()
            case 8:
                self.error()
            case 9:
                self.error()
                self.parts[6].off()
            case _:
                print("invalid input")


class Clock:
    # sklada sa zo 6 segmentov
    # metoda on (zobrat systemovy cas, rozbit na cislice)
    def __init__(self, color: str, canvas, small:int, big:int, point:tuple):
        self.canvas = canvas
        self.small = small
        self.big = big
        self.point = point
        self.segments = []
        self.ovals = []
        for i in range(6):
            if i%2==0 or i ==5:
                self.segments.append(Segment((point[0] + i * (2 * small + big +20), point[1]), small, big, color, canvas))
            else:
                self.segments.append(Segment((point[0] + i * (2 * small + big +20), point[1]), small, big, color, canvas))
                self.ovals.append(Oval((point[0]+(i+1)*(2 * small + big + 20)-(20+8)/2,point[1]+(3*small+2*big)/4),8,color,canvas))
                self.ovals.append(Oval((point[0]+(i+1)*(2 * small + big + 20)-(20+8)/2,point[1]+(3*small+2*big)*3/4),8,color,canvas))
        self.update_clock()


    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_time = current_time.split(':')
        current_time = [letter for word in current_time for letter in word]
        for i in range(len(current_time)):
            self.segments[i].display(current_time[i])
        self.canvas.after(1000, self.update_clock)








skuska = Clock('red', canvas, 10,50,(100,100))


root.mainloop()
