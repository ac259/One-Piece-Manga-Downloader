import urllib.request
import os
import shutil
import img2pdf
import progressbar
from time import sleep
from urllib.request import Request, urlopen
from selenium import webdriver


browser = webdriver.Chrome('chromedriver')


def retrieve_number_of_pages():
	pages = browser.find_element_by_id('selectpage')
	#print(number_of_pages.text) 
	# print(number_of_pages)
	# print(type(number_of_pages))

	pages_array = [pages.text]
	#print(pages_array)
	pages_array = [i.split('\n') for i in pages_array] 
	page_array_flattened = [val for sublist in pages_array for val in sublist]
	# Deleting the last element which is the 17 `of 17 page`
	page_array_flattened = page_array_flattened[:-1]
	#print(page_array_flattened)
	number_of_pages = page_array_flattened[-1]
	return number_of_pages

def download_latest_chapter():
	
	browser.get("https://ww21.watchop.io/manga2/")
	elem = browser.find_element_by_id("latestchapters")
	#print(elem.text)

	latest_manga_link = elem.find_element_by_css_selector('a').get_attribute('href')
	#print(latest_manga_link)

	browser.get(latest_manga_link)

	imgdiv = browser.find_element_by_id('imgholder')

	imglink = imgdiv.find_element_by_css_selector('a').get_attribute('href')
	print(imglink)
	manga_number = imglink.split('/')
	manga_number = manga_number[-2]
	print("The manga number is :", manga_number)

	# Returning the total number of pages in the manga
	max_pages = retrieve_number_of_pages()
	print(max_pages)
	img2pdf_list = []

	bar = progressbar.ProgressBar(maxval=int(max_pages)+1, \
	    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()

	for i in range(1,int(max_pages)+1):
		img = browser.find_element_by_id('img')
		#print(img.text)
		imgdiv = browser.find_element_by_id('imgholder')
		img2 = imgdiv.find_element_by_css_selector('img').get_attribute('src')
		#print(img2)

		page = img2.split('/')[-1]
		#print(page)
		# urllib.request.urlretrieve(img2, page)

		req = Request(img2, headers={'User-Agent': 'Mozilla/5.0'})
		
		# Download the file from `url` and save it locally under `file_name`:
		with urllib.request.urlopen(req) as response, open(page, 'wb') as out_file:
		    #print(out_file)
		    #print('page is: ',page)
		    shutil.copyfileobj(response, out_file)
	    
		#print(page)
		
		os.rename(page,str(i)+'.jpg')
		filename = str(i) +'.jpg'
		img2pdf_list.append(filename)
		bar.update(i+1)
		sleep(0.1)
		imgdiv.find_element_by_id('img').click()

	bar.finish()
	return img2pdf_list,manga_number


def convert_to_pdf(img_list,manga_number):
	'''
	Convert them to a pdf

	img2pdf : Lossless conversion of raster images to PDF
	installation : `pip install img2pdf`

	`# multiple inputs (variant 2)
	with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(["test1.jpg", "test2.png"]))`

	'''

	with open(manga_number + ".pdf","wb") as f:
		f.write(img2pdf.convert(img_list))

	sleep(0.1)
	# Delete Images once pdf is created!
	for image in img_list:
		os.remove(image)

if __name__ == "__main__":

	img_list,manga_number = download_latest_chapter()
	convert_to_pdf(img_list,manga_number)
	print("Your Download is Complete! Enjoy")