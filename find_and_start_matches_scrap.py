# Парсит все матчи сезона для сезонов из list_with_number_of_season
from selenium import webdriver
import pymysql
from main_parse_function import parse_whoscored
from selenium.webdriver.firefox.options import Options
import traceback
from constant_path import tb_name_main, db_host, db_passwd, db_port, db_usr, path_to_geckodriver_profile, addon_cookies, addon_adblock_ultim, country_map


"""
Получает список ссылок на матчи с сайта whoscored.com:
-Сезоны хранятся в списке list_of_number_season
-Все ссылки сохраняются в list_of_matches_per_season

"""

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
profile.set_preference("intl.accept_languages", "en")

driver = webdriver.Firefox(options=options, firefox_profile=profile)
driver.set_window_size(1360, 2500)
driver.install_addon(addon_adblock_ultim, temporary=True)
driver.install_addon(addon_cookies, temporary=True)
list_with_all_matches = []
for i in country_map:
    db = pymysql.connect(host=db_host, port=db_port, user=db_usr, passwd=db_passwd, db=country_map.get(i).db_name)
    cursor = db.cursor()
    cursor.execute("SELECT url FROM " + tb_name_main + ";")
    db_response = cursor.fetchall()
    for url_from_db in db_response:
        list_with_all_matches.append(url_from_db[0])
    try_counter = 0
    try:
        while list_with_all_matches:
            url_to_match = list_with_all_matches.pop()
            try:
                sub = cursor.execute(
                    "SELECT * FROM " + tb_name_main + " WHERE url='" + url_to_match.replace("Show", "Live") + "';")
                print(url_to_match.replace("Show", "Live"), ' ', sub)
                if sub == 0:
                    parse_whoscored(url_to_match, driver, db)
            except:
                print(traceback.format_exc())
                driver.quit()
                profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
                profile.set_preference("intl.accept_languages", "en")
                driver = webdriver.Firefox(options=options, firefox_profile=profile)
                driver.set_window_size(1360, 2500)
                driver.install_addon(addon_adblock_ultim, temporary=True)
                driver.install_addon(addon_cookies, temporary=True)
                list_with_all_matches.insert(0, url_to_match)
                try_counter += 1
                print("Current attemp:", try_counter)
                if try_counter == 5:
                    exit(-1)
    finally:
        driver.quit()