# pip install selenium
# pip install beautifulsoup4
# pip install pandas

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://hprera.nic.in/PublicDashboard'
path = r'C:\DATA\web Scraping\chromedriver-mac-x64\chromedriver'

webdriver.chrome.driver = path

options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
driver.get(url)

wait = WebDriverWait(driver, 300)

element = wait.until(EC.presence_of_element_located((By.ID, "reg-Projects")))
elements = driver.find_elements(By.XPATH, "//a[@data-qs and @title='View Application' and @onclick='tab_project_main_ApplicationPreview($(this));']")[:5]
data_qs_value = []

for element in elements:
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    data_qs_value.append(soup.a['data-qs'])

name_list =[]
pan_no_list = []
gstin_no_list = []
p_address_list=[]
count=1
for data_qs_val in data_qs_value:
    element_2_click = driver.find_element(By.XPATH, "//a[@data-qs='" + data_qs_val + "']")
    element_2_click.click()
    check_element = wait.until(EC.presence_of_element_located((By.ID, "project-menu-html")))
    print("Application " + str(count) + " loaded")
    time.sleep(2)
    
    table_rows = driver.find_elements(By.XPATH, "//table[@class='table table-borderless table-sm table-responsive-lg table-striped font-sm']//tr")
    
    for row in table_rows:
        check_element = row.find_element(By.XPATH, "./td[1]")
        if check_element.text == "Name":
            name = row.find_element(By.XPATH, "./td[2]")
            name_list.append(name.text)
        elif check_element.text == "PAN No.":
            pan_no = row.find_element(By.XPATH, "./td[2]/span")
            pan_no_list.append(pan_no.text)
        elif check_element.text == "GSTIN No.":
            gstin_no = row.find_element(By.XPATH, "./td[2]/span")
            gstin_no_list.append(gstin_no.text)
        elif check_element.text == "Permanent Address":
            p_address = row.find_element(By.XPATH, "./td[2]")
            p_address_list.append(p_address.text)
        
    cross = driver.find_element(By.CLASS_NAME,"close" )
    print("Application " + str(count) + " data scraped successfully")
    cross.click()
    print("Openning next application ")
    count+=1
driver.quit()

for i in range(len(pan_no_list)):
    if pan_no_list[i] == "" or pan_no_list[i] == "-NA-":
        pan_no_list[i] = "N/A"

for i in range(len(gstin_no_list)):
    if gstin_no_list[i] == "" or gstin_no_list[i] == "-NA-":
        gstin_no_list[i] = "N/A"

p_addresses_final = [address.replace(" Address Proof", "").strip() for address in p_address_list]

df = pd.DataFrame({'Name':name_list, 'Pan No': pan_no_list, 'GSTIN No': gstin_no_list, 'Premanent Adrress':p_addresses_final})
df.to_csv('Data.csv', index=False)
print (df)

