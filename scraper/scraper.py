from django.db import models

# Create your models here.
from django.db import models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class University(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH
    
    def scrape_universities(self):
        universities = [
            # Add the 25 Ghanaian universities here
            {"name": "University of Ghana", "url": "https://www.ug.edu.gh/"},
            {"name": "Kwame Nkrumah University of Science and Technology", "url": "https://www.knust.edu.gh/"},
            # ... Add more universities
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
            
            # Extract information (customize these selectors based on the actual website structure)
            location = self.safe_find_element(By.CSS_SELECTOR, ".university-location")
            description = self.safe_find_element(By.CSS_SELECTOR, ".university-description")
            
            # Create or update University model
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

# Usage:
# scraper = Scraper()
# scraper.scrape_universities()
