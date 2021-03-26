import differencing
import os
import editScript as ed
import XML_Writer as xml
import patching as patch
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MyWindow1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.medicalSimilarity = IntVar()
        self.firstSequenceLabel = Label(self, text='First sequence')
        self.secondSequenceLabel = Label(self, text='Second sequence')
        self.distanceArrayLabel = Label(self, text='Distance Array')
        self.editScriptLabel = Label(self, text='Edit Scripts')
        self.editDistanceLabel = Label(self, text='Edit distance: ')
        self.similarityMeasureLabel = Label(self, text='Similarity: ')

        self.distanceArrayContainer = tk.Frame(self, bd=1, width=100, height=10, relief="sunken")

        # Horizontal (x) Scroll bar
        self.xscrollbar = Scrollbar(self.distanceArrayContainer, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)

        # Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(self.distanceArrayContainer)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        self.firstSequence = Text(self, bd=3, width=50, height=1)
        self.secondSequence = Text(self, bd=3, width=50, height=1)
        self.distanceArray = Text(self.distanceArrayContainer, width=100, height=10, wrap="none", xscrollcommand=self.xscrollbar.set,
                                  yscrollcommand=self.yscrollbar.set)
        self.distanceArray.pack()
        self.editScript = Text(self, width=100, height=10, wrap="none")
        self.editDistance = Text(self, bd=1, width=10, height=1)
        self.similarityMeasure = Text(self, bd=1, width=10, height=1)

        # Configure the scrollbar
        self.xscrollbar.config(command=self.distanceArray.xview)
        self.yscrollbar.config(command=self.distanceArray.yview)

        self.firstSequenceLabel.place(x=100, y=50)
        self.firstSequence.place(x=200, y=50)
        self.secondSequenceLabel.place(x=100, y=100)
        self.secondSequence.place(x=200, y=100)

        self.getDistanceArrButton = Button(self, text='Get Distance Array', command=self.getDistanceArray)
        self.getEditScriptsButton = Button(self, text='Get Edit Scripts', command=self.getEditScripts)
        self.saveToXMLButton = Button(self, text='Save to XML', command=self.saveToXML)
        self.clearSequences = Button(self, text='Clear', command=self.clearSequences)
        self.medicalSimilarityButton = Checkbutton(self, text="Medical Similarity", variable=self.medicalSimilarity)
        self.button_explore_source = Button(self, text="Browse Files", command=lambda: self.browseFiles(destination=0))
        self.button_explore_destination = Button(self, text="Browse Files",
                                                 command=lambda: self.browseFiles(destination=1))

        self.getDistanceArrButton.place(x=100, y=150)
        self.getEditScriptsButton.place(x=250, y=150)
        self.saveToXMLButton.place(x=400, y=150)
        self.clearSequences.place(x=550, y=150)
        self.medicalSimilarityButton.place(x=700, y=75)
        self.button_explore_source.place(x=650, y=50)
        self.button_explore_destination.place(x=650, y=100)

        self.editDistanceLabel.place(x=600, y=150)
        self.editDistance.place(x=680, y=150)
        self.similarityMeasureLabel.place(x=800, y=150)
        self.similarityMeasure.place(x=880, y=150)

        self.distanceArrayLabel.place(x=100, y=200)
        self.distanceArrayContainer.place(x=200, y=200)
        self.editScriptLabel.place(x=100, y=400)
        self.editScript.place(x=200, y=400)

    def browseFiles(self, destination=0):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.xml*"),
                                                         ("all files",
                                                          "*.*")))
        # Change label contents
        sequence = xml.sequenceExtraction(filename)
        if destination:
            self.secondSequence.insert(END, sequence)
        else:
            self.firstSequence.insert(END, sequence)

    def getDistanceArray(self):
        self.distanceArray.delete('1.0', END)
        self.editDistance.delete('0.0', END)
        self.similarityMeasure.delete('0.0', END)
        A = str(self.firstSequence.get('0.0', END))[0:-1]
        B = str(self.secondSequence.get('0.0', END))[0:-1]
        distArr = differencing.differenceCalculation(A.upper(), B.upper(),
                                                     medicalSimilarity=self.medicalSimilarity.get())
        self.distanceArray.insert(END, differencing.prettyPrint(A, B, distArr))
        editdistance = distArr[distArr.shape[0] - 1][distArr.shape[1] - 1]
        self.editDistance.insert(END, editdistance)
        similarity = (1 - (editdistance) / (len(A) + len(B)))
        self.similarityMeasure.insert(END, similarity)

    def getEditScripts(self):
        self.getDistanceArray()
        self.editScript.delete('1.0', 'end')
        A = str(self.firstSequence.get('0.0', END))[0:-1]
        B = str(self.secondSequence.get('0.0', END))[0:-1]
        distArr = differencing.differenceCalculation(A.upper(), B.upper(),
                                                     medicalSimilarity=self.medicalSimilarity.get())
        editScripts = ed.getEditScripts(distArr, A.upper(), B.upper(),
                                        medicalSimilarity=self.medicalSimilarity.get(),
                                        operations=1)
        for es in editScripts:
            self.editScript.insert(END, es)
            self.editScript.insert(END, "\n")

    def saveToXML(self):
        self.getDistanceArray()
        self.editScript.delete('1.0', 'end')
        A = str(self.firstSequence.get('0.0', END))[0:-1]
        B = str(self.secondSequence.get('0.0', END))[0:-1]
        distArr = differencing.differenceCalculation(A.upper(), B.upper(),
                                                     medicalSimilarity=self.medicalSimilarity.get())
        editScripts = ed.getEditScripts(distArr, A.upper(), B.upper(),
                                        medicalSimilarity=self.medicalSimilarity.get(),
                                        operations=1)
        for es in editScripts:
            self.editScript.insert(END, es)
            self.editScript.insert(END, "\n")
        xml.differencing(editScripts)

    def clearSequences(self):
        self.firstSequence.delete('0.0', END)
        self.secondSequence.delete('0.0', END)
        self.distanceArray.delete('0.0', END)
        self.editDistance.delete('0.0', END)
        self.editScript.delete('0.0', 'end')


class MyWindow2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.sourceSequenceLabel = Label(self, text='Source sequence')
        self.destinationSequenceLabel = Label(self, text='Destination sequence')
        self.differenceFileLabel = Label(self, text='Difference File Name')

        self.sourceSequence = Text(self, bd=3, width=50, height=1)
        self.destinationSequence = Text(self, bd=3, width=50, height=1)
        self.differenceFile = Text(self, bd=3, width=50, height=1)

        self.sourceSequenceLabel.place(x=100, y=50)
        self.sourceSequence.place(x=250, y=50)
        self.destinationSequenceLabel.place(x=100, y=100)
        self.destinationSequence.place(x=250, y=100)
        self.differenceFileLabel.place(x=100, y=150)
        self.differenceFile.place(x=250, y=150)

        self.patchForward = Button(self, text='Patch Source to Destination', command=self.patchforward)
        self.patchReverse = Button(self, text='Patch Destination to Source', command=self.patchreverse)
        self.button_explore = Button(self, text="Browse Difference File", command=self.browseFiles)

        self.patchForward.place(x=670, y=50)
        self.patchReverse.place(x=670, y=100)
        self.button_explore.place(x=670, y=150)

    def patchforward(self):
        self.destinationSequence.delete('1.0', END)
        src = str(self.sourceSequence.get('0.0', END))[0:-1]
        file = str(self.differenceFile.get('0.0', END))[0:-1]
        self.destinationSequence.insert(END, patch.patch(file, src.upper(), 0))

    def patchreverse(self):
        self.sourceSequence.delete('1.0', END)
        dest = str(self.destinationSequence.get('0.0', END))[0:-1]
        file = str(self.differenceFile.get('0.0', END))[0:-1]
        self.sourceSequence.insert(END, patch.patch(file, dest.upper(), 1))

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                              filetypes=(("Text files", "*.xml*"), ("all files", "*.*")))

        # Change label contents
        self.differenceFile.insert(END, filename)


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

        b1 = tk.Button(buttonframe, text="DNA Sequence Differencing", command=p1.lift)
        b2 = tk.Button(buttonframe, text="XML Tree Patching", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1200x700+10+10")
    root.mainloop()
