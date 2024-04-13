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

        ### WIDGET 1 ###
        mainFrame = LabelFrame(window, text="Upload File", fg='red', font=("Bahnschrift", 16), labelanchor="n")
        mainFrame.pack(fill="both", expand=False)

        # WIDGET 1.1 #
        fileFrame = Frame(mainFrame)
        fileFrame.pack(fill="both", expand=True, side="top")
        fileSelectLabel = Label(fileFrame, text="Select File", fg='black', font=("Bahnschrift", 12))
        fileSelectLabel.pack(fill="x", expand=False, side="left")
        fileSelectButton = Button(fileFrame, text="Choose an audio file", command=self.selectFile)
        fileSelectButton.pack(fill="none", expand=False, side="right")

        ### WIDGET 2 ###
        afterUploadFrame = LabelFrame(window, text="Verify File", fg='red', font=("Bahnschrift", 16), labelanchor="n")
        afterUploadFrame.pack(fill="both", expand=False)

        # WIDGET 2.1 #
        processFrame = Frame(afterUploadFrame)
        processFrame.pack(fill="both", expand=True, side="top")
        fileSelectLabel = Label(processFrame, textvariable=self.fileName, fg='black', font=("Bahnschrift", 12), wraplength=350)
        fileSelectLabel.pack(fill="x", expand=False, side="left")
        submitFileButton = Button(processFrame, text="Submit File", command=self.submitToProcess)
        submitFileButton.pack(fill="none", expand=False, side="right")
        removeFileButton = Button(processFrame, text="Remove File", command=self.removeFile)
        removeFileButton.pack(fill="none", expand=False, side="right")

        ### WIDGET 3 ###
        processFrame = LabelFrame(window, text="Processing File", fg='red', font=("Bahnschrift", 16), labelanchor="n")
        processFrame.pack(fill="both", expand=False)

        # WIDGET 3.1 #
        processingFrame = Frame(processFrame)
        processingFrame.pack(fill="both", expand=True, side="top")
        processingLabel = Label(processFrame, textvariable=self.processingStatus, fg='black', font=("Bahnschrift", 12))
        processingLabel.pack(fill="x", expand=False, side="left")

        ### WIDGET 4 ###
        predictionFrame = LabelFrame(window, text="Model Results", fg='red', font=("Bahnschrift", 16), labelanchor="n")
        predictionFrame.pack(fill="both", expand=False)

        # WIDGET 4.1 #
        resultFrame = Frame(predictionFrame)
        resultFrame.pack(fill="both", expand=True, side="top")
        radioAngry = Radiobutton(resultFrame, text="Angry", variable=self.modelPrediction, value=1, font=("Bahnschrift", 12), fg="white", state=DISABLED, indicatoron=False)
        radioHappy = Radiobutton(resultFrame, text="Happy", variable=self.modelPrediction, value=2, font=("Bahnschrift", 12), fg="white", state=DISABLED, indicatoron=False)
        radioNeutral = Radiobutton(resultFrame, text="Neutral", variable=self.modelPrediction, value=3, font=("Bahnschrift", 12), fg="white", state=DISABLED, indicatoron=False)
        radioSad = Radiobutton(resultFrame, text="Sad", variable=self.modelPrediction, value=4, font=("Bahnschrift", 12), fg="white", state=DISABLED, indicatoron=False)
        
        radioAngry.pack(fill="x", expand=True, side="left")
        radioHappy.pack(fill="x", expand=True, side="left")
        radioNeutral.pack(fill="x", expand=True, side="left")
        radioSad.pack(fill="x", expand=True, side="left")

        # other properties
        window.minsize(550, 575)
        window.protocol("WM_DELETE_WINDOW", self.on_closing) # if setup is closed directly
        # window.iconphoto(False, PhotoImage(file='favicon.png'))
        window.title('Audio Emotion Predictor')
        window.geometry("600x600+400+200")
        window.mainloop()

    def selectFile(self):
        fileName = filedialog.askopenfilename(initialdir="/", title="Select An Audio File", filetypes=(("wav files", "*.wav"), ("mp4 files", "*.mp4")))
        self.fileName.set(fileName)
    
    def removeFile(self):
        self.fileName.set('')

    def submitToProcess(self):
        if self.fileName.get() == "":
            self.processingStatus.set("No file selected!")
        else:
            self.processingStatus.set("Processing")
            dmlObject = DataML()
            self.modelPrediction.set(dmlObject.getPredictionResults())

    def on_closing(self):
        """
        Closes window if the "X" is clicked.
        """
        self.window.destroy()

if __name__ == "__main__":
    FrontEnd()