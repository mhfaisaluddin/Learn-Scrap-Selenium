import time
import pandas as pd

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

## PART I
# setup the path for the webdriver
path = 'C:/Users/User/Downloads/chromedriver.exe'
driver = webdriver.Chrome(path)

# maximizing the window
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# entering the site 
driver.get('https://www.linkedin.com/login')
time.sleep(2) 
# time.sleep(n): made the program wait n sec to be sure that the page is loaded

# user credentials
# reading txt file store your account id and password
with open('user_credentials.txt', 'r',encoding='utf-8') as file:
    user_credentials = file.readlines()
    user_credentials = [line.rstrip() for line in user_credentials]

# your account username & password
user_name = user_credentials[0] 
password = user_credentials[1] 

# input username & password
driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(user_name)
driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
time.sleep(2)

# login button
driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(20)

# visiting job page
driver.find_element(By.XPATH,'//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
time.sleep(3)

# go to job search result 
search_keyword = 'data science'
search_loc = 'indonesia'
driver.find_element(By.XPATH,'//*[@id="global-nav-search"]/div/div[2]/div[2]').click()
driver.find_element(By.XPATH, '//*[@id="jobs-search-box-keyword-id-ember249"]').send_keys(search_keyword)
driver.find_element(By.XPATH, '//*[@id="jobs-search-box-location-id-ember249"]').send_keys(search_loc + '\n')
time.sleep(2)


## PART II 
# get all links for the job offers
links = []

print('Links are being collected now.')
try:
    # navigate 2 pages
    for page in range (2,4): 
        time.sleep(2)
        jobs_block = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')

        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME, 'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith('https://www.linkedin.com/jobs/view') and a.get_attribute('href') not in links:
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down
            driver.execute_script('arguments[0].scrollIntoView();', job)

        print(f'Collecting the links in the page : {page-1}')
        # go to next page through loop
        driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']").click()
        time.sleep(3)
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers.')

# try and except: pass block in case there is a missing element in a page,
# it prevents automation from failing and stopping the whole process instead of passing the problematic 1 specific page 


## PART III
# create empty list to store the info
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = []
job_desc = []

i = 0 ; j = 1

# visit each link one by one to scrape the info
print('Visiting the links and collecting info just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(3)
        # click 'see more'
        driver.find_element(By.CLASS_NAME, 'artdeco-card__actions').click()
        time.sleep(2)
    except:
        pass

    # find the general information from the job offers
    contents = driver.find_elements(By.CLASS_NAME, 'p5')
    for content in contents:
        try:
            job_titles.append(content.find_element(By.TAG_NAME,'h1').text)
            company_names.append(content.find_element(By.CLASS_NAME,'jobs-unified-top-card__company-name').text)
            company_locations.append(content.find_element(By.CLASS_NAME,'jobs-unified-top-card__bullet').text)
            work_methods.append(content.find_element(By.CLASS_NAME,'jobs-unified-top-card__workplace-type').text)
            post_dates.append(content.find_element(By.CLASS_NAME,'jobs-unified-top-card__posted-date').text)
            work_times.append(content.find_element(By.CLASS_NAME,'jobs-unified-top-card__job-insight').text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+=1
        except:
            pass
        time.sleep(2)

    # scraping the job description
    job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME,'jobs-box__html-content').text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(4)


# PART IV
# creating the dataframe
df = (pd.DataFrame(list(zip(job_titles,company_names,company_locations,
                            work_methods,post_dates,work_times)),
                            columns=['job_title','company_name','company_location',
                                    'work_method','post_date','work_time']))

# storing into csv file
df.to_csv('job_offers.csv', index=False)

# pull out the job description as txt file
with open('job_descriptions.txt', 'w',encoding='utf-8') as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')

print(f'Finished scraping {j-1} offers and storing them in job_offers.csv')