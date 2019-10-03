# Парсит все матчи сезона для сезонов из list_with_number_of_season
from selenium import webdriver
import time
import pymysql
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException, TimeoutException, \
    WebDriverException
from main_parse_function import parse_whoscored
from selenium.webdriver.firefox.options import Options
import traceback
from constant_path import tb_name_main, db_host, db_passwd, db_port, db_name, db_usr, xpath_to_button_prev_month, \
    xpath_to_table_with_matches, path_to_geckodriver_profile, addon_cookies, addon_adblock_ultim, script_scroll_down, \
    Matches_wich_was_no_processed_filepath, Seasons_wich_was_no_processed_filepath, country_map
from collections import namedtuple



options = Options()
options.headless = True


def main_get(country):
    list_with_number_of_season = country_map.get(country).Seasons

    profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
    profile.set_preference("intl.accept_languages", "en")

    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.install_addon(addon_adblock_ultim, temporary=True)
    driver.install_addon(addon_cookies, temporary=True)
    driver.set_window_size(1360, 2000)

    db = pymysql.connect(host=db_host, port=db_port, user=db_usr, passwd=db_passwd, db=country_map.get(country).db_name)

    for j in range(2012, 2019):
        SQL = "INSERT INTO " + tb_name_main + " (url, home, away, season) VALUES"
        season = list_with_number_of_season[j-2012]
        driver.get(
            "https://www.whoscored.com/Regions/"+country_map.get(country).Regions+"/Tournaments/"+country_map.get(country).Tournaments+"/Seasons/" + season + "/"+country_map.get(country).League)
        time.sleep(10)

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
                    if (i.get_attribute("class") in ("item alt", "item "))and (i.find_element_by_css_selector("td:nth-child(3) > span:nth-child(1)").text == 'FT'):
                        url = str(
                            i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute(
                                "href")).replace("MatchReport", "Show")
                        home = i.find_element_by_css_selector("td:nth-child(4) > a").text
                        away = i.find_element_by_css_selector("td:nth-child(6) > a").text
                        SQL += " ('"+str(url)+"', '"+str(home)+"', '"+str(away)+"', "+str(j)+"),"
                        list_with_matches_per_season.append(url)
                action = ActionChains(driver)
                action.move_to_element(element)
                action.click(element)
                action.perform()
                time.sleep(7)
            elem = driver.find_elements_by_xpath(xpath_to_table_with_matches)
            for i in elem:
                if (i.get_attribute("class") in ("item alt", "item "))and (i.find_element_by_css_selector("td:nth-child(3) > span:nth-child(1)").text == 'FT'):
                    url = str(
                        i.find_element_by_css_selector("td:nth-child(7) > a:nth-child(1)").get_attribute(
                            "href")).replace("MatchReport", "Show")
                    home = i.find_element_by_css_selector("td:nth-child(4) > a").text
                    away = i.find_element_by_css_selector("td:nth-child(6) > a").text
                    SQL += " ('" + str(url) + "', '" + str(home) + "', '" + str(away) + "', " + str(j) + "),"
                    list_with_matches_per_season.append(url)
            print(SQL[:-1]+";")
            db.cursor().execute(SQL[:-1]+";")
            print("Well done with season:", season, len(list_with_matches_per_season))
        except:
            print(traceback.format_exc())
            driver.quit()
            exit()
        db.commit()
    driver.quit()

for i in country_map:
    main_get(i)
