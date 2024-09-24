from django.db import models
from university.models import University

# Create your models here.
from django.db import models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def scrape_universities(self):
        universities = [
            {"name": "University of Ghana", "url": "https://www.ug.edu.gh/"},
            {"name": "Kwame Nkrumah University of Science and Technology", "url": "https://www.knust.edu.gh/"},
        ]
        
        for uni in universities:
            self.scrape_university(uni["name"], uni["url"])
    
    def scrape_university(self, name, url):
        self.driver.get(url)
        
        try:
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            location = self.safe_find_element(By.CSS_SELECTOR, ".university-location")
            description = self.safe_find_element(By.CSS_SELECTOR, ".university-description")
            
            University.objects.update_or_create(
                name=name,
                defaults={
                    'website': url,
                    'location': location,
                    'description': description
                }
            )
            
        except TimeoutException:
            print(f"Timeout while scraping {name}")
        except Exception as e:
            print(f"Error scraping {name}: {str(e)}")
    
    def safe_find_element(self, by, selector):
        try:
            element = self.driver.find_element(by, selector)
            return element.text
        except:
            return ""
    
    def __del__(self):
        self.driver.quit()

# scraper = Scraper()
# scraper.scrape_universities()
