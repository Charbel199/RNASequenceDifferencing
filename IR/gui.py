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

        self.technique = StringVar(self)
        self.technique.set("TED")  # default value
        self.techniqueOptions = OptionMenu(self, self.technique, "TED", "Multiset/vector-based").place(x=100, y=140)
        self.tokenizationSingleMethod = StringVar(self)
        self.tokenizationSingleMethod.set("Tag-based")  # default value
        self.tokenizationSingleMethodOptions = OptionMenu(self, self.tokenizationSingleMethod, "Tag-based", "Edge-based",
                                                    "All Paths").place(x=100, y=180)
        self.similarityMethod = StringVar(self)
        self.similarityMethod.set("ED")  # default value
        self.similarityMethodOptions = OptionMenu(self, self.similarityMethod, "ED", "Jaccard",
                                                    "Dice","Cosine","Pearson").place(x=100, y=220)
        self.computeSingleSimilaritiyButton = Button(self, text='Compute similarity', command=self.computeSingleSimilarity)
        self.computeSingleSimilaritiyButton.place(x=450, y=140)

        self.similairtySingleLabel = Label(self, text='Similarity')
        self.timeSingleLabel = Label(self, text='Time (s)')
        self.similairtySingleLabel.place(x=450, y=180)
        self.timeSingleLabel.place(x=570, y=180)


        self.singleMethod = Text(self, bd=1, width=10, height=1)
        self.singleMethodTime = Text(self, bd=1, width=10, height=1)
        self.singleMethod.place(x=450, y=210)
        self.singleMethodTime.place(x=570, y=210)


        self.computeSimilaritiesButton = Button(self, text='Compute All Similarities', command=self.computeSimilarities)
        self.computeSimilaritiesButton.place(x=100, y=380)

        self.tokenizationMethod = StringVar(self)
        self.tokenizationMethod.set("Tag-based")  # default value
        self.tokenizationMethodOptions = OptionMenu(self,  self.tokenizationMethod, "Tag-based", "Edge-based", "All Paths").place(x=250,y=378)

        self.plotRadarsButton = Button(self, text='Graph', command=self.plotRadar)
        self.plotRadarsButton.place(x=380, y=380)

        self.similairtyLabel =  Label(self, text='Similarity')
        self.timeLabel = Label(self, text='Time (s)')
        self.similairtyLabel.place(x=200, y=420)
        self.timeLabel.place(x=320, y=420)

        self.TEDLabel = Label(self, text='TED: ')
        self.TED = Text(self, bd=1, width=10, height=1)
        self.TEDTime = Text(self, bd=1, width=10, height=1)
        self.TEDLabel.place(x=100, y=450)
        self.TED.place(x=200, y=450)
        self.TEDTime.place(x=320, y=450)

        self.VectorBasedLabel = Label(self, text='Vector based: ')
        self.VectorBasedLabel.place(x=200, y=480)

        self.CosineLabel = Label(self, text='Cosine measure: ')
        self.Cosine = Text(self, bd=1, width=10, height=1)
        self.CosineTime = Text(self, bd=1, width=10, height=1)
        self.CosineLabel.place(x=100, y=510)
        self.Cosine.place(x=200, y=510)
        self.CosineTime.place(x=320, y=510)

        self.PearsonLabel = Label(self, text='Pearson measure: ')
        self.Pearson = Text(self, bd=1, width=10, height=1)
        self.PearsonTime = Text(self, bd=1, width=10, height=1)
        self.PearsonLabel.place(x=100, y=540)
        self.Pearson.place(x=200, y=540)
        self.PearsonTime.place(x=320, y=540)

        self.setBasedLabel = Label(self, text='Set based: ')
        self.setBasedLabel.place(x=200, y=570)

        self.JaccardLabel = Label(self, text='Jaccard measure: ')
        self.Jaccard = Text(self, bd=1, width=10, height=1)
        self.JaccardTime = Text(self, bd=1, width=10, height=1)
        self.JaccardLabel.place(x=100, y=600)
        self.Jaccard.place(x=200, y=600)
        self.JaccardTime.place(x=320, y=600)

        self.DiceLabel = Label(self, text='Dice measure: ')
        self.Dice = Text(self, bd=1, width=10, height=1)
        self.DiceTime = Text(self, bd=1, width=10, height=1)
        self.DiceLabel.place(x=100, y=630)
        self.Dice.place(x=200, y=630)
        self.DiceTime.place(x=320, y=630)

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



    def plotRadar(self):

        from math import pi
        figure = plt.Figure(figsize=(3.2, 3), dpi=100)
        figure.patch.set_facecolor('#F0F0F0')
        ax = figure.add_subplot(111 ,polar=True)
        categories = ["TED", "Cosine", "Pearson", "Jaccard", "Dice"]

        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values = []
        values.append(float(self.TED.get("1.0",'end-1c')))
        values.append(float(self.Cosine.get("1.0",'end-1c')))
        values.append(float(self.Pearson.get("1.0",'end-1c')))
        values.append(float(self.Jaccard.get("1.0",'end-1c')))
        values.append(float(self.Dice.get("1.0",'end-1c')))
        N = len(values)
        values += values[:1]
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        # Draw one axe per variable + add labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        # Draw ylabels
        ax.set_rlabel_position(0)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels(["-1", "-0.5", "0", "0.5", "1"], color="red", size=7)
        ax.set_ylim(-1, 1)

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid')

        # Fill area
        ax.fill(angles, values, 'b', alpha=0.1)

        global chart_type
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().place(x=500, y=390)


    def computeSingleSimilarity(self):
        pass




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
        b2 = tk.Button(buttonframe, text="Search", command=lambda:[p2.lift(),chart_type.get_tk_widget().place_forget()])

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1200x700+10+10")

    root.mainloop()
