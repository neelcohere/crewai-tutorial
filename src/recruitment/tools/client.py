# ../src/project/tools/client.py

import os
import urllib
from selenium.webdriver.common.by import By
from typing import List, Dict

from recruitment.tools.driver import Driver
from dotenv import load_dotenv
load_dotenv()


class Client:
    def __init__(self) -> None:
        url = 'https://linkedin.com/'
        cookie = {
            "name": "li_at",
            "value": os.environ["LINKEDIN_COOKIE"],
            "domain": ".linkedin.com"
        }
        self.driver = Driver(url, cookie)

    def find_people(self, skills: str) -> List[Dict]:
        skills = skills.split(",")
        search = " ".join(skills)
        encoded_string = urllib.parse.quote(search.lower())
        url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_string}"
        self.driver.navigate(url)

        people = self.driver.get_elements("ul li div div.linked-area")
        results = []
        for person in people:
            try:
                result = {}
                result["name"] = person.find_element(By.CSS_SELECTOR, "span.entity-result__title-line").text
                result["position"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text
                result["location"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__secondary_subtitle").text
            except Exception as e:
                print(e)
                continue
            results.append(result)
        return results

    def close(self) -> None:
        self.driver.close()
