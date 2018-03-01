#!/usr/bin/python
try:
    import Image

except ImportError:
	from PIL import Image

import pyscreenshot as ImageGrab

import pytesseract

import webbrowser

from pymouse import PyMouse
from pykeyboard import PyKeyboard

import nltk
import wikipedia

import time

#Gets rid of all the funky symbols that get generated when encoding
def unicodetoascii(text):

    TEXT = (text.
    		replace('\\xe2\\x80\\x99', "'").
            replace('\\xc3\\xa9', 'e').
            replace('\\xe2\\x80\\x90', '-').
            replace('\\xe2\\x80\\x91', '-').
            replace('\\xe2\\x80\\x92', '-').
            replace('\\xe2\\x80\\x93', '-').
            replace('\\xe2\\x80\\x94', '-').
            replace('\\xe2\\x80\\x94', '-').
            replace('\\xe2\\x80\\x98', "'").
            replace('\\xe2\\x80\\x9b', "'").
            replace('\\xe2\\x80\\x9c', '"').
            replace('\\xe2\\x80\\x9c', '"').
            replace('\\xe2\\x80\\x9d', '"').
            replace('\\xe2\\x80\\x9e', '"').
            replace('\\xe2\\x80\\x9f', '"').
            replace('\\xe2\\x80\\xa6', '...').
            replace('\\xe2\\x80\\xb2', "'").
            replace('\\xe2\\x80\\xb3', "'").
            replace('\\xe2\\x80\\xb4', "'").
            replace('\\xe2\\x80\\xb5', "'").
            replace('\\xe2\\x80\\xb6', "'").
            replace('\\xe2\\x80\\xb7', "'").
            replace('\\xe2\\x81\\xba', "+").
            replace('\\xe2\\x81\\xbb', "-").
            replace('\\xe2\\x81\\xbc', "=").
            replace('\\xe2\\x81\\xbd', "(").
            replace('\\xe2\\x81\\xbe', ")")

                 )
    return TEXT

#Handles formatting strings with a combination of f_
def formatStringsWithF(formattedText):
	if 'x80' in formattedText:
		formattedText = formattedText[:formattedText.index('x80') - 9] + "ff" + formattedText[formattedText.index('x80') + 3:]
	
	if 'x81' in formattedText:
		formattedText = formattedText[:formattedText.index('x81') - 9] + "fi" + formattedText[formattedText.index('x81') + 3:]
	
	if 'x82' in formattedText:
		formattedText = formattedText[:formattedText.index('x82') - 9] + "fl" + formattedText[formattedText.index('x82') + 3:]
	
	if 'x83' in formattedText:
		formattedText = formattedText[:formattedText.index('x83') - 9] + "ffi" + formattedText[formattedText.index('x83') + 3:]

	return formattedText

#Searches question in web browser
def searchQuestion(text, questionHeight):
	m = PyMouse()
	k = PyKeyboard() 
	m.move(2500,100)
	m.click(2500,100)
	m.click(2500,100)
	m.click(2500,100)
	k.type_string(text)
	k.tap_key(k.return_key)
	k.tap_key(k.return_key)
		
	#Delay is needed otherwise question doesn't get searched
	time.sleep(.5)
		
	m.move(2866, 100)
	m.click(2866, 100)
	
	time.sleep(.4)
		
	m.move(2834, 188)
	m.click(2834, 188)
			
	k.press_key(k.control_key)
	k.tap_key('a')
	k.release_key(k.control_key)
			
	k.type_string(retrieveOptions(questionHeight))
	
	#Delay is needed otherwise question doesn't get searched
	time.sleep(.3)
	
	m.move(2361, 1058)
	m.click(2361, 1058)

def removeBeginningNumber(text):
	return text[3:]

#Gets rid of all kinks in text to make it work in functions
#Formats the question
def formatText(text):
	formattedText = text.replace('\n', ' ').encode('utf-8').encode('string_escape')
	
	#Removes the beginning number from the question
	formattedText = removeBeginningNumber(formattedText)	
	
	#the letter F has a lot of weird cases that need to be handled
	formattedText = formatStringsWithF(unicodetoascii(formattedText))
	
	#Gets rid of backslash (\) from the string
	formattedText = formattedText.replace("\\", "")
	
	return formattedText

def optionFormat(text):
	formattedText = text.encode('utf-8').encode('string_escape')
	
	formattedText = unicodetoascii(formattedText)
	
	#Removes quotations from the text because otherwise it wouldn't be recognized by the search
	formattedText = formattedText.replace('"', '')
	
	return formattedText
	

#Waits for question to disappear off screen to resume waiting for next one
def waitEndQuestion(endQuestion):
	while (endQuestion.getcolors()[0][1][0] == 255 and endQuestion.getcolors()[0][1][1] == 255 and endQuestion.getcolors()[0][1][2] == 255):
		# White box detection
		endQuestion = ImageGrab.grab(bbox = (750, 400, 755, 405))
		
		print("waiting for question to end") 

def getFullQuestionHeight():
	#Checks the far left portion of the question so the text doesn't get in the way
	width = 1115
	
	#Ideally the min height of the question
	height = 380
	
	question = ImageGrab.grab(bbox = (width, height, width + 5, height + 5)).getcolors()
	
	#While the recieved box is not grey (246, 246, 246) since all 246, in theory only have to check for one
	while (question[0][1][0] != 246):
		height += 15
		question = ImageGrab.grab(bbox = (width, height, width + 5, height + 5)).getcolors()
		
		#Debugging purposes
		ImageGrab.grab(bbox = (753, 322, 1230, height)).save("q" + str(height) + ".jpg")
		#print(question)
		
	return height

def retrieveOptions(questionHeight):
	#Grabs Question
	
	startPos = questionHeight
	optionHeight = 52
	optionGap = 15
	fullOption = optionHeight + optionGap
	
	option1 = ImageGrab.grab(bbox = (795, startPos, 1181, startPos + optionHeight))
	option2 = ImageGrab.grab(bbox = (795, startPos + fullOption, 1181, startPos + fullOption + optionHeight))
	option3 = ImageGrab.grab(bbox = (795, startPos + (fullOption*2), 1181, startPos + (fullOption*2) + optionHeight))
	
	#Testing purposes
	#option1.save("option1.png")
	#option2.save("option2.png")
	#option3.save("option3.png")
	
	
	text1 = optionFormat(pytesseract.image_to_string(option1))
	text2 = optionFormat(pytesseract.image_to_string(option2))
	text3 = optionFormat(pytesseract.image_to_string(option3))
	
	#Testing purposes
	#print(text1)
	#print(text2)
	#print(text3)
	
	formOptionString = text1 + " " + text2 + " " + text3
	
	formOptionString = formOptionString.replace("\n", '')
	
	return formOptionString
	
#Runs loop while waiting for question to appear
def startBot():
	#Concrete coordinates of the question
	#questionEndY is determined using the function getFullQuestionHeight
	questionStartX = 753
	questionEndX = 1230
	questionStartY = 322
	
	#Coordinates used to check if the space is white
	#White space indicates that a question is present
	whiteSpaceStartX = 750
	whiteSpaceEndX = 755
	whiteSpaceStartY = 400
	whiteSpaceEndY = 405
	
	while True:
		whiteBox = ImageGrab.grab(bbox = (whiteSpaceStartX, whiteSpaceStartY, whiteSpaceEndX, whiteSpaceEndY))
		
		print("waiting for question")
		
		if (whiteBox.getcolors()[0][1][0] == 255 and whiteBox.getcolors()[0][1][1] == 255 and whiteBox.getcolors()[0][1][2] == 255):
			print("question loaded")
			
			questionEndY = getFullQuestionHeight()
			
			#Grabs Question
			im = ImageGrab.grab(bbox = (questionStartX, questionStartY, questionEndX, questionEndY))
						
			text = formatText(pytesseract.image_to_string(im))
			
			searchLoop = True
			while searchLoop:
				#Searches question in browser
				searchQuestion(text, questionEndY)
				
				response = raw_input("Search again?")
				
				#If something is entered, then searches again, otherwise, ends loop
				if response == "":
					searchLoop = False

			waitEndQuestion(ImageGrab.grab(bbox = (whiteSpaceStartX, whiteSpaceStartY, whiteSpaceEndX, whiteSpaceEndY)))

if __name__ == "__main__":
	startBot()
