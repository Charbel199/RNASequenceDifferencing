from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from similarityMeasures import similarity,tokenization
from data import parser
from search import searchSimilarSequences, TFIDF
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
        self.techniqueOptions = OptionMenu(self, self.technique, "TED", "Multiset/vector-based").place(x=250, y=140)
        self.tokenizationSingleMethod = StringVar(self)
        self.tokenizationSingleMethod.set("Tag-based")  # default value
        self.tokenizationSingleMethodOptions = OptionMenu(self, self.tokenizationSingleMethod, "Tag-based", "Edge-based",
                                                    "All Paths").place(x=250, y=180)
        self.similarityMethod = StringVar(self)
        self.similarityMethod.set("ED")  # default value

        self.similarityMethodOptions = OptionMenu(self, self.similarityMethod, "ED", "Jaccard",
                                                    "Dice","Cosine","Pearson").place(x=250, y=220)
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
        self.singleMethod.delete('1.0', END)
        self.singleMethodTime.delete('1.0', END)

        sourceArr = str(self.firstSequence.get('0.0', END))[0:-1]
        destinationArr = str(self.secondSequence.get('0.0', END))[0:-1]
        technique = self.technique.get()
        tokenizationMethod = self.tokenizationSingleMethod.get()
        similarityChosenMethod = self.similarityMethod.get()



        if(tokenizationMethod == "Tag-based"):
            tokenizationMethod = tokenization.sequence_to_vector_tag
        elif(tokenizationMethod == "Edge-based"):
            tokenizationMethod = tokenization.sequence_to_vector_edge
        else:
            tokenizationMethod = tokenization.sequence_to_vector_allpaths


        if (similarityChosenMethod ==  "ED"):
            similarityChosenMethod = similarity.TEDSimilarity_measure
            self.technique.set("TED")
        elif (similarityChosenMethod ==  "Jaccard"):
            similarityChosenMethod = similarity.multiset_jackard_measure
        elif(similarityChosenMethod ==  "Dice"):
            similarityChosenMethod = similarity.multiset_dice_measure
        elif(similarityChosenMethod ==  "Cosine"):
            similarityChosenMethod = similarity.vector_cosine_measure
        else:
            similarityChosenMethod = similarity.vector_pearsoncorrelation_measure

        if (technique == "TED"):
            similarityChosenMethod = similarity.TEDSimilarity_measure
            self.similarityMethod.set("ED")

        similarityMeasure, timeMeasure = similarity.compute_one_similarity(sourceArr,destinationArr,tokenizationMethod,similarityChosenMethod)
        self.singleMethod.insert(END, similarityMeasure)
        self.singleMethodTime.insert(END, timeMeasure)






# Setting the GUI for page 2
class MyWindow2(Page):
    # GUI Components
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.sequenceLabel = Label(self, text='Sequence')
        self.sequence = Text(self, bd=3, width=50, height=1)
        self.sequenceLabel.place(x=100, y=50)
        self.sequence.place(x=200, y=50)

        self.searchButton = Button(self, text="Search",command=self.searchSimilarSequence).place(x=650,y=48)


        self.numberOfSequencesToLookInLabel = Label(self, text='Number of sequences to search:')
        self.numberOfSequencesToLookIn = Text(self, bd=3, width=10, height=1)
        self.numberOfSequencesToLookInLabel.place(x=630,y=28)
        self.numberOfSequencesToLookIn.place(x=710,y=50)

        self.numberOfOutputsLabel = Label(self, text='Number of outputs:')
        self.numberOfOutputs = Text(self, bd=3, width=10, height=1)
        self.numberOfOutputsLabel.place(x=650, y=78)
        self.numberOfOutputs.place(x=710, y=100)

        #options
        self.technique = StringVar(self)
        self.technique.set("TED")  # default value
        self.techniqueOptions = OptionMenu(self, self.technique, "TED", "Multiset/vector-based").place(x=200, y=80)

        self.preprocessButton = Button(self, text="Preprocess Database", command=self.preprocessDatabase).place(x=60, y=120)
        self.deletePreprocessButton = Button(self, text="Delete preprocessed Database", command=self.deletePreprocessDatabase).place(x=25, y=150)
        self.tokenizationSingleMethod = StringVar(self)
        self.tokenizationSingleMethod.set("Tag-based")  # default value
        self.tokenizationSingleMethodOptions = OptionMenu(self, self.tokenizationSingleMethod, "Tag-based",
                                                          "Edge-based",
                                                          "All Paths").place(x=200, y=120)
        self.similarityMethod = StringVar(self)
        self.similarityMethod.set("ED")  # default value

        self.similarityMethodOptions = OptionMenu(self, self.similarityMethod, "ED", "Jaccard",
                                                  "Dice", "Cosine", "Pearson").place(x=200, y=160)
        self.TFIDF = StringVar(self)
        self.TFIDF.set("TF")  # default value
        self.TFIDFOptions = OptionMenu(self, self.TFIDF, "TF", "IDF", "TF-IDF").place(x=500, y=80)

        self.TFMethodLabel = Label(self, text='TF Method').place(x=420, y=120)
        self.IDFMethodLabel = Label(self, text='IDF Method').place(x=420, y=160)

        self.TFMethod = StringVar(self)
        self.TFMethod.set("Simple TF")  # default value
        self.TFMethodOptions = OptionMenu(self, self.TFMethod, "Simple TF", "TF over maximum TF", "Logarithmic TF").place(x=500, y=118)

        self.IDFMethod = StringVar(self)
        self.IDFMethod.set("Logarithmic IDF")  # default value
        self.IDFMethodOptions = OptionMenu(self, self.IDFMethod, "Logarithmic IDF", "Logarithmic IDF plus one", "Absolute Logarithmic IDF").place(x=500, y=158)


        ##Search results
        self.searchResultsContainer = tk.Frame(self, bd=1, width=50, height=10, relief="sunken")
        # Horizontal (x) Scroll bar
        self.xscrollbar2 = Scrollbar(self.searchResultsContainer, orient=HORIZONTAL)
        self.xscrollbar2.pack(side=BOTTOM, fill=X)
        # Vertical (y) Scroll Bar
        self.yscrollbar2 = Scrollbar(self.searchResultsContainer)
        self.yscrollbar2.pack(side=RIGHT, fill=Y)
        self.searchResults = Text(self.searchResultsContainer, width=60, height=10, wrap="none",
                                     xscrollcommand=self.xscrollbar2.set,
                                     yscrollcommand=self.yscrollbar2.set)
        self.searchResults.pack()
        self.xscrollbar2.config(command=self.searchResults.xview)
        self.yscrollbar2.config(command=self.searchResults.yview)
        self.searchResultsContainer.place(x=200, y=200)

        self.singleSearchTimeLabel = Label(self, text='Time elapsed:')
        self.singleSearchTime = Text(self, bd=3, width=10, height=1)
        self.singleSearchTimeLabel.place(x=710, y=200)
        self.singleSearchTime.place(x=710, y=230)

        self.wasItPreprocessedLabel = Label(self, text=' ')
        self.wasItPreprocessedLabel.place(x=700, y=255)






        ##Databse of sequences
        self.sequenceDatabaseContainer = tk.Frame(self, bd=1, width=50, height=10, relief="sunken")
        # Horizontal (x) Scroll bar
        self.xscrollbar = Scrollbar(self.sequenceDatabaseContainer, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        # Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(self.sequenceDatabaseContainer)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.sequenceDatabase = Text(self.sequenceDatabaseContainer, width=50, height=10, wrap="none",
                               xscrollcommand=self.xscrollbar.set,
                               yscrollcommand=self.yscrollbar.set)
        self.sequenceDatabase.pack()
        self.xscrollbar.config(command=self.sequenceDatabase.xview)
        self.yscrollbar.config(command=self.sequenceDatabase.yview)
        self.sequenceDatabaseContainer.place(x=850, y=50)
        self.numberOfSequencesToShowLabel = Label(self, text='Show:')
        self.numberOfSequencesToShow = Text(self, bd=3, width=10, height=1)
        self.numberOfSequencesToShowLabel.place(x=855, y=250)
        self.numberOfSequencesToShow.place(x=900, y=250)
        self.fileNameLabel = Label(self, text='File:')
        self.fileName = Text(self, bd=3, width=20, height=1)
        self.fileName.insert('0.0',"humanRNA.fa")
        self.fileNameLabel.place(x=855, y=290)
        self.fileName.place(x=900, y=290)
        self.initializeDatabaseButton = Button(self, text="Initialize Database", command=self.initializeDatabase).place(x=1000, y=250)

    def searchSimilarSequence(self):
        self.searchResults.delete('1.0', 'end')
        self.singleSearchTime.delete('1.0', 'end')
        global sequences
        results = []
        times = []
        technique = self.technique.get()
        tokenizationMethod = self.tokenizationSingleMethod.get()
        similarityChosenMethod = self.similarityMethod.get()
        TFIDFoption = self.TFIDF.get()
        TF_Method = self.TFMethod.get()
        IDF_Method = self.IDFMethod.get()
        if( TFIDFoption == "TF"):
            TF=1
            IDF=0
        elif( TFIDFoption == "IDF"):
            TF = 0
            IDF = 1
        else:
            TF = 1
            IDF = 1

        if(TF_Method == "TF over maximum TF"):
            TF_Method = TFIDF.TF_over_max
        elif(TF_Method == "Logarithmic TF"):
            TF_Method = TFIDF.TF_log
        else:
            TF_Method = TFIDF.TF_normal

        if (IDF_Method =="Logarithmic IDF plus one"):
            IDF_Method = TFIDF.IDF_log_plus_one
        elif (IDF_Method == "Absolute Logarithmic IDF"):
            IDF_Method = TFIDF.IDF_absolute_log
        else:
            IDF_Method = TFIDF.IDF_log


        if (tokenizationMethod == "Tag-based"):
            tokenizationMethod = tokenization.sequence_to_vector_tag
        elif (tokenizationMethod == "Edge-based"):
            tokenizationMethod = tokenization.sequence_to_vector_edge
        else:
            tokenizationMethod = tokenization.sequence_to_vector_allpaths

        if (similarityChosenMethod == "ED"):
            similarityChosenMethod = similarity.TEDSimilarity_measure
            self.technique.set("TED")
        elif (similarityChosenMethod == "Jaccard"):
            similarityChosenMethod = similarity.multiset_jackard_measure
        elif (similarityChosenMethod == "Dice"):
            similarityChosenMethod = similarity.multiset_dice_measure
        elif (similarityChosenMethod == "Cosine"):
            similarityChosenMethod = similarity.vector_cosine_measure
        else:
            similarityChosenMethod = similarity.vector_pearsoncorrelation_measure

        if (technique == "TED"):
            similarityChosenMethod = similarity.TEDSimilarity_measure
            self.similarityMethod.set("ED")

        try:
            numberOfSequences = int(self.numberOfSequencesToLookIn.get('0.0', END))
        except:
            numberOfSequences = 100

        try:
            numberOfOutputs = int(self.numberOfOutputs.get('0.0', END))
        except:
            numberOfOutputs = 3
        
        global processed_sequences_database
        if("processed_sequences_database" not in globals()):
            processed_sequences_database = []
            if (technique == "TED" or similarityChosenMethod == "ED"):
                self.wasItPreprocessedLabel.config(text="No preprocessing")
            else:
                self.wasItPreprocessedLabel.config(text="Preprocessing Included")
        else:
            if (technique == "TED" or similarityChosenMethod == "ED"):
                self.wasItPreprocessedLabel.config(text="No preprocessing")
            else:
                if(len(processed_sequences_database) != numberOfSequences):
                    self.wasItPreprocessedLabel.config(text = "Preprocessing Included")
                else:
                    self.wasItPreprocessedLabel.config(text="Preprocessing NOT Included")
        searchSimilarSequences.IR_Method(sequences,
                                         self.sequence.get('0.0', END),
                                         results,
                                         times,
                                         tokenizationMethod,
                                         similarityChosenMethod,
                                         TF_Method,
                                         IDF_Method,
                                         processed_sequences_database = processed_sequences_database,
                                         numberOfOutputs = numberOfOutputs,
                                         numberOfSequencesToSearch= numberOfSequences,
                                         TF = TF,
                                         IDF = IDF)

        for i,resultDict in enumerate(results):
            if(i == 0):
                self.searchResults.insert(END, "Top " +str(numberOfOutputs)+ " results:")
                self.searchResults.insert(END, "\n")
            else:
                self.searchResults.insert(END, "\nLowest " +str(numberOfOutputs)+ " results:")
                self.searchResults.insert(END, "\n")

            for key in resultDict:
                self.searchResults.insert(END, key)
                self.searchResults.insert(END, " : ")
                self.searchResults.insert(END, resultDict[key])
                self.searchResults.insert(END, "\n")

        self.singleSearchTime.insert(END, times[0])
    def initializeDatabase(self):
        self.sequenceDatabase.delete('1.0', 'end')
        global sequences
        try:
            sequences = parser.parse_fa(self.fileName.get('0.0', END))
        except:
            sequences = parser.parse_fa('humanRNA.fa')
            self.fileName.delete('1.0', 'end')
            self.fileName.insert('0.0', "humanRNA.fa")
        try:
            sequencesToShow = sequences[0:int(self.numberOfSequencesToShow.get('0.0', END))]
        except:
            sequencesToShow = []


        for sequence in sequencesToShow:
            self.sequenceDatabase.insert(END, sequence)
            self.sequenceDatabase.insert(END, "\n")

    def preprocessDatabase(self):
        global processed_sequences_database
        global sequences
        processed_sequences_database = []
        try:
            numberOfSequences = int(self.numberOfSequencesToLookIn.get('0.0', END))
        except:
            numberOfSequences = 100
        sequencesDatabase = sequences[0:numberOfSequences]

        tokenizationMethod = self.tokenizationSingleMethod.get()
        if (tokenizationMethod == "Tag-based"):
            tokenizationMethod = tokenization.sequence_to_vector_tag
        elif (tokenizationMethod == "Edge-based"):
            tokenizationMethod = tokenization.sequence_to_vector_edge
        else:
            tokenizationMethod = tokenization.sequence_to_vector_allpaths
        if (not processed_sequences_database):
            processed_sequences_database = list(map(tokenizationMethod, sequencesDatabase))
    def deletePreprocessDatabase(self):
        global processed_sequences_database
        processed_sequences_database = []
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
