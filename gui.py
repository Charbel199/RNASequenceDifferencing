import differencing
import editScript as ed



A = 'zzz'
B = 'abddc'
distArr = differencing.differenceCalculation(A,B)
differencing.prettyPrint(A,B,distArr)
editScripts =ed.getEditScripts(distArr, A, B)

for editScript in editScripts:
    print(editScript)

from tkinter import *

class MyWindow:
    def __init__(self, win):
        self.firstSequenceLabel=Label(win, text='First sequence')
        self.secondSequenceLabel=Label(win, text='Second sequence')
        self.distanceArrayLabel=Label(win, text='Distance Array')
        self.editScriptLabel = Label(win, text='Distance Array')
        self.editDistanceLabel = Label(win, text='Edit distance: ')

        self.firstSequence=Entry(bd=3, width=50)
        self.secondSequence=Entry(bd=3, width=50)
        self.distanceArray=Text(width=100, height=10)
        self.editScript = Text(width=100, height=10)
        self.editDistance = Entry(bd=1, width=10)



        self.firstSequenceLabel.place(x=100, y=50)
        self.firstSequence.place(x=200, y=50)
        self.secondSequenceLabel.place(x=100, y=100)
        self.secondSequence.place(x=200, y=100)

        self.getDistancArrButton=Button(win, text='Get Distance Array', command=self.getDistanceArray)
        self.getEditScriptsButton=Button(win, text='Get Edit Scripts', command=self.getEditScripts)
        self.getDistancArrButton.place(x=100, y=150)
        self.getEditScriptsButton.place(x=250, y=150)

        self.editDistanceLabel.place(x=400,y=150)
        self.editDistance.place(x=480,y=150)

        self.distanceArrayLabel.place(x=100, y=200)
        self.distanceArray.place(x=200, y=200)
        self.editScriptLabel.place(x=100, y=400)
        self.editScript.place(x=200, y=400)
    def getDistanceArray(self):
        self.distanceArray.delete('1.0', END)
        self.editDistance.delete(0, END)
        A=str(self.firstSequence.get())
        B=str(self.secondSequence.get())
        distArr = differencing.differenceCalculation(A, B)
        self.distanceArray.insert(END, distArr)
        self.editDistance.insert(END, distArr[distArr.shape[0]-1][distArr.shape[1]-1])
    def getEditScripts(self):
        self.editScript.delete('1.0', 'end')
        A = str(self.firstSequence.get())
        B = str(self.secondSequence.get())
        distArr = differencing.differenceCalculation(A, B)
        editScripts = ed.getEditScripts(distArr, A, B)
        for es in editScripts:
            self.editScript.insert(END, es)
            self.editScript.insert(END,"\n")

window=Tk()
mywin=MyWindow(window)
window.title('RNA Differencing')
window.geometry("600x600+10+10")
window.mainloop()