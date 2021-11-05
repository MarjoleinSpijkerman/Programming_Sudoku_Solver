from tkinter import * 
import pyaudio
import wave
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sklearn 
#from sklearn import hmm
from hmmlearn.hmm import GMMHMM
from librosa.feature import mfcc
import warnings
import os
from hmmlearn import hmm
import numpy as np
from librosa.feature import mfcc
import librosa
import random
import pickle
import tkinter.font as font


root = Tk()
root.title('Sudoku')
root.state('zoomed')


#audio MNIST https://www.kaggle.com/alanchn31/free-spoken-digits
# https://github.com/at16k/at16k


class Sudoku:
	def __init__(self):
		self.sudoku = [[0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0],
					   [0,0,0,0,0,0,0,0,0]]
					   				   
	
	def update_value(self, column, row, value):
		print(row, column)
		print(row+1, column+1)
		self.sudoku[row][column] = int(value)
		print(self.sudoku[row][column])
		self.printSudoku()
		
	def find_possible_digits(self, row, column):
		possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		
		for i in range(9):
			if self.sudoku[row][i] != 0:
				if self.sudoku[row][i] in possible:
					possible.remove(self.sudoku[row][i])

		for i in range(9):
			if self.sudoku[i][column] !=  0:
				if self.sudoku[i][column] in possible:
					possible.remove(self.sudoku[i][column])

		
		r0 = row - row%3
		r1 = r0 + 3
		k0 = column - column%3
		k1 = k0 + 3
		
		while r0 < r1:
			while k0 < k1:
				if self.sudoku[r0][k0] != 0:
					if self.sudoku[r0][k0] in possible:
						possible.remove(self.sudoku[r0][k0])
				k0+=1
			r0+=1

		return possible

	def solve_sudoku_recursion(self, row, column):		 
		if row == 9:
			return True

		if column < 8:
			r = row
			k = column+1

		else:
			r = row+1
			k = 0

		if self.sudoku[row][column] != 0:
			return self.solve_sudoku_recursion(r, k)

		for digit in range(1,10):
			options = self.find_possible_digits(row, column)
			if digit in options:
				self.sudoku[row][column] = digit
				if self.solve_sudoku_recursion(r, k):
					return True
				
			self.sudoku[row][column] = 0


	def solve_sudoku_no_recursion(self):
		while any(0 in sublist for sublist in self.sudoku):
			changes = 0
			for row in range(9):
				for column in range(9):
					if self.sudoku[row][column] == 0:
						possible = self.find_possible_digits(row, column)
						if len(possible) == 1:
							self.sudoku[row][column] = possible[0]
							changes += 1
			if changes == 0:
				break
		if any(0 in sublist for sublist in self.sudoku):
			self.solve_sudoku_recursion(0, 0)
							
	def printSudoku(self):
		print(self.sudoku)
	
	def return_value(self, row, column):
		return self.sudoku[row][column]


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
sudoku = Sudoku()


canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), 
                   borderwidth=0, highlightthickness=0)
canvas.create_line((75, 75), (795, 75), width=4)
canvas.create_line((75, 315), (795, 315), width=4)
canvas.create_line((75, 555), (795, 555), width=4)
canvas.create_line((75, 795), (795, 795), width=4)

canvas.create_line((75, 155), (795, 155), width=1)
canvas.create_line((75, 235), (795, 235), width=1)
canvas.create_line((75, 395), (795, 395), width=1)
canvas.create_line((75, 475), (795, 475), width=1)
canvas.create_line((75, 635), (795, 635), width=1)
canvas.create_line((75, 715), (795, 715), width=1)



canvas.create_line((75, 75), (75, 795), width=4)
canvas.create_line((315, 75), (315, 795), width=4)
canvas.create_line((555, 75), (555, 795), width=4)
canvas.create_line((795, 75), (795, 795), width=4)

canvas.create_line((153, 75), (153, 795), width=1)
canvas.create_line((233, 75), (233, 795), width=1)
canvas.create_line((393, 75), (393, 795), width=1)
canvas.create_line((473, 75), (473, 795), width=1)
canvas.create_line((633, 75), (633, 795), width=1)
canvas.create_line((713, 75), (713, 795), width=1)

canvas.pack()


def onClick(i):
	Default = 'SystemButtonFace'
	buttons[current_button.current_button_col][current_button.current_button_row]['bg'] = Default
	current_button.update(int(i[0])-1, int(i[1])-1)
	buttons[current_button.current_button_col][current_button.current_button_row]['bg'] = '#bcedef'
	
for i in range(1, 10):
	myFont = font.Font(size=9, weight="bold")
	buttons_column = []
	for j in range(1, 10):
		str_pos = str(i) + str(j)
		b = Button(root, height=4, width=8, text = "", command = lambda str_pos=str_pos: onClick(str_pos))
		b['font'] = myFont
		b.place(x=i*80, y=j*80)
		buttons_column.append(b)
	buttons.append(buttons_column)




import pickle

#OPEN MODEL
with open('model_hmm2.pkl', 'rb') as f:
	hmmModels = pickle.load(f)


#https://github.com/msnmkh/Spoken-Digit-Recognition/blob/master/SDR.py

#RECORDING OF THE AUDIO
def record_audio():
	fs = 16000	# Sample rate
	seconds = 3	 # Duration of recording

	my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
	sd.wait()  # Wait until recording is finished
	write('output.wav', fs, my_recording)  # Save as WAV file 
	
	wave, sample_rate =	 librosa.load('output.wav')
	mfcc_features = mfcc(wave, sample_rate).T
	
	#mfcc_features = mfcc(my_recording, fs)
	scoreList = {}
	for model_label in hmmModels.keys():
		model = hmmModels[model_label]
		score = model.score(mfcc_features)
		scoreList[model_label] = score
	predict = max(scoreList, key=scoreList.get)
	buttons[current_button.current_button_col][current_button.current_button_row]['text'] = predict
	sudoku.update_value(current_button.current_button_col, current_button.current_button_row, predict)

myFont = font.Font(size=18, weight="bold")
button_rec = Button(root, text='Record audio', font = myFont, command=record_audio)
#button_rec['font'] = myFont
button_rec.place(x=900, y=200)

def solve_sudoku():	
	#column, row
	sudoku.printSudoku()
	sudoku.solve_sudoku_no_recursion()
	sudoku.printSudoku()
	
	for i in range(9):
		for j in range(9):
			buttons[i][j]['text'] = sudoku.return_value(j, i)
			
myFont = font.Font(size=18, weight="bold")	
button_solve = Button(root, text='Solve sudoku', font=myFont, command=solve_sudoku)
button_solve.place(x=900, y=540)

value = StringVar()
 
def submit():
	number = value.get()
	buttons[current_button.current_button_col][current_button.current_button_row]['text'] = number
	sudoku.update_value(current_button.current_button_col, current_button.current_button_row, number)

myFont = font.Font(size=18, weight="bold")
value_entry = Entry(root,textvariable = value, font = myFont).place(x=880, y=260)
sub_btn=Button(root,text = 'Manual override', font = myFont, command = submit).place(x=900, y=300)

def reset_one():
	buttons[current_button.current_button_col][current_button.current_button_row]['text'] = ''
	sudoku.update_value(current_button.current_button_col, current_button.current_button_row, 0)
	

def reset_all():
	for i in range(9):
		for j in range(9):
			buttons[i][j]['text'] = ''
			sudoku.update_value(i, j, 0)

myFont = font.Font(size=18, weight="bold")	
button_reset_1 = Button(root, text='Reset current button', font=myFont, command=reset_one)
button_reset_1.place(x=900, y=420)
	
button_reset_all = Button(root, text='Reset sudoku', font=myFont, command=reset_all)
button_reset_all.place(x=900, y=480)




Information_Text = """How to use the sudoku solver:

First select a square in the sudoku --> the currently selected square will turn blue
Then either select record audio to insert a number between 1 and 9 or manually insert a number

Click on reset current button, to empty the current square
Click on reset all to empty the entire sudoku

Click on solve sudoku to get a solution
Please note:
  -  If there are multiple solutions, the solver will return only 1 solution
  -  If there are errors in the given input, the solver will not be able to find a good solution"""

def clickAbout():
    toplevel = Toplevel()
    label1 = Label(toplevel, text=Information_Text, height=0, width=100)
    label1.pack()


button1 = Button(root, text="How to use the sudoku solver", font=myFont, command=clickAbout)
button1.place(x=900, y=100)




















root.mainloop()