from tkinter import * 
import pyaudio
import wave
import sounddevice as sd
from scipy.io.wavfile import write

root = Tk()
root.title('Sudoku')
root.state('zoomed')


#audio MNIST https://www.kaggle.com/alanchn31/free-spoken-digits
# https://github.com/at16k/at16k

### CREATING THE GRID OF THE SUDOKU
global buttons
buttons = []

class Current():
	def __init__(self):
		self.current_button = (0,0)
		self.current_button_col = 0
		self.current_button_row = 0
	def update(self, i, j):
		self.current_button = (i, j)
		self.current_button_col = i
		self.current_button_row = j

current_button = Current()

def onClick(i):
	current_button.update(int(i[0])-1, int(i[1])-1)
	
for i in range(1, 10):
	buttons_column = []
	for j in range(1, 10):
		#b = Tkinter.Button(win, height=10, width=100, command=lambda i=i: onClick(i))
		str_pos = str(i) + str(j)
		b = Button(root, height=4, width=8, text = str((i, j)), command = lambda str_pos=str_pos: onClick(str_pos))
		b.place(x=i*80, y=j*80)
		print(i*80, j*80)
		#b.pack()
		buttons_column.append(b)
	buttons.append(buttons_column)

#column, row
buttons[0][4]['text'] = '1'


#RECORDING OF THE AUDIO
def record_audio():
	fs = 44100  # Sample rate
	seconds = 3  # Duration of recording

	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	sd.wait()  # Wait until recording is finished
	write('output.wav', fs, myrecording)  # Save as WAV file 
	print("Finished recording :)")
	buttons[current_button.current_button_col][current_button.current_button_row]['text'] = "yay"

button_rec = Button(root, text='Record audio', command=record_audio)
button_rec.place(x=800, y=400)





root.mainloop()