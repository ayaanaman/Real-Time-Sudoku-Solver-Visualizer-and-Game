# Real-Time-Sudoku-Solver-Visualizer-and-Game
Developed a software that scans physical sudoku puzzles and is able to solve it in real time bases or you can play on an interactive and user friendly grid all designed on Tkinter. 

Topic : Real Timer Sudoku Solver and Game

Problem : To make a real time Sudoku solver and an interactive playing
platform.

Special Features :
❏ Input by webcam
❏ Real time solution
❏ Interactive grid to play
❏ All in GUI

Approach :
● Input using Webcam or Generate method:
Reading Image -> Processing -> Extracting digits(using OCR) ->Forming grid

● Sudoku solving module:
Using Backtracking algo for solving.

● Real time solution:
Using Opencv for masking solution on real time image.

● Playing Grid:
GUI using tkinter along with HINT, CHECK, CLEAR, SOLUTION
buttons.

![image](https://user-images.githubusercontent.com/58986643/175779768-8f8d531a-3360-4680-92ff-025e1d4040af.png)

CODE SNIPPETS
Programming Language: Python 3.7

Python Modules:
1. OpenCV -> for image reading, writing, processing on image.
2. Numpy -> for performing operations on images to reduce
noises.
3. Tkinter -> for GUI
4. Pytesseract -> for OCR
5. copy,os,glob,PIL,random -> for deep copy, file handling,
removing folder data, reading image, randint()
respectively.

User Defined Classes and Functions:
● class sudokucls(Frame) #GUI CLASS
○ def __incls(self): #Playing GUI window
○ def draw_grid(self): #drawing grids of 9x9
○ def draw_fill(self, fill_flag): #filling in grids
○ def highlight_cell(self): #highlighting cell in focus
○ def cell_clicked(self, event): #detect click on canvas
○ def key_pressed(self, event): #detect pressed key
○ def check(self): #checking inputs (Button on GUI)
○ def clear_ans(self): #clearing inputs (Button on GUI)
○ def hint(self): #printing a row as hint (Button on GUI)
○ def solution(self): #show whole solution (Button on GUI)
○ def victory(self): #last message display

● def solving_module(): #main solving module
    def find_blank(row, col) finding voids
    def is_allow(num, row, col): checking for possibility
● def cam(): Getting grid from webcam
    def blurring_mod(img): image smoothing module
    def proper_order(ar): check the order of points
    def chopping_grid(pt): chopping 0f cells
● def gen(): function for generating Sudoku
● def separate_space(): separating blanks and numbers
● def remove_cell_noice(num_pos): removing cell's noises and saving
    def autocrop(image): Black edge cropping
    def ocr_detector(x,num): detect and place digit in grid
● def windowprint_grid(sudo): solution printing function in output
● def function vir_sol(num_pos): real time solution display
● def flagrts(): function for assigning
● def quit(): closing GUI windows
● def re-useclose_fol(Path): removing data from folder for
● GUI Window code

Folders Used:
● Binary (for storing Binary image of cells with digits)
● cells (for storing all image 81 cells)
● data_base (contain images of sudoku used in gen())
● icons (contain different icons to used in GUI)

Additional software Used:
● tesseract

![image](https://user-images.githubusercontent.com/58986643/175779897-85920be1-93b2-4134-add9-74f0d0c2801f.png)
![image](https://user-images.githubusercontent.com/58986643/175779948-5c4f87d7-7f75-4a22-802d-3b876f806297.png)
![image](https://user-images.githubusercontent.com/58986643/175779960-3590efb7-379f-4130-8d0e-f6d9aaca4930.png)


