from tkinter import * 
import pyaudio
import wave
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

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



def check_mono(signal):
	if signal.ndim == 1:
		return True
	else:
		return False

def convert_to_mono(signal):
	#if the signal is already mono, we return the original signal
	if check_mono(signal) == True:
		return signal
	else:
		#create a new numpy array filled with 0s with the length of the original signal
		new_array = np.zeros(len(signal))
		#we'll add the average of the two stereo channels to our new array
		for i in range(len(signal)):
			new_array[i] += signal[i][0]/2 + signal[i][1]/2
		#return our newly created mono signal
		return new_array

def cut_silence(data, threshold = 0.1 , audio_length = 132300):
	min_val = threshold * max(abs(data))
	start_audio_pos = 0
	end_audio_pos = 0

	for i in range(len(data)):
		if data[i] > min_val:
			start_audio_pos = i
			break

	#Here we do the same thing, but we start at the end
	for i in range(len(data)-1, 0, -1):
		if data[i] > min_val:
			end_audio_pos = i+1
			break
  
	#Cut out the silence from the data
	data = data[start_audio_pos : end_audio_pos]
	print(data.shape)
	padding_length = audio_length - len(data)
	if padding_length % 2 == 0:
		padding_length = int(padding_length/2)
		data = np.pad(data, (padding_length, padding_length))
	else:
		padding_length = int(padding_length/2)
		data = np.pad(data, (padding_length, padding_length+1))
	
	return data


import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

#OPEN MODEL
with open('model.pkl', 'rb') as f:
	clf2 = pickle.load(f)


#RECORDING OF THE AUDIO
def record_audio():
	fs = 44100	# Sample rate
	seconds = 3	 # Duration of recording

	my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	sd.wait()  # Wait until recording is finished
	my_recording = convert_to_mono(my_recording)
	my_recording = cut_silence(my_recording)
	
	arr = []
	arr.append(my_recording)
	arr = np.array(arr)
	print(arr.shape)
	
	solution = clf2.predict(arr)
	
	
	#TRY TO ESTIMATE THE NUMBER
	#UPDATE THE NUMBER
	
	
	#write('output.wav', fs, myrecording)  # Save as WAV file 
	#print("Finished recording :)")
	buttons[current_button.current_button_col][current_button.current_button_row]['text'] = solution

button_rec = Button(root, text='Record audio', command=record_audio)
button_rec.place(x=800, y=400)





root.mainloop()