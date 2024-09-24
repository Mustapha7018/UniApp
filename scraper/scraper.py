import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from university.models import University
import time

class Scraper:
    def __init__(self, driver_path='chromedriver', headless=True, excel_path='output/universities.xlsx'):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.excel_path = excel_path
        self.data = []  

    def scrape_universities(self):
        universities = [
            {"name": "University of Ghana", "url": "https://www.ug.edu.gh/"},
            {"name": "Kwame Nkrumah University of Science and Technology", "url": "https://www.knust.edu.gh/"},
            {"name": "University of Cape Coast", "url": "https://www.ucc.edu.gh/"},
            {"name": "University of Education, Winneba", "url": "https://www.uew.edu.gh/"},
            {"name": "University of Professional Studies, Accra", "url": "https://www.upsa.edu.gh/"},
            {"name": "University of Mines and Technology", "url": "https://www.ug.edu.gh/"},
            {"name": "University of Energy and Natural Resources", "url": "https://www.ug.edu.gh/"},
            {"name": "University for Development Studies", "url": "https://www.univdevstudies.edu.gh/"},
            {"name": "University of Health and Allied Sciences", "url": "https://www.ug.edu.gh/"},
            {"name": "Ashesi University", "url": "https://www.ashesi.edu.gh/"},
            {"name": "Valley View University", "url": "https://www.valleyview.edu.gh/"},
            {"name": "Covenant University", "url": "https://www.covenantuniversity.edu.gh/"},
            {"name": "Central University", "url": "https://www.centraluniversity.edu.gh/"},
            {"name": "All Nations University", "url": "https://www.allnationsuniversity.edu.gh/"},
            {"name": "Catholic University of Ghana", "url": "https://www.catholic.org.gh/"},
            {"name": "Regent University College of Science and Technology", "url": "https://www.regentuniversity.edu.gh/"},
            {"name": "Tekedia University", "url": "https://www.tekediauniversity.edu.gh/"},
            {"name": "Pentecost University", "url": "https://www.pent.edu.gh/"},
            {"name": "Mountcrest University College", "url": "https://www.mountcrest.edu.gh/"},
            {"name": "KAAF University College", "url": "https://www.kaafuniversity.edu.gh/"},
            {"name": "Zenith University College", "url": "https://www.zenithuniversity.edu.gh/"},
            {"name": "Ghana Christian University College", "url": "https://www.gchristianuniversity.edu.gh/"},
            {"name": "BlueCrest College", "url": "https://www.bluecrestcollege.edu.gh/"},
            {"name": "Dominion University College", "url": "https://www.dominionuniversity.edu.gh/"},
            {"name": "Michael Essien University (MEU)", "url": "https://www.meu.edu.gh/"},
            {"name": "Simon's University College", "url": "https://www.simonsuniversity.edu.gh/"},
            {"name": "Lotus International University College", "url": "https://www.lotusuniversity.edu.gh/"},
            {"name": "Gaia University College", "url": "https://www.gaiau.edu.gh/"},
            {"name": "International University College", "url": "https://www.iuc.edu.gh/"},
            {"name": "Wisconsin International University College", "url": "https://www.wiuc.edu.gh/"},
            {"name": "Maranatha University College", "url": "https://www.maranathauniversity.edu.gh/"},
            {"name": "Kings University College", "url": "https://www.kingsuniversity.edu.gh/"},
            {"name": "Knutsford University College", "url": "https://www.knutsford.edu.gh/"},
            {"name": "Meds University College", "url": "https://www.medsuniversity.edu.gh/"},
            {"name": "SD Dombo University of Business and Integrated Development Studies", "url": "https://ubids.edu.gh/"},
            {"name": "St. Francis College of Education", "url": "https://www.stfrancis.edu.gh/"},
            {"name": "Akenten Appiah-Menka University of Skills Training and Entrepreneurial Development", "url": "https://www.akenten.edu.gh/"},
            {"name": "Evangelical Presbyterian University College", "url": "https://www.eppuc.edu.gh/"},
            {"name": "Jayee University College", "url": "https://www.jayeeuniversity.edu.gh/"},
            {"name": "Sammy and Florence University College", "url": "https://www.sammyflorence.edu.gh/"},
            {"name": "Faithford University College", "url": "https://www.faithford.edu.gh/"},
            {"name": "Pilgrims University College", "url": "https://www.pilgrimsuniversity.edu.gh/"},
            {"name": "SoS International University College", "url": "https://www.sosinternational.edu.gh/"},
            {"name": "Eastend University College", "url": "https://www.eastenduniversity.edu.gh/"},
            {"name": "Harbour University College", "url": "https://www.harbouruniversity.edu.gh/"},
            {"name": "Nimble University College", "url": "https://www.nimbleuniversity.edu.gh/"},
            {"name": "Talent University College", "url": "https://www.talentuniversity.edu.gh/"},
            {"name": "New Horizons University College", "url": "https://www.newhorizonsuniversity.edu.gh/"},
            {"name": "Winneba Business School", "url": "https://www.winnewabaschool.edu.gh/"}
            ]
        
        for uni in universities:
            self.scrape_university(uni["name"], uni["url"])
            time.sleep(2)  
        
        self.export_to_excel()
        
        for uni in universities:
            self.scrape_university(uni["name"], uni["url"])
            time.sleep(2)  
        
        self.export_to_excel()

    def scrape_university(self, name, url):
        self.driver.get(url)
        
        try:
            # Wait for the main content to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Scrape Name
            university_name = self.get_text(By.TAG_NAME, "h1") or name
            
            # Scrape Type (Public/Private)
            university_type = self.get_text(By.XPATH, "//span[contains(text(), 'Public') or contains(text(), 'Private')]")
            
            # Scrape Logo
            logo_url = self.get_attribute(By.CSS_SELECTOR, "img.logo", "src")
            
            # Scrape Banner
            banner_url = self.get_attribute(By.CSS_SELECTOR, ".banner img", "src")
            
            # Scrape Card Image
            card_image_url = self.get_attribute(By.CSS_SELECTOR, ".card-image img", "src")
            
            # Scrape Location (City, Region)
            location_text = self.get_text(By.CSS_SELECTOR, ".location")
            city, region = self.parse_location(location_text)
            
            # Scrape About (Description)
            about_text = self.get_text(By.CSS_SELECTOR, ".about-section p")
            
            # Scrape General Entry Requirements
            entry_requirements = self.get_text(By.CSS_SELECTOR, ".entry-requirements")
            
            # Scrape Address
            address = self.get_text(By.CSS_SELECTOR, ".address-section")
            
            # Scrape Website Link
            website_link = url
            
            # Scrape Social Media Links
            twitter_link = self.get_attribute(By.CSS_SELECTOR, "a.twitter", "href")
            facebook_link = self.get_attribute(By.CSS_SELECTOR, "a.facebook", "href")
            instagram_link = self.get_attribute(By.CSS_SELECTOR, "a.instagram", "href")
            linkedin_link = self.get_attribute(By.CSS_SELECTOR, "a.linkedin", "href")
            
            # Scrape Map Location
            map_url = self.get_attribute(By.CSS_SELECTOR, "iframe.map", "src")
            
            # Scrape Resources
            additional_info = self.get_text(By.XPATH, "//div[@class='resources']//div[contains(@class, 'additional-info')]")
            discover = self.get_text(By.XPATH, "//div[@class='resources']//div[contains(@class, 'discover')]")
            useful_links = self.get_text(By.XPATH, "//div[@class='resources']//div[contains(@class, 'useful-links')]")
            
            # Scrape Undergraduate and Graduate Links
            undergrad_link = self.get_attribute(By.CSS_SELECTOR, "a.undergraduate", "href")
            graduate_link = self.get_attribute(By.CSS_SELECTOR, "a.graduate", "href")
            
            # Append the scraped data to the list
            self.data.append({
                'Name': university_name,
                'Type': university_type,
                'Logo URL': logo_url,
                'Banner URL': banner_url,
                'Card Image URL': card_image_url,
                'City': city,
                'Region': region,
                'About': about_text,
                'General Entry Requirements': entry_requirements,
                'Address': address,
                'Website Link': website_link,
                'Twitter': twitter_link,
                'Facebook': facebook_link,
                'Instagram': instagram_link,
                'LinkedIn': linkedin_link,
                'Map URL': map_url,
                'Resources - Additional Info': additional_info,
                'Resources - Discover': discover,
                'Resources - Useful Links': useful_links,
                'Undergraduate Link': undergrad_link,
                'Graduate Link': graduate_link,
            })

            # Update or Create University Instance
            University.objects.update_or_create(
                name=university_name,
                defaults={
                    'type': university_type,
                    'logo': logo_url,
                    'banner': banner_url,
                    'card_image': card_image_url,
                    'city': city,
                    'region': region,
                    'about': about_text,
                    'general_entry_requirements': entry_requirements,
                    'address': address,
                    'website_link': website_link,
                    'twitter': twitter_link,
                    'facebook': facebook_link,
                    'instagram': instagram_link,
                    'linkedin': linkedin_link,
                    'map_location': map_url,
                    'resources_additional_info': additional_info,
                    'resources_discover': discover,
                    'resources_useful_links': useful_links,
                    'undergraduate_link': undergrad_link,
                    'graduate_link': graduate_link,
                }
            )
            
            print(f"Successfully scraped data for {university_name}")

        except TimeoutException:
            print(f"Timeout while scraping {name}")
        except NoSuchElementException as e:
            print(f"Element not found while scraping {name}: {e}")
        except Exception as e:
            print(f"Error scraping {name}: {str(e)}")

    def get_text(self, by, value):
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            return element.text.strip()
        except TimeoutException:
            return ""

    def get_attribute(self, by, value, attribute):
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            return element.get_attribute(attribute)
        except TimeoutException:
            return ""

    def parse_location(self, location_text):
        if location_text:
            parts = location_text.split(",")
            city = parts[0].strip() if len(parts) > 0 else ""
            region = parts[1].strip() if len(parts) > 1 else ""
            return city, region
        return "", ""

    def export_to_excel(self):
        df = pd.DataFrame(self.data)
        df.to_excel(self.excel_path, index=False)
        print(f"Data exported to {self.excel_path}")

    def __del__(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = Scraper(driver_path='chromedriver',
                      headless=True,
                      excel_path='output/universities.xlsx')
    scraper.scrape_universities()