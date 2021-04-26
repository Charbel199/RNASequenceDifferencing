from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from similarityMeasures import similarity,tokenization
from os import sys, path
sys.path.append(path.dirname(__file__))


# Managing GUI
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MyWindow1(Page):
    # All GUI components and placements
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.firstSequenceLabel = Label(self, text='First sequence')
        self.secondSequenceLabel = Label(self, text='Second sequence')
        self.firstSequence = Text(self, bd=3, width=50, height=1)
        self.secondSequence = Text(self, bd=3, width=50, height=1)
        

        self.firstSequenceLabel.place(x=100, y=50)
        self.firstSequence.place(x=200, y=50)
        self.secondSequenceLabel.place(x=100, y=100)
        self.secondSequence.place(x=200, y=100)

        self.computeSimilaritiesButton = Button(self, text='Compute Similarities', command=self.computeSimilarities)
        self.computeSimilaritiesButton.place(x=100, y=150)

        self.tokenizationMethod = StringVar(self)
        self.tokenizationMethod.set("Tag-based")  # default value

        self.tokenizationMethodOptions = OptionMenu(self,  self.tokenizationMethod, "Tag-based", "Edge-based", "All Paths").place(x=250,y=148)

        self.similairtyLabel =  Label(self, text='Similarity')
        self.timeLabel = Label(self, text='Time (s)')
        self.similairtyLabel.place(x=750, y=20)
        self.timeLabel.place(x=870, y=20)

        self.TEDLabel = Label(self, text='TED: ')
        self.TED = Text(self, bd=1, width=10, height=1)
        self.TEDTime = Text(self, bd=1, width=10, height=1)
        self.TEDLabel.place(x=650, y=50)
        self.TED.place(x=750, y=50)
        self.TEDTime.place(x=870, y=50)

        self.VectorBasedLabel = Label(self, text='Vector based: ')
        self.VectorBasedLabel.place(x=750, y=80)

        self.CosineLabel = Label(self, text='Cosine measure: ')
        self.Cosine = Text(self, bd=1, width=10, height=1)
        self.CosineTime = Text(self, bd=1, width=10, height=1)
        self.CosineLabel.place(x=650, y=110)
        self.Cosine.place(x=750, y=110)
        self.CosineTime.place(x=870, y=110)

        self.PearsonLabel = Label(self, text='Pearson measure: ')
        self.Pearson = Text(self, bd=1, width=10, height=1)
        self.PearsonTime = Text(self, bd=1, width=10, height=1)
        self.PearsonLabel.place(x=650, y=140)
        self.Pearson.place(x=750, y=140)
        self.PearsonTime.place(x=870, y=140)

        self.setBasedLabel = Label(self, text='Set based: ')
        self.setBasedLabel.place(x=750, y=170)

        self.JaccardLabel = Label(self, text='Jaccard measure: ')
        self.Jaccard = Text(self, bd=1, width=10, height=1)
        self.JaccardTime = Text(self, bd=1, width=10, height=1)
        self.JaccardLabel.place(x=650, y=200)
        self.Jaccard.place(x=750, y=200)
        self.JaccardTime.place(x=870, y=200)

        self.DiceLabel = Label(self, text='Dice measure: ')
        self.Dice = Text(self, bd=1, width=10, height=1)
        self.DiceTime = Text(self, bd=1, width=10, height=1)
        self.DiceLabel.place(x=650, y=230)
        self.Dice.place(x=750, y=230)
        self.DiceTime.place(x=870, y=230)

    def computeSimilarities(self):
        self.TED.delete('1.0', END)
        self.TEDTime.delete('1.0', END)
        self.Cosine.delete('1.0', END)
        self.CosineTime.delete('1.0', END)
        self.Pearson.delete('1.0', END)
        self.PearsonTime.delete('1.0', END)
        self.Jaccard.delete('1.0', END)
        self.JaccardTime.delete('1.0', END)
        self.Dice.delete('1.0', END)
        self.DiceTime.delete('1.0', END)



        sourceArr = str(self.firstSequence.get('0.0', END))[0:-1]
        destinationArr = str(self.secondSequence.get('0.0', END))[0:-1]
        if(self.tokenizationMethod.get() == "Tag-based"):
            tokenizationMethodChosen = tokenization.sequence_to_vector_tag
        elif(self.tokenizationMethod.get() == "Edge-based"):
            tokenizationMethodChosen = tokenization.sequence_to_vector_edge
        else:
            tokenizationMethodChosen = tokenization.sequence_to_vector_allpaths



        similarities, times = similarity.compute_all_similarities(sourceArr,destinationArr,tokenizationMethodChosen)

        self.TED.insert(END, similarities[0])
        self.TEDTime.insert(END, times[0])
        self.Cosine.insert(END, similarities[1])
        self.CosineTime.insert(END, times[1])
        self.Pearson.insert(END, similarities[2])
        self.PearsonTime.insert(END, times[2])
        self.Jaccard.insert(END, similarities[3])
        self.JaccardTime.insert(END, times[3])
        self.Dice.insert(END, similarities[4])
        self.DiceTime.insert(END, times[4])


# Setting the GUI for page 2
class MyWindow2(Page):
    # GUI Components
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


# Managing both pages
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = MyWindow1(self)
        p2 = MyWindow2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Similarity Comparison", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Search", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1200x700+10+10")

    root.mainloop()
