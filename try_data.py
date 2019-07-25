#Парсит все матчи сезона для сезонов из list_of_number_of_season
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException,MoveTargetOutOfBoundsException, TimeoutException
from parse_whoscored import parse_whoscored
from selenium.webdriver.firefox.options import Options
import traceback
from constant_path import *
"""
Получает список ссылок на матчи с сайта whoscored.com:
-Сезоны хранятся в списке list_of_number_season
-Все ссылки сохраняются в list_of_matches_per_season

"""
#Расширение для кукисов
# driver.install_addon("C:\\Users\\Наталья\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\61witmx9.selenium\\extensions\\jid1-KKzOGWgsW3Ao4Q@jetpack.xpi", temporary = True)


def open_and_write_Error_file(list_with_matches_per_season, filename="Matches_which_was_no_processed"):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        while list_with_matches_per_season:
            fh.write(str(list_with_matches_per_season.pop()) + '\n')
    except IOError as er:
        print(er)
    finally:
        fh.close()

def open_and_get_Error_file(filename="Matches_which_was_no_processed"):
    fh = None
    queue = []
    try:
        fh = open(filename, encoding="utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if not line:
                continue
            queue.append(line)
    except IOError("Failed in openning file") as er:
        print(er)
    return queue

def open_and_get_Seasons_file(filename="Seasons_which_was_no_processed"):
    fh = None
    queue = []
    try:
        fh = open(filename, encoding="utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if not line:
                continue
            queue.append(str(line))
    except IOError("Failed in openning file") as er:
        print(er)
    return queue

def open_and_write_Seasons_file(list_of_number_of_season, filename="Seasons_which_was_no_processed"):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        while list_of_number_of_season:
            fh.write(str(list_of_number_of_season.pop()) + '\n')
    except IOError as er:
        print(er)
    finally:
        fh.close()

options = Options()
options.headless = True
profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
profile.set_preference("intl.accept_languages", "en")

driver2 = webdriver.Firefox(options=options, firefox_profile=profile)
driver2.install_addon(addon_adblock, temporary=True)

driver = webdriver.Firefox(options=options, firefox_profile=profile)
driver.install_addon(addon_adblock, temporary=True)

list_with_matches_per_season = open_and_get_Error_file()
list_of_number_of_season = open_and_get_Seasons_file()

if list_with_matches_per_season:
    while list_with_matches_per_season:
        url_to_match = list_with_matches_per_season.pop()
        try:
            parse_whoscored(url_to_match, driver2)
        except:
            print(traceback.format_exc())
            list_with_matches_per_season.insert(0, url_to_match)
            open_and_write_Error_file(list_with_matches_per_season)
            open_and_write_Seasons_file(list_of_number_of_season)
            driver2.quit()
            driver.quit()
            exit(-1)
assert list_of_number_of_season

while list_of_number_of_season:
    season = list_of_number_of_season.pop()
    driver.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/"+season+"/England-Premier-League")
    time.sleep(1)
    driver.execute_script(script_scroll_down, 550)
    time.sleep(5)
    elem = driver.find_element_by_xpath("//*[@id=\"link-fixtures\"]")
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click(elem)
    action.perform()
    time.sleep(10)

    driver.execute_script(script_scroll_down, 550)
    time.sleep(10)

    try:
        element = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[2]/div[6]/dl/dd/div/a[1]")
        while element.get_attribute("title") != "No data for previous month":
            elem = driver.find_elements_by_xpath("/html/body/div[6]/div[2]/div[2]/div[8]/table/tbody/*")
            for i in elem:
                if i.get_attribute("class") == "item alt" or i.get_attribute("class") == "item ":
                    subelem = str(i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute("href")).replace("MatchReport", "Show")
                    list_with_matches_per_season.append(subelem)
            action = ActionChains(driver)
            action.move_to_element(element)
            action.click(element)
            action.perform()
            time.sleep(7)
        elem = driver.find_elements_by_xpath("/html/body/div[6]/div[2]/div[2]/div[8]/table/tbody/*")
        for i in elem:
            if i.get_attribute("class") == "item alt" or i.get_attribute("class") == "item ":
                subelem = str(
                    i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute("href")).replace(
                    "MatchReport", "Show")
                list_with_matches_per_season.append(subelem)
    except:
        print(traceback.format_exc())
        list_with_matches_per_season.insert(0, season)
        open_and_write_Error_file(list_with_matches_per_season)
        open_and_write_Seasons_file(list_of_number_of_season)
        driver.quit()
        exit(-1)

    while list_with_matches_per_season:
        url_to_match = list_with_matches_per_season.pop()
        try:
            parse_whoscored(url_to_match, driver2)
        except:
            print(traceback.format_exc())
            list_with_matches_per_season.insert(0, url_to_match)
            open_and_write_Error_file(list_with_matches_per_season)
            open_and_write_Seasons_file(list_of_number_of_season)
            driver.quit()
            driver2.quit()
            exit(-1)