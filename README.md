# Learn Selenium Scrape on LinkedIn Job Post
Thank you to Mert Kucukkuru for his medium article, which inspired this learning project to be created. You can visit it at: https://medium.com/@kurumert/web-scraping-linkedin-job-page-with-selenium-python-e0b6183a5954.

The library that is needed in the code is **selenium** and **pandas**. Install the requirement library and get your web driver (I use chromedriver) and then run the .py file in your code editor. This code includes **automating filling out forms, clicking actions, navigating between pages, passing the page with missing elements, and data scraping**. The code will navigate through specified pages within each page containing 25 job offers. 

Items that are scraped by this code are:
- job title, 
- company name, 
- company location, 
- work method (on-site, remote, or hybrid), 
- post date, 
- work time (internship, part-time, contract, or full-time), and 
- job description. 

The code successfully scrapes 43 job offers from 2 pages and pulls out the data into a .csv and .txt file on 10/31/2022.

## File description
- user_credentials.txt, as a container for your LinkedIn account username & password.
- scrapeCode.py, as the code for data scraping LinkedIn job posts.
- job_offers.csv, as the stored data from the web scraping.
- job_descriptions.txt, as the full description of all offers.
