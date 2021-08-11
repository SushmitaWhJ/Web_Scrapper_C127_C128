#Step 1- Upload the new created folder in VS and run pip install virtualenv 
#Step 2 - Run virtualenv env (Gives name to the virtual environment).It creates a file named env
#Step 3 - Run source env/bin/activate(Mac)   
#         venv\Scripts\activate.bat  (Windows)


from selenium import webdriver
from bs4 import BeautifulSoup   #BeautifulSoup reads page as html page 
import time
import csv
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

#Before installing chrome extensions, we need to check chrome extension in chrome/settings
#Download the extension in the same folder you are working on and give the path

browser = webdriver.Chrome("/Users/sushmitasingh/Desktop/Web_Scrapping/chromedriver")
browser.get(START_URL)
time.sleep(10)

#header infromation which I need from page
def scrape():
    headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]
       # empty list to save data
    planet_data = []
    for i in range(0, 428):
            #we are passing the page source and asking bs4 to read it as html page
        soup = BeautifulSoup(browser.page_source, "html.parser")

          #when you inspect the page the entire information is wriiten inside li and ui tag
        #we are fetching the information using those tags

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []

                #.inside ui we have to access li tag that we will access using index 
            # enumerate is a function that returns index along with component

            for index, li_tag in enumerate(li_tags):
                if index == 0:

                      #inside the li tag we have "a" tag which contains hyperlink 
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0]) #this is for data with no hyperlink
                    except:
                        temp_list.append("")    #this is for no data
            planet_data.append(temp_list)
             #to move from one page to another we need x path .Inspect on the next arrow ,right click and choose copy the x path from
                #click will instructing the browser to click on next page

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)
scrape()
