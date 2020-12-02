import cv2
import copy
import os
import glob
import random
import numpy as np
import pytesseract as pytes
from tkinter import*
from PIL import Image
pytes.pytesseract.tesseract_cmd="Tesseract-OCR\\tesseract.exe"

#************************************************************************** GUI class *******************************************************************

class sudokucls(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.row, self.col = -1, -1
        self.r = list()
        self.c = list()
        self.num = list()
        self.hint_i = 0
        self.exe = 0
        self.__incls()

    def __incls(self):                              #Playing GUI window
        photo = PhotoImage(file="icons/icon.png")
        root.iconphoto(False, photo)
        self.root.title(" Sudoku ")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=490, height=490, bg="snow")

        self.f1 = Frame(self).pack(fill=BOTH, side=BOTTOM)
        self.B1 = Button(self.f1, text="Clear", font="Helvetica 10 bold", fg="red3", bg="snow", height=1, width=9,
                         command=self.clear_ans) \
            .pack(side=RIGHT, padx=10, pady=10)
        self.B2 = Button(self.f1, text="Hint", font="Helvetica 10 bold", fg="royalblue4", bg="snow", height=1, width=9,
                         command=self.hint) \
            .pack(side=RIGHT)
        self.B3 = Button(self.f1, text="Solution", font="Helvetica 10 bold", fg="darkgreen", bg="snow", height=1,
                         width=9, command=self.solution) \
            .pack(side=LEFT, padx=10)
        self.B4 = Button(self.f1, text="CHECK", font="Helvetica 10 bold", fg="royalblue4", bg="snow", height=1, width=9,
                         command=self.check) \
            .pack(side=LEFT, padx=10)

        self.draw_grid()                    #for drawing grids of 9x9
        self.canvas.pack(fill=BOTH, side=TOP)
        fill_flag = 0
        self.draw_fill(fill_flag)               #for filling in grids

        self.canvas.bind("<Button-1>", self.cell_clicked)               #if any left click then call cell_clicked()

        self.canvas.bind("<Key>", self.key_pressed)                     #if any number key pressed then call key_pressed()


    def draw_grid(self):                                        #drawing grids of 9x9
        for i in range(10):
            color = "navy" if i % 3 == 0 else "gray"

            x0 = 20 + i * 50
            y0 = 20
            x1 = 20 + i * 50
            y1 = 470
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = 20
            y0 = 20 + i * 50
            x1 = 470
            y1 = 20 + i * 50
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def draw_fill(self, fill_flag):                 #filling in grids
        global Usudoku, sudoku

        if (fill_flag == 1):
            k = 0
            for (i, j) in zip(self.r, self.c):
                if self.num[k] != 0:
                    x = 20 + j * 50 + 25
                    y = 20 + i * 50 + 25
                    self.canvas.create_text(x, y, text=self.num[k], font=("Purisa", 18, "bold"), fill="springGreen4")
                k += 1

        else:
            for i in range(9):
                for j in range(9):
                    if Usudoku[i][j] != 0:
                        x = 20 + j * 50 + 25
                        y = 20 + i * 50 + 25
                        self.canvas.create_text(x, y, text=Usudoku[i][j], font=("purisa", 18, "bold"), fill="black")

    def highlight_cell(self):                   #highlighting cell in focus
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = 20 + self.col * 50 + 1
            y0 = 20 + self.row * 50 + 1
            x1 = 20 + (self.col + 1) * 50 - 1
            y1 = 20 + (self.row + 1) * 50 - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (20 < x < 470 and 20 < y < 470):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - 20) // 50, (x - 20) // 50

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif Usudoku[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.highlight_cell()                  #calling for highlithing cell

    def key_pressed(self, event):

        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            x = 20 + self.col * 50 + 25
            y = 20 + self.row * 50 + 25
            self.canvas.create_text(x, y, text=(event.char), font=("Purisa", 14), tags="numbers", fill="deeppink")
            self.r.append(self.row)
            self.c.append(self.col)
            self.num.append(int(event.char))
            self.col, self.row = -1, -1

    def check(self):                    #checking inputs
        flag = 0
        for i in range(len(self.num)):
            if sudoku[self.r[i]][self.c[i]] == self.num[i]:
                Usudoku[self.r[i]][self.c[i]] = self.num[i]
                flag = 1
            else:
                self.num[i] = 0

        self.draw_fill(flag)
        self.r.clear()
        self.c.clear()
        self.num.clear()

        if (int(0) not in Usudoku and Usudoku == sudoku):
            self.victory()

    def clear_ans(self):                    #clearing inputs
        self.canvas.delete("numbers")

    def hint(self):                            #printing a row as hint
        self.exe += 1
        a = [3, 6, 8, 1, 2, 7, 5, 0, 4]
        i = a[self.hint_i]
        y = 20 + i * 50 + 25
        for j in range(9):
            x = 20 + j * 50 + 25
            if (Usudoku[i][j] & sudoku[i][j] == 0):
                Usudoku[i][j] = sudoku[i][j]
                self.canvas.create_text(x, y, text=sudoku[i][j], font=("Purisa", 18, "bold"), fill="deep sky blue")

        self.hint_i = (self.hint_i + 1) % 9

    def solution(self):                         #show whole solution
        self.exe = 4
        self.clear_ans()
        for i in range(9):
            for j in range(9):
                y = 20 + i * 50 + 25
                x = 20 + j * 50 + 25
                if (Usudoku[i][j] & sudoku[i][j] == 0):
                    Usudoku[i][j] = sudoku[i][j]
                    self.canvas.create_text(x, y, text=sudoku[i][j], font=("Purisa", 18, "bold"), fill="deep sky blue")

    def victory(self):                          #last message
        x0 = y0 = 120
        x1 = y1 = 370
        self.canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        # create text
        x = y = 20 + 4 * 50 + 25
        if self.exe == 0:
            ch = "You win!"
        elif self.exe in [2, 3]:
            ch = "Satisfactory!"
        else:
            ch = "Try Again!"
        self.canvas.create_text(x, y, text=ch, tags="victory", fill="white", font=("Arial", 32))


#**************************************************************** sudoku solver functions module *********************************************************

def print_grid(sudo):
    for i in sudo:
        print (i)

#---------------------------------------------------------------- finding voids ---------------------------------------------------------------------------

def find_blank(row, col):
    flag=0
    for i in range(9):
        for j in range(9):
            if(sudoku[i][j]==0):
                row = i
                col = j
                flag= 1
                a=[row,col,flag]
                return a
    a=[-1,-1,flag]
    return a

#----------------------------------------------------------------- checking for possibility ---------------------------------------------------------------

def is_allow(num, row, col):
    for i in range(9):                               #checking row wise
        if(sudoku[row][i] == num):
            return False

    for i in range(9):                               #checking col wise
        if(sudoku[i][col] == num):
            return False

    start_row = (row//3)*3
    start_col = (col//3)*3
    for i in range(start_row, start_row + 3):        #checking box wise
        for j in range(start_col, start_col + 3):
            if sudoku[i][j] == num:
                return False

    return True

#----------------------------------------------------------------- main solving module --------------------------------------------------------------------

def solving_module():

  row=0
  col=0
  rec=find_blank(row, col)                          #calling for checking voids
  if (rec[2]==0):
      return True
  row=rec[0]
  col=rec[1]

  for num in range(1,10):
      if (is_allow(num, row, col)):                #calling for possibility func.
         sudoku[row][col]=num

         if (solving_module()):                    #recursive calling
            return True
         sudoku[row][col]=0

  return False                                     #recursion trigger

#**************************************************** Grid and digit detection module function ************************************************************

#cleaning folders

def clean_fol(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#Black edge croping

def autocrop(image):
    for i in range(28):
        for j in range(28):
            if (i<=3 or j<=3 or i>=26 or j>=26) and image[i][j]==255:
                image[i][j]=0
    return image
#--------------------------------------------------------------------------------------------------------------------------------------------------------

#using ocr to detect and place digit in solving grid
def ocr_detector(x,num):
    pos=1
    k=0
    for i in range(9):
        for j in range(9):
            if pos == x:                        #getting correct position in solving grid
                if is_allow(num,i,j):                #only checking for acurracy
                    Usudoku[i][j]=num

            pos+=1

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# function to check the order of points

def proper_order(ar):
    ar1 = [[0, 0], [0, 0], [0, 0], [0, 0]]
    max = 0
    ymax = 0
    min = 99999
    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) > max:
            max = ar[i][0][0] + ar[i][0][1]
            ar1[2][0] = ar[i][0][0]
            ar1[2][1] = ar[i][0][1]
        if (ar[i][0][0] + ar[i][0][1]) < min:
            min = ar[i][0][0] + ar[i][0][1]
            ar1[0][0] = ar[i][0][0]
            ar1[0][1] = ar[i][0][1]

    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) < max and (ar[i][0][0] + ar[i][0][1]) > min and ar[i][0][1] > ymax:
            ar1[1][0] = ar[i][0][0]
            ar1[1][1] = ar[i][0][1]
            ymax = ar[i][0][1]
    for i in range(len(ar)):
        if (ar[i][0][0] + ar[i][0][1]) < max and (ar[i][0][0] + ar[i][0][1]) > min and ar[i][0][1] < ymax:
            ar1[3][0] = ar[i][0][0]
            ar1[3][1] = ar[i][0][1]

    return ar

#------------------------------------------------------ function smothing module --------------------------------------------------------------------------
#converting BGR -> grayscale -> blurs to remove noise

def blurring_mod(img):
   imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
   imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)
   imgCanny=cv2.Canny(imgBlur,10,50)
   cv2.imshow("canny",imgCanny)
   return imgCanny

#-------------------------------------------------------------- chopping 0f cells -------------------------------------------------------------------------

def chopping_grid(pt):

    img = cv2.imread("frame.jpg", 1)  # reading captured grid
    flag = 1
    dim = np.float32([[0, 0], [0, 252], [252, 252], [252, 0]])  # converting it into 28x3x3 grid
    pt = np.float32(pt)

    grid = cv2.getPerspectiveTransform(pt, dim)
    warp_img = cv2.warpPerspective(img, grid, dsize=(252, 252))

    cv2.imwrite('warp_frame.jpg', warp_img )
    cv2.imshow('warp-frame', warp_img)

    for i in range(9):  # loop for chopping cells
        for j in range(9):
            cell = warp_img[(i * 28):((i + 1) * 28), (j * 28):((j + 1) * 28)]
            cell = cv2.GaussianBlur(cell, (5, 5), 1)

            cv2.imwrite('cells/cell{}.png'.format(flag), cell)
            flag = flag + 1

#-------------------------------------------------- separating spaces and numbers -------------------------------------------------------------------------

def separate_space():

    noNum = 0
    list_cell = [list()]        # list to store (pos,element)
    num_pos = list()           # list to store number's position

    for k in range(1, 82):
        sum = 0

        cell = cv2.imread("cells/cell{}.png".format(k), 0)

        cell = cv2.adaptiveThreshold(cell, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)
        list_cell.append([k, cell])

        # separating module

        for i in range(10, 19):
            for j in range(10, 19):
                sum = sum + cell[i, j]

        j = 81 - (sum / 255)

        if j >= 10:        # separating condition
            noNum += 1
            num_pos.append(k)

    return (noNum,list_cell,num_pos)

#----------------------------------------------- removing cell's noices and saving ------------------------------------------------------------------------

def remove_cell_noice(num_pos):

    for i in num_pos:
        cell = cv2.imread("cells/cell{}.png".format(i), 0)
        # for sharpning of image

        cell = cv2.adaptiveThreshold(cell, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)
        f2, cell = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        cell = autocrop(cell)          # removing borders of cells

        # removing noices
        kernel = np.ones((2, 2), np.uint8)
        cell = cv2.dilate(cell, kernel, iterations=1)
        cell = cv2.erode(cell, kernel)

        max_con = [0]
        max_area = 0
        cell_copy = cell.copy()
        contours, hie = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for j in range(len(contours)):
            if cv2.contourArea(contours[j]) > max_area:
                max_area = cv2.contourArea(contours[j])
                max_con = contours[j]

        cv2.drawContours(cell, [max_con], -1, (255, 255, 255), -1)
        f3, thresh = cv2.threshold(cell, 254, 255, cv2.THRESH_BINARY)

        cell = cv2.bitwise_and(cell_copy, cell_copy, mask=thresh)
        f4, cell = cv2.threshold(cell, 254, 255, cv2.THRESH_BINARY_INV)

        cell = cv2.dilate(cell, kernel)
        cell = cv2.erode(cell, kernel)

        cv2.imwrite("binary/cell_binary{}.png".format(i), cell)         # saving of filtered cells

        if i == len(num_pos):
            break

# ----------------------------------------------------------using pytesseract OCR to recognise the num-----------------------------------------------------
        img_ocr = Image.open("binary/cell_binary{}.png".format(i))
        string = pytes.image_to_string(img_ocr, lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        if string[0] >= '1' and string[0] <= '9':
            ocr_detector(i, int(string[0]))

#-------------------------------------------------------- virtual solution display -----------------------------------------------------------------------

def vir_sol(num_pos):

    dst = cv2.imread("warp_frame.jpg",1)

    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX    #font of text
    for i in range(9):
        for j in range(9):
            if (sudoku[i][j]!=0) and ((i*9)+j+1) not in num_pos:
                x = (j * 28 + 8)
                y = (i * 28 + 22)
                dig = str(sudoku[i][j])           #reading digits as string

                cv2.putText(dst,dig,(x,y),font,0.65,(200,100,50),1,2)           #putting text on image

            vir_img = cv2.resize(dst, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)         #resizing image
            cv2.imshow('SUDOKU!!!', vir_img)          #display window
            cv2.waitKey(40)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



#-------------------------------------------------------- Getting grid from webcam -----------------------------------------------------------------------

def cam():
    # use of webcam to capture image of sudoku
    global pt
    count = 0
    flag = 1

    cap = cv2.VideoCapture(0)  # web cam ON
    while (cap.isOpened()):

        f1, img = cap.read()  # reading frames from web cam

        imgCanny = blurring_mod(img)  # calling smothing func
        # finding sudoku grid

        contours, hie = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        max_con = [0]  # maxc for maximum contours
        max_area = 0  # max is variable for maximum area

        for i in range(len(contours)):  # loop to find largest contour in given frame

            peri = cv2.arcLength(contours[i], True)  # finding perimeter of contour
            approx = cv2.approxPolyDP(contours[i], 0.011 * peri, True)  # contour approximation
            (x, y, w, h) = cv2.boundingRect(approx)
            # checking maximum contours

            if cv2.contourArea(contours[i]) > 10000 and cv2.contourArea(contours[i]) > max_area \
                    and len(approx) == 4 and float(w) / h == 1:
                max_area = cv2.contourArea(contours[i])
                max_con = approx

        # check for four corners then drawing contours
        if len(max_con) == 4:
            count = count + 1
        else:
            count = 0
        if len(max_con) == 4:
            cv2.drawContours(img, [max_con], -1, (100, 200, 0), 2)
            cv2.drawContours(img, max_con, -1, (0, 0, 255), 4)

        flag = 0
        cv2.imshow('Contours', img)  # displaying contours
        cv2.waitKey(1)
        if count == 4:
            cv2.imwrite("frame.jpg", img)  # saving that frame
            pt = max_con
            flag = 1

        if flag == 1:
            break

    cv2.destroyAllWindows()
    cap.release()

    im = cv2.imread("icons/wait.png")
    cv2.imshow("Loading Image", im)
    cv2.waitKey(1)

    pt = proper_order(pt)  # function to set proper order of points

    chopping_grid(pt)  # function for chopping grid in 9x9

#---------------------------------------------------------- generating function ----------------------------------------------------------------

def gen():
    im=cv2.imread("icons/wait.png")
    cv2.imshow("Loading Image",im)
    cv2.waitKey(1)
    img = cv2.imread("data_base/{}.png".format(random.randint(1,40)))
    img = cv2.resize(img, (252, 252))
    cv2.imwrite("warp_frame.jpg", img)
    flag = 1
    for i in range(9):  # loop for chopping cells
        for j in range(9):
            cell = img[(i * 28):((i + 1) * 28), (j * 28):((j + 1) * 28)]
            cell = cv2.GaussianBlur(cell, (5, 5), 1)

            cv2.imwrite('cells/cell{}.png'.format(flag), cell)
            flag = flag + 1


def rts():
    global rts_var
    rts_var=1

def quit():
    root.destroy()

#----------------------------------------------------------- A beginning of new tour of learning ---------------------------------------------


pt=None
rts_var=0
Usudoku = [[0 for x in range(9)] for y in range(9)]
sudoku = [[0 for x in range(9)] for y in range(9)]

root=Tk()
root.geometry("%dx%d" % (490,490+60))
photo = PhotoImage(file="icons/icon.png")
root.iconphoto(False, photo)
root.title(" Sudoku ")
frame=Frame().pack()
Label(frame,text=" WELCOME TO SUDOKU !!!",font=("Comicsansms",20,"bold"),fg="royalblue3").pack(side=TOP, fill="x",pady=20)
Label(frame,text='" Stay Home Stay Safe" \n\n" Every Smile Matters "',font=("Comicsansms",12,"bold"),fg="darkgreen").pack(side=TOP, fill="x",pady=20)
photo=PhotoImage(file="icons/cam.png")
photo=photo.subsample(3,3)
Button(frame,text="Camera",font=("script", 20,"bold"), image=photo, compound=TOP,bg="snow",command=lambda:[cam(),quit()]).pack(side=LEFT, padx=50)
photo2=PhotoImage(file="icons/generate.png")
photo2=photo2.subsample(3,3)
Button(frame,text="Generate",font=("script", 20,"bold"), image=photo2, compound=TOP,bg="snow",command=lambda:[gen(),quit()]).pack(side=LEFT,padx=50)
root.mainloop()

noNum, list_cell, num_pos = separate_space()      # function for separating numbers

remove_cell_noice(num_pos)     # function to clean cell noice and save cell

sudoku=copy.deepcopy(Usudoku)

solving_module()          #calling solving module

cv2.destroyAllWindows()

root = Tk()
root.geometry("500x500")
photo = PhotoImage(file="icons/icon.png")
root.iconphoto(False, photo)
root.title(" Sudoku ")
Label(root,text=" Select one ",font=("Arial", 32,"bold"),fg="red4").pack(fill=BOTH, pady=25)
frame=Frame().pack(side=BOTTOM)
Button(frame,text=" Play!!! ",font=("Arial", 20,"bold"),relief=RAISED,bg="light green",height=5,width=10,command=lambda:[quit()]).pack(side=LEFT,padx=15)
Button(frame,text=" Real Time\n sol. ",font=("Arial", 20,"bold"),relief=RAISED,bg="light pink",height=5,width=10,command=lambda:[rts(),quit()]).pack(side=RIGHT,padx=15)
root.mainloop()

if(rts_var==1):
   vir_sol(num_pos)            #function for virtual display

elif(rts_var==0):
    root = Tk()
    root.geometry("%dx%d" % (490, 490 + 60))
    sudokucls(root)                #class of final GUI
    root.mainloop()


clean_fol("binary/*.png")           #removing data from file
clean_fol("cells/*.png")            #removing data from file

