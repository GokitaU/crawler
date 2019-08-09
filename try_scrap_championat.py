from selenium import webdriver
import time
import pymysql
import traceback
from selenium.webdriver.firefox.options import Options
from constant_path import tb_name_main, path_to_geckodriver_profile, addon_adblock, addon_cookies, db_passwd, db_host, db_name, db_port, db_usr, template_of_team

"""
Парсит с сhampionat.com данные о турах и командах:
-Шаблон ссылки https://www.championat.com/football/_england/tournament/"+ номер сезона  +"/calendar/
-Команды играющие в данном сезоне должны быть в template_of_team где "Команда с сайта whoscored.com": "Перевод на русский язык с сайта championat.com"
-Все матчи добавляются в matches_list откуда сопоставляются с английским переводом, проверяются на наличие в дб и в случае если в дб их нет записываются
"""


list_of_season = ('1042', '1323', '1764', '2613', '2214', '548', '773')
css_to_current_season = "/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[1]"
css_to_matches = 'html.match-center-page.football.england._adaptive-page body.match-center.tournament div.page div.mc-page.js-main-content div.mc-page-content.tournament div.mc-page-main__wrapper div#stat_data.mc-page-main.js-page-main.js-date-arrows div.js-tournament-filter-content table.table._no-stretch.table-stripe-with-class.table-row-hover.stat-results__table.table-col-hover tbody tr.stat-results__row.js-tournament-filter-row._odd'




for num_season in list_of_season:
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile(path_to_geckodriver_profile)
    profile.set_preference("intl.accept_languages", "en")
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.set_window_size(1360, 768)
    #driver.install_addon(addon_adblock, temporary=True)
    driver.install_addon(addon_cookies, temporary=True)

    driver.get("https://www.championat.com/football/_england/tournament/"+str(num_season)+"/calendar/")
    time.sleep(0.5)
    current_season = str(driver.find_element_by_xpath(css_to_current_season).get_attribute("data-month"))[0:4]
    i = 1
    matches_list = []
    for i in range(380):
         first_team = template_of_team.get((driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[" + str(i+1) + "]/td[5]/div[2]/a[1]/span[2]").text))
         second_team = template_of_team.get((driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[" + str(i+1) + "]/td[5]/div[2]/a[2]/span[2]").text))
         if first_team is None or second_team is None:
             print((first_team, second_team, rounds, current_season))
             print("Team not found")
             driver.quit()
             exit(-1)
         rounds = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr["+str(i+1)+"]").get_attribute("data-tour")
         matches_list.append((first_team, second_team, rounds, current_season))

    db = pymysql.connect(host=db_host, port=db_port, user=db_usr, passwd=db_passwd, db=db_name)
    cursor = db.cursor()
    for i in matches_list:
        try:
            if(not cursor.execute("SELECT * FROM "+ tb_name_main +" WHERE home='" + str(i[0]) + "' && away='" + str(i[1]) + "' && round='" + str(i[2]) + "' && season='" + str(i[3]) + "'")):
                sql = "INSERT INTO " + tb_name_main + " (home, away, round, season) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, i)
        except:
            print(traceback.format_exc())
            print("home=", str(i[0]), "away=", str(i[1]), "round=", str(i[2]), "season=", str(i[3]))
            exit(-1)
        finally:
            driver.quit()
    db.commit()

