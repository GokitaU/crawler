

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pymysql
from pymysql.err import IntegrityError

"""
Парсит с сhampionat.com данные о турах и командах:
-Шаблон ссылки https://www.championat.com/football/_england/tournament/"+ номер сезона  +"/calendar/
-Команды играющие в данном сезоне должны быть в template_of_team где "Команда с сайта whoscored.com": "Перевод на русский язык с сайта championat.com"
-Все матчи добавляются в matches_list откуда сопоставляются с английским переводом, проверяются на наличие в дб и в случае если в дб их нет записываются
"""

template_of_team = {
    'Арсенал': 'Arsenal',
    'Сандерленд': 'Sunderland',
    'Фулхэм': 'Fulham',
    'Норвич Сити': 'Norwich',
    'Куинз Парк Рейнджерс': 'Queens Park Rangers',
    'Суонси Сити': 'Swansea',
    'Рединг': 'Reading',
    'Сток Сити': 'Stoke',
    'Вест Бромвич Альбион': 'West Bromwich Albion',
    'Ливерпуль': 'Liverpool',
    'Вест Хэм Юнайтед': 'West Ham',
    'Астон Вилла': 'Aston Villa',
    'Ньюкасл Юнайтед': 'Newcastle United',
    'Тоттенхэм Хотспур': 'Tottenham',
    'Уиган Атлетик': 'Wigan',
    'Челси': 'Chelsea',
    'Манчестер Сити': 'Manchester City',
    'Саутгемптон': 'Southampton',
    'Эвертон': 'Everton',
    'Манчестер Юнайтед': 'Manchester United',
    'Кардифф Сити': 'Cardiff',
    'Халл Сити': 'Hull',
    'Кристал Пэлас': 'Crystal Palace',
    'Бёрнли': 'Burnley',
    'Лестер Сити': 'Leicester',
    'Борнмут': 'Bournemouth',
    'Уотфорд': 'Watford',
    'Мидлсбро': 'Middlesbrough',
    'Лидс Юнайтед': 'Leeds',
    'Шеффилд Юнайтед': 'Sheffield United',
    'Бристоль Сити': 'Bristol City',
    'Дерби Каунти': 'Derby',
    'Шеффилд Уэнсдей': 'Sheffield Wednesday',
    'Ноттингем Форест': 'Nottingham Forest',
    'Престон Норт Энд': 'Preston',
    'Брентфорд': 'Brentford',
    'Блэкберн Роверс': 'Blackburn',
    'Бирмингем Сити': 'Birmingham',
    'Миллуолл': 'Millwall',
    'Ротерхэм Юнайтед': 'Rotherham',
    'Болтон Уондерерс': 'Bolton',
    'Ипсвич Таун': 'Ipswich',
    'Вулверхэмптон': 'Wolverhampton Wanderers',
    'Хаддерсфилд Таун': 'Huddersfield',
    'Брайтон энд Хоув Альбион': 'Brighton'
}
list_of_season = ('2214', '548', '773', '1042', '1323', '1764', '2613')
css_to_current_season = "/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[1]"
css_to_matches = 'html.match-center-page.football.england._adaptive-page body.match-center.tournament div.page div.mc-page.js-main-content div.mc-page-content.tournament div.mc-page-main__wrapper div#stat_data.mc-page-main.js-page-main.js-date-arrows div.js-tournament-filter-content table.table._no-stretch.table-stripe-with-class.table-row-hover.stat-results__table.table-col-hover tbody tr.stat-results__row.js-tournament-filter-row._odd'

for num_season in list_of_season:
    profile = webdriver.FirefoxProfile(
        "C:\\Users\\Наталья\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\61witmx9.selenium")
    profile.set_preference("intl.accept_languages", "en")

    driver = webdriver.Firefox(firefox_profile=profile)

    driver.install_addon(
        "C:\\Users\\Наталья\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\61witmx9.selenium\\extensions\\{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi",
        temporary=True)

    driver.get("https://www.championat.com/football/_england/tournament/"+str(num_season)+"/calendar/")
    time.sleep(0.5)
    current_season = str(driver.find_element_by_xpath(css_to_current_season).get_attribute("data-month"))[0:4]
    i = 1
    matches_list = []
    while i <= 380:
         try:
             first_team = template_of_team.get((driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[5]/span[1]/a/span").text))
             second_team = template_of_team.get((driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[5]/span[3]/a/span").text))
         except:
             if first_team is None or second_team is None:
                 print("Team not found")
                 driver.quit()
                 exit(0)
         rounds = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[3]/div/div[2]/table/tbody/tr["+str(i)+"]").get_attribute("data-tour")
         matches_list.append((first_team, second_team, rounds, current_season))
         i += 1


    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='epl_2012')
    cursor = db.cursor()
    for i in matches_list:
        try:
            if(not cursor.execute("SELECT * FROM epl_2012 WHERE home='" + str(i[0]) + "' && away='" + str(i[1]) + "' && round='" + str(i[2]) + "' && season='" + str(i[3]) + "'")):
                sql = "INSERT INTO epl_2012 (home, away, round, season) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, i)
        except IntegrityError as er:
            print(er, "home=", str(i[0]), "away=", str(i[1]))
            exit(-1)
    db.commit()
    driver.quit()








