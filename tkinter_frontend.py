from tkinter import *
from tkinter import filedialog
from dataML import DataML

class FrontEnd:
    """
    Frontend class to display tkinter
    """
    def __init__(self):
        self.window = Tk()
        self.fileName = StringVar()
        self.processingStatus = StringVar()
        self.results = StringVar()
        self.modelPrediction = IntVar()
        self.openMainMenu()

    def openMainMenu(self):
        """
        Main function
        """
        window = self.window
        # to bring window to foreground
        window.lift()
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)

        mainLabel = Label(window, text="Audio Emotion Predictor App", fg='black', font=("Bahnschrift", 32))
        mainLabel.pack(fill="x", expand=False, side="top", padx=(5, 5), pady=(5, 5))

        ### WIDGET 1 ###
        mainFrame = LabelFrame(window, text="Step 1: Upload File", fg='green', font=("Bahnschrift", 20), labelanchor="n")
        mainFrame.pack(fill="both", expand=False, padx=(5, 5), pady=(5, 5))

        # WIDGET 1.1 #
        fileFrame = Frame(mainFrame)
        fileFrame.pack(fill="both", expand=True, side="top")
        fileSelectLabel = Label(fileFrame, text="Select A File", fg='black', font=("Bahnschrift", 16))
        fileSelectLabel.pack(fill="x", expand=False, side="left")
        fileSelectButton = Button(fileFrame, text="Choose an audio file", command=self.selectFile, font=("Bahnschrift", 16))
        fileSelectButton.pack(fill="none", expand=False, side="right", padx=(5, 5))

        ### WIDGET 2 ###
        afterUploadFrame = LabelFrame(window, text="Step 2: Verify File", fg='green', font=("Bahnschrift", 20), labelanchor="n")
        afterUploadFrame.pack(fill="both", expand=False, padx=(5, 5), pady=(5, 5))

        # WIDGET 2.1 #
        processFrame = Frame(afterUploadFrame)
        processFrame.pack(fill="both", expand=True, side="top")
        fileSelectLabel = Label(processFrame, textvariable=self.fileName, fg='black', font=("Bahnschrift", 16), wraplength=300)
        fileSelectLabel.pack(fill="x", expand=False, side="left")
        submitFileButton = Button(processFrame, text="Submit File", command=self.submitToProcess, font=("Bahnschrift", 16))
        submitFileButton.pack(fill="none", expand=False, side="right", padx=(5, 5))
        removeFileButton = Button(processFrame, text="Remove File", command=self.removeFile, font=("Bahnschrift", 16))
        removeFileButton.pack(fill="none", expand=False, side="right", padx=(5, 5))

        ### WIDGET 3 ###
        processFrame = LabelFrame(window, text="Step 3: Processing File", fg='green', font=("Bahnschrift", 20), labelanchor="n")
        processFrame.pack(fill="both", expand=False, padx=(5, 5), pady=(5, 5))

        # WIDGET 3.1 #
        processingFrame = Frame(processFrame)
        processingFrame.pack(fill="both", expand=True, side="top")
        processingLabel = Label(processFrame, textvariable=self.processingStatus, fg='black', font=("Bahnschrift", 16))
        processingLabel.pack(fill="x", expand=False, side="left")

        ### WIDGET 4 ###
        predictionFrame = LabelFrame(window, text="Step 4: Model Results", fg='green', font=("Bahnschrift", 20), labelanchor="n")
        predictionFrame.pack(fill="both", expand=False, padx=(5, 5), pady=(5, 5))

        # WIDGET 4.1 #
        resultFrame = Frame(predictionFrame)
        resultFrame.pack(fill="both", expand=True, side="top")
        radioAngry = Radiobutton(resultFrame, text="Angry", variable=self.modelPrediction, value=1, font=("Bahnschrift", 16), fg="white", state=DISABLED, indicatoron=False)
        radioHappy = Radiobutton(resultFrame, text="Happy", variable=self.modelPrediction, value=2, font=("Bahnschrift", 16), fg="white", state=DISABLED, indicatoron=False)
        radioNeutral = Radiobutton(resultFrame, text="Neutral", variable=self.modelPrediction, value=3, font=("Bahnschrift", 16), fg="white", state=DISABLED, indicatoron=False)
        radioSad = Radiobutton(resultFrame, text="Sad", variable=self.modelPrediction, value=4, font=("Bahnschrift", 16), fg="white", state=DISABLED, indicatoron=False)
        
        radioAngry.pack(fill="x", expand=True, side="left")
        radioHappy.pack(fill="x", expand=True, side="left")
        radioNeutral.pack(fill="x", expand=True, side="left")
        radioSad.pack(fill="x", expand=True, side="left")

        # WIDGET 4.2 #
        resultWordFrame = Frame(predictionFrame)
        resultWordFrame.pack(fill="both", expand=True, side="top")
        resultLabel = Label(resultWordFrame, textvariable=self.results, fg='red', font=("Bahnschrift", 72))
        resultLabel.pack(fill="x", expand=False, side="top")

        # other properties
        window.minsize(575, 575)
        window.protocol("WM_DELETE_WINDOW", self.on_closing) # if setup is closed directly
        # window.iconphoto(False, PhotoImage(file='favicon.png'))
        window.title('Audio Emotion Predictor')
        window.geometry("600x600+400+200")
        window.mainloop()

    def selectFile(self):
        fileName = filedialog.askopenfilename(initialdir="/", title="Select An Audio File", filetypes=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.fileName.set(fileName)
    
    def removeFile(self):
        self.results.set("")
        self.modelPrediction.set("")
        self.processingStatus.set("")
        self.fileName.set("")

    def getPredictions(self):
        self.modelPrediction.set(self.dmlObject.getPredictionResults())
        self.processingStatus.set("Emotion Predicted Below")
        predictionMapper = {1: "Angry", 2: "Happy", 3: "Neutral", 4: "Sad"}
        self.results.set(predictionMapper[self.modelPrediction.get()])

    def submitToProcess(self):
        self.results.set("")
        self.modelPrediction.set("")
        if self.fileName.get() == "":
            self.processingStatus.set("No file selected!")
        else:
            self.processingStatus.set("Processing... Please Wait!")
            self.dmlObject = DataML(self.fileName.get())
            self.window.after(250, self.getPredictions) # gives some time before calling predictions on the newly created object

    def on_closing(self):
        """
        Closes window if the "X" is clicked.
        """
        self.window.destroy()

if __name__ == "__main__":
    FrontEnd()