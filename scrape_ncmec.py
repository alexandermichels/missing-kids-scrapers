import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

attributes = [
    "missingDate",
    "missingLocation",
    "ageNow",
    "sex",
    "race",
    "hairColor",
    "eyeColor",
    "height",
    "weight"
            ]

output_file = open("NCMEC.csv", "w")
output_csv = csv.writer(output_file)
header_row = ["casenumber", "name", "url"] + [a for a in attributes] + ["narrative"]
output_csv.writerow(header_row)

# open URL and click submit
search_url = "https://www.missingkids.org/gethelpnow/search/poster-results"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="./webdrivers/chromedriver", options=chrome_options)

driver.get(search_url)
submit_button = driver.find_element_by_class_name("missing-filter-submit")
submit_button.click()
time.sleep(3)


another_page = True
while another_page:
    # get list of missing kids
    missing_list = driver.find_element_by_id("missing_lists")
    missing_list = missing_list.find_elements_by_xpath(".//div[@class='missing-person-poster']")
    print(len(missing_list))
    current_window = driver.current_window_handle
    for elem in missing_list:
        try:
            name = elem.find_element_by_class_name("missing-person-name")
            name_val = name.text
            name.click()
            time.sleep(5)  # wait for the page to load
            driver.switch_to.window(driver.window_handles[1])
            casenumber = driver.find_element_by_class_name("caseNumber").text
            url = driver.current_url
            attributes_list = driver.find_element_by_class_name("mkPersonAttributes")
            info_dict = {}
            for attribute in attributes:
                info_dict[attribute] = "N/A"
                try:
                    attribute_info = attributes_list.find_element_by_class_name(attribute)
                    value = attribute_info.find_element_by_class_name("value")
                    print(value.text)
                    info_dict[attribute] = value.text
                except Exception as e:
                    print(e)
                    print(attribute_info.get_attribute("innerHTML"))
            print(info_dict)
            narrative = driver.find_element_by_class_name("narrativeTextBlock").text
            to_write = [casenumber, name_val, url] + [info_dict[a] for a in attributes] + [narrative]
            output_csv.writerow(to_write)
            output_file.flush()
        except Exception as e:
            print(e)
            print(driver.current_url)
            # print(driver.find_element_by_tag_name("body").get_attribute("innerHTML"))
            print(elem.get_attribute("innerHTML"))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        #     poster = elem.find_element_by_class_name("missing-person-link").get_attribute('href')
        #     info = elem.find_elements_by_class_name("missing-person-personal-info")
        #     print(len(info))
        #     missing_since = info[0].find_element_by_xpath(".//span").text
        #     missing_from = info[1].find_element_by_xpath(".//span").text
        #     age_now = info[2].find_element_by_xpath(".//span").text
        #     entry = [name, poster, missing_since, missing_from, age_now]
        #     print(entry)
        #     output_csv.writerow(entry)
        #     exit()
    # look for next page button
    next_button = driver.find_element_by_xpath("//*[@id='pagination-demo']/ul/li[6]/a")
    next_button.click()
    time.sleep(3)
output_file.close()