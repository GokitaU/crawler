#Парсит все матчи сезона для сезонов из list_with_number_of_season
from selenium import webdriver
import time
import pymysql
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException,MoveTargetOutOfBoundsException, TimeoutException
from parse_whoscored import parse_whoscored
from selenium.webdriver.firefox.options import Options
import traceback
from constant_path import db_host, db_passwd, db_port, db_name, db_usr, xpath_to_button_prev_month, xpath_to_table_with_matches, path_to_geckodriver_profile, addon_cookies, addon_adblock, script_scroll_down, Matches_wich_was_no_processed_filepath, Seasons_wich_was_no_processed_filepath
"""
Получает список ссылок на матчи с сайта whoscored.com:
-Сезоны хранятся в списке list_of_number_season
-Все ссылки сохраняются в list_of_matches_per_season

"""
#Расширение для кукисов
# driver.install_addon("C:\\Users\\Наталья\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\61witmx9.selenium\\extensions\\jid1-KKzOGWgsW3Ao4Q@jetpack.xpi", temporary = True)

def open_and_write_Error_file(list_with_matches_per_season, filename=Matches_wich_was_no_processed_filepath):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        while list_with_matches_per_season:
            fh.write(str(list_with_matches_per_season.pop()) + '\n')
    except IOError as er:
        print(traceback.format_exc())
        exit(-1)
    finally:
        fh.close()

def open_and_get_Error_file(filename = Matches_wich_was_no_processed_filepath):
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
        print(traceback.format_exc())
        exit(-1)
    return queue


def open_and_get_Seasons_file(filename=Seasons_wich_was_no_processed_filepath):
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
        print(traceback.format_exc())
        exit(-1)
    return queue

def open_and_write_Seasons_file(list_with_number_of_season, filename=Seasons_wich_was_no_processed_filepath):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        while list_with_number_of_season:
            fh.write(str(list_with_number_of_season.pop()) + '\n')
    except IOError as er:
        print(traceback.format_exc())
        exit(-1)
    finally:
        fh.close()

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
profile.set_preference("intl.accept_languages", "en")

driver2 = webdriver.Firefox(options=options, firefox_profile=profile)
driver2.set_window_size(1360, 2000)
driver2.install_addon(addon_adblock, temporary=True)
driver2.install_addon(addon_cookies, temporary=True)
list_with_all_matches = open_and_get_Error_file()
list_with_number_of_season = open_and_get_Seasons_file()

if not list_with_all_matches:
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.install_addon(addon_adblock, temporary=True)
    driver.install_addon(addon_cookies, temporary=True)
    driver.set_window_size(1360, 2000)
    for j in range(10):
        while list_with_number_of_season:
            season = list_with_number_of_season.pop()
            driver.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/"+season+"/England-Premier-League")


            elem = driver.find_element_by_xpath("//*[@id=\"link-fixtures\"]")
            action = ActionChains(driver)
            action.move_to_element(elem)
            action.click(elem)
            action.perform()
            time.sleep(10)

            try:
                list_with_matches_per_season = []
                element = driver.find_element_by_xpath(xpath_to_button_prev_month)
                while element.get_attribute("title") != "No data for previous month":
                    elem = driver.find_elements_by_xpath(xpath_to_table_with_matches)
                    for i in elem:
                        if i.get_attribute("class") in ("item alt", "item "):
                            subelem = str(i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute("href")).replace("MatchReport", "Show")
                            list_with_matches_per_season.append(subelem)
                    action = ActionChains(driver)
                    action.move_to_element(element)
                    action.click(element)
                    action.perform()
                    time.sleep(7)
                elem = driver.find_elements_by_xpath(xpath_to_table_with_matches)
                for i in elem:
                    if i.get_attribute("class") in ("item alt", "item "):
                        subelem = str(
                            i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute("href")).replace(
                            "MatchReport", "Show")
                        list_with_matches_per_season.append(subelem)
                assert len(list_with_matches_per_season)==380
                list_with_all_matches += list_with_matches_per_season
                print("Well done with season:", season, len(list_with_all_matches))
            except:
                print(traceback.format_exc())
                list_with_number_of_season.insert(0, season)
                if j == 9:
                    open_and_write_Seasons_file(list_with_number_of_season)
                    open_and_write_Error_file(list_with_all_matches)
                    driver.quit()
                    driver2.quit()
                    exit(-1)
        open_and_write_Error_file(list_with_all_matches)
        open_and_write_Seasons_file(list_with_number_of_season)
        driver.quit()

db = pymysql.connect(host=db_host, port=db_port, user=db_usr, passwd=db_passwd, db=db_name)
j = 0
try:
    while list_with_all_matches:
        url_to_match = list_with_all_matches.pop()
        try:
            if db.cursor().execute("SELECT * FROM " + db_name + " WHERE url='"+url_to_match.replace("Show", "Live") +"' && referee='';")==0:
                parse_whoscored(url_to_match, driver2, db)
        except:
            print(traceback.format_exc())
            driver2.save_screenshot('screen.png')
            list_with_all_matches.insert(0, url_to_match)
            j += 1
            if j == 9:
                open_and_write_Error_file(list_with_all_matches)
                driver2.quit()
                exit(-1)
finally:
    open_and_write_Error_file(list_with_all_matches)
    driver2.quit()

