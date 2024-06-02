import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid
from config import EMAIL, PASSWORD, USERNAME, PROXY_LIST
import requests

# Function to initialize WebDriver with ProxyMesh
def get_driver():
    proxy = random.choice(PROXY_LIST)
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--proxy-server=%s' % proxy) 
    service = Service("chromedriver-win64\chromedriver.exe")  # Update path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to log in to Twitter via Google
def twitter_login(driver):
    driver.get("https://x.com/i/flow/login")
    
    # Wait for the email input field and enter the email
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "text"))
    )
    email_input.send_keys(EMAIL)
    email_input.send_keys(u'\ue007')  # Press Enter

    # Check if additional step for phone/username is required
    try:
        phone_username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "text"))
        )
        phone_username_input.send_keys(USERNAME)
        phone_username_input.send_keys(u'\ue007')  # Press Enter
    except:
        # Proceed if the additional step is not required
        pass

    # Wait for the password input field and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )
    password_input.send_keys(PASSWORD)
    password_input.send_keys(u'\ue007')  # Press Enter

    # Wait for the main page to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='sidebarColumn']")))

# Function to fetch trending topics
def fetch_trending_topics(driver):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now']"))
    )
    trends = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] div[data-testid='trend'] div[dir='ltr']:nth-of-type(2) span:not(:has(span))")
    top_trends = [trend.text for trend in trends[:5]]
    return top_trends

# Function to fetch the current IP address using an external service
def get_current_ip():
    response = requests.get("https://httpbin.org/ip")
    ip_address = response.json()["origin"]
    return ip_address

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trending']

# Main function
def main():
    driver = get_driver()
    try:
        twitter_login(driver)
        top_trends = fetch_trending_topics(driver)
        unique_id = str(uuid.uuid4())
        ip_address = get_current_ip()  # Fetch the current IP address
        end_time = datetime.now()
        
        # Store results in MongoDB
        result = {
            "unique_id": unique_id,
            "trend1": top_trends[0] if len(top_trends) > 0 else "",
            "trend2": top_trends[1] if len(top_trends) > 1 else "",
            "trend3": top_trends[2] if len(top_trends) > 2 else "",
            "trend4": top_trends[3] if len(top_trends) > 3 else "",
            "trend5": top_trends[4] if len(top_trends) > 4 else "",
            "date_time": end_time,
            "ip_address": ip_address
        }
        collection.insert_one(result)
    finally:
        print("task finished")
        driver.close()

if __name__ == "__main__":
    main()
