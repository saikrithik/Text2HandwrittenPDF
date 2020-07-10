from PIL import Image
from fpdf import FPDF
from PIL import Image
import os
import re, os.path
import cv2

import time
import sys
animation = "|/-\\"


#checking if there are existing files in imageout directory
#Deleting them if they exist
mypath = "imageout"
for root, dirs, files in os.walk(mypath):
    for file in files:
        os.remove(os.path.join(root, file))

#Reading Background image 
BG = Image.open("background/bg.png")
sizeOfSheet = BG.width
gap, _ = 0, 0 #dont change this
#mentioning allowed chars
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890'


#function for pasting the letters on the backround
def write(char):
    global gap, _
    if char == '\n':
        pass
    else:
        char.lower()
        cases = Image.open("letterimages/%s.png" % char)
        BG.paste(cases, (gap, _))
        size = cases.width
        gap += size
        del cases

#function for mapping letter with the letterimages data
def letterwrite(word):
    global gap, _
    if gap > sizeOfSheet - 95 * (len(word)):
        gap = 0
        _ += 200
    for letter in word:
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter = 'u'+letter
            elif letter == '.':
                letter = "fullstop"
            elif letter == '!':
                letter = 'exclamation'
            elif letter == '?':
                letter = 'question'
            elif letter == ',':
                letter = 'comma'
            elif letter == '(':
                letter = 'braketop'
            elif letter == ')':
                letter = 'braketcl'
            elif letter == '-':
                letter = 'hiphen'
            write(letter)

#function for mapping words
def word(Input):
    wordlist = Input.split(' ')
    for i in wordlist:
        letterwrite(i)
        write('space')


if __name__ == '__main__':
    
    try:
        with open('input.txt', 'r') as file:
            data = file.read().replace('\n', ' ')

        with open('output.pdf', 'w') as file:
            pass
        # getting necessary Data in to a list
        split_data = []
        for match in re.finditer(r'[^.,?!\s]+|[.,?!]', data):
            split_data.append(match.group())
        #input no. of words per page(depends on the user letterimages)
        words = input("Enter No. of words per Page[150-250]:")
        print("------------------- Getting Text Ready -------------------")
        #intializing Content variables
        numwords = len(split_data) // int(words)
        allwords = len(split_data)
        page_size = len(split_data) // (numwords + 1)
        temp=[]
        #clipping data in to pages
        for i in range(0, allwords, page_size):
            clip_data =  [' '.join(i) for i in [split_data[i:i + page_size]]]
            temp.append(clip_data[0])
        print("--Generating Images--")
        #Making border and saving file
        for i in range(0, len(temp)):
            time.sleep(0.01)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
            
            word(temp[i])
            write('\n')
            
            imageName = 'imageout/'+str(i)+'out.png'
            BG.save(imageName)

            borderType = cv2.BORDER_CONSTANT
            
            
            src = cv2.imread(cv2.samples.findFile(imageName), cv2.IMREAD_COLOR)
            top = int(0.05 * src.shape[1] )  # shape[0] = rows
            bottom = top
            left = int(0.05 * src.shape[1])  # shape[1] = cols
            right = left
            value = [255,  255, 255]
            
            BG = cv2.copyMakeBorder(src, top,
                                     bottom, left,
                                     right, borderType, None, value)
            BG = cv2.resize(BG, (2632,3176))
            
            cv2.imwrite(imageName, BG)
            BG1 = Image.open("background/bg.png")
            BG = BG1
            gap = 0
            _ = 0
        print("-->END")
    except ValueError as E:
        print("{}\nTry again".format(E))


from fpdf import FPDF
from PIL import Image

print("------------------- Converting to PDF -------------------")
#Generating PDF
imagelist = []
for i in range(0, len(temp)):
    imageName = 'imageout/'+str(i)+'out.png'
    imagelist.append(imageName)

cover = Image.open(imagelist[0])
width, height = cover.size
pdf = FPDF(unit="pt", format=[width, height])

for i in range(0, len(imagelist)):
    pdf.add_page()
    pdf.image(imagelist[i], 0, 0)
pdf.output("output.pdf", "F")
