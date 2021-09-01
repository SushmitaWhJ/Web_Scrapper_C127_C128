#pip install request
#python C128.py

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("./chromedriver")
browser.get(START_URL)
time.sleep(10)

# adding one more header in the list to save hyperlink of details of the planet
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", 
"planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []
def scrape():
    for i in range(1, 5):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            print(soup)
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value")) 

            #This if condition helps to help us keep the current page num = 1 
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

            #<ul class="expoplanet"></ul>
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            #Inside ul
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            #adding "https://exoplanets.nasa.gov" before the hyperlink of individual planets list            
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")

  #This function is to scrape data for individual planets      
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        #Planet individual information is stored in rows under tag tr (right click over the row)
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            #td tag contains individual information
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    #div tag under td contains the individual info that we are trying to scrap
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    #leaving the blank information
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
scrape()
for index, data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")

   # putting scrapped data in new list
final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
  
    final_planet_data.append(data + new_planet_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)
        csvwriter.writerows(final_planet_data)
