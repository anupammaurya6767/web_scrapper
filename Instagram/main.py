from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

class InstagramScraper:
    def __init__(self):
        self.driver = None

    def initialize_driver(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    def scrape_user_details(self, username: str):
        """
        Scrapes Instagram user details.

        Args:
            username (str): The Instagram username to scrape.

        Returns:
            dict: A dictionary containing user details.
                  Example:
                  {
                      "Username": "example_user",
                      "Number of Posts": "123",
                      "Number of Followers": "456",
                      "Number of Following": "789"
                  }
        """
        try:
            if not self.driver:
                self.initialize_driver()

            self.driver.get(f"https://www.instagram.com/{username}/")
            wait = WebDriverWait(self.driver, 180)
            account_details = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//span[@class="_ac2a"]')
                )
            )

            user_details = {
                "Username": username,
                "Number of Posts": account_details[0].text,
                "Number of Followers": account_details[1].text,
                "Number of Following": account_details[2].text,
            }

            return user_details

        except Exception as e:
            message = f"{username} not found!"
            return {"Username": username, "data": None, "message": message}
        finally:
            if self.driver:
                self.driver.quit()

# Usage example:
# scraper = InstagramScraper()
# user_details = scraper.scrape_user_details(username="example_user")
# print(user_details)
