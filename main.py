DATA_CONTAINER_CLASS = "cntanr"
LOADER_CLASS = "ldmore"
MAX_ATTEMPTS = 4
STORE_NAME_CLASS = "store-name"
RATING_SELECTOR = ".newrtings .green-box"
CONTACT_CONTAINER_CLASS = "contact-info"
CONTACT_DIGIT_CLASS = 'mobilesv'
ADDRESS_CLASS = "address-info"
URL = "https://www.justdial.com/Delhi/House-On-Rent/nct-10192844"

CLASS_TO_NUMERIC = {
    "icon-dc": "+",
    "icon-fe": "(",
    "icon-hg": ")",
    "icon-ba": "-",
    "icon-acb": "0",
    "icon-yz": "1",
    "icon-wx": "2",
    "icon-vu": "3",
    "icon-ts": "4",
    "icon-rq": "5",
    "icon-po": "6",
    "icon-nm": "7",
    "icon-lk": "8",
    "icon-ji": "9",
}

# for speeding up the process of extraction (not implemented yet)
ENABLE_MUTITHREADING = False 
OUTPUT_FILE = 'out.json'


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import sys





class Scrapper(webdriver.Firefox):
    def __init__(self):
        options = Options()
        options.headless = True
        webdriver.Firefox.__init__(self, options=options)

    def scroll(self, scroll_height):
        self.execute_script(f"window.scrollBy(0, {str(scroll_height)})")

    def scroll_to_end(self):
        scroll_height = 3000

        attempts = 0
        while attempts < MAX_ATTEMPTS:
            self.scroll(scroll_height)
            display = self.find_element_by_class_name(
                LOADER_CLASS
            ).value_of_css_property("display")

            if display == "block":
                attempts = 0
            else:
                attempts += 1


class Extractor:
    def __init__(self, data_container):
        self.data_container = data_container

    def get_contact(self):
        contact_container = self.data_container.find_element_by_class_name(CONTACT_CONTAINER_CLASS)
        contact_number = ""
        for digit in contact_container.find_elements_by_class_name(CONTACT_DIGIT_CLASS):
            for _class in digit.get_attribute('class').split(" "):
                try:
                    contact_number += CLASS_TO_NUMERIC[_class]
                except:
                    pass

        return contact_number

    def get_address(self):
        return self.data_container.find_element_by_class_name(ADDRESS_CLASS).text

    def get_name(self):
        return self.data_container.find_element_by_class_name(STORE_NAME_CLASS).text

    def get_rating(self):
        return self.data_container.find_element_by_css_selector(RATING_SELECTOR).text

    def get_json(self):
        obj = {
        "name" : self.get_name(),
        "rating" : self.get_rating(),
        "phone" : self.get_contact(),
        "address" : self.get_address()
        }

        return json.dumps(obj)




driver = Scrapper()
driver.get(URL)
driver.scroll_to_end()

data_containers = driver.find_elements_by_class_name(DATA_CONTAINER_CLASS)



if not ENABLE_MUTITHREADING:
    sys.stdout = open(OUTPUT_FILE, 'w')

    print("[")  

    for data_container in data_containers:
        extractor = Extractor(data_container)
        print(extractor.get_json(), end=',\n')

    print("]")

    sys.stdout.close()


else:
    # not implemented yet
    pass