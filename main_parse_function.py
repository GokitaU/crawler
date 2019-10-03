from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException, TimeoutException
from constant_path import *

class Temp_List(list):
    def append(self, item=None):
        if item in (None, ''):
            raise AssertionError
        super().append(item)

class element_has_text(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if str(element.text) not in ('', 'None'):
            return element
        else:
            return False

def move_part(driver, len_of_shift, function, time_scroll):
    STAT = []

    elem = driver.find_elements_by_css_selector(time_scroll)
    X1 = elem[1].location.get('x')
    X0 = elem[0].location.get('x')
    print("INPUT POSSITIONS(X1, X0): ", X1, X0)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, time_scroll)))
    print(len_of_shift)

    action = ActionChains(driver)
    elem = driver.find_elements_by_css_selector(time_scroll)
    action.move_to_element(elem[1])
    action.drag_and_drop_by_offset(elem[1], len_of_shift, 0).perform()

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, time_scroll)))
    elem = driver.find_elements_by_css_selector(time_scroll)
    X1 = elem[1].location.get('x')
    X0 = elem[0].location.get('x')
    print("AFTER TRANSFROM(X1, X0): ", X1, X0)
    print(elem[0].text, "-", elem[1].text)
    try:
        STAT += function(driver)
    except AssertionError:
        print(traceback.format_exc())
        STAT += function(driver)

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, time_scroll)))
    action = ActionChains(driver)
    elem = driver.find_elements_by_css_selector(time_scroll)
    action.move_to_element(elem[0])
    action.drag_and_drop_by_offset(elem[0], X1 - X0 + 5, 0).perform()

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, time_scroll)))
    elem = driver.find_elements_by_css_selector(time_scroll)
    X1 = elem[1].location.get('x')
    X0 = elem[0].location.get('x')
    print("OUTPUT POSSITIONS(X1, X0): ", X1, X0)
    return STAT

def get_text_excluding_children(driver, element):
    return str(driver.execute_script(
        """ return jQuery(arguments[0]).contents().filter(function() { return this.nodeType == Node.TEXT_NODE; }).text(); """,
    element))

def get_text_children(driver, element):
    return str(driver.execute_script(
        """ return jQuery(arguments[0]).children().text(); """,
    element))

def parse_shots_zones(driver, xpath_to_shot_detail):
    on_target_low_left = '0'
    on_target_high_left = '0'
    on_target_low_right = '0'
    on_target_high_right = '0'
    on_target_low_centre = '0'
    on_target_high_centre = '0'
    on_target_low_left_goals = '0'
    on_target_high_left_goals = '0'
    on_target_low_right_goals = '0'
    on_target_high_right_goals = '0'
    on_target_low_centre_goals = '0'
    on_target_high_centre_goals = '0'
    miss_left = '0'
    miss_right = '0'
    miss_high_left = '0'
    miss_high_right = '0'
    miss_high_centre = '0'
    post_left = '0'
    post_right = '0'

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_to_shots_chalkboard)))
    elem = driver.find_element_by_xpath(xpath_to_shots_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()


    stat = driver.find_elements_by_xpath(xpath_to_shot_detail)

    for elem in stat:
        WebDriverWait(driver, 30).until(
            EC.visibility_of(elem))
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowleft has-goals has-goals-and-shots":#left low
            on_target_low_left = get_text_excluding_children(driver, elem)
            on_target_low_left_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowleft has-goals":
            on_target_low_left_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowleft":
            on_target_low_left = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighleft has-goals has-goals-and-shots":  #left high
            on_target_high_left = get_text_excluding_children(driver, elem)
            on_target_high_left_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighleft has-goals":
            on_target_high_left_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighleft":
            on_target_high_left = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowcentre has-goals has-goals-and-shots":  # center low
            on_target_low_centre = get_text_excluding_children(driver, elem)
            on_target_low_centre_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowcentre has-goals":
            on_target_low_centre_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowcentre":
            on_target_low_centre = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighcentre has-goals has-goals-and-shots":  # center high
            on_target_high_centre = get_text_excluding_children(driver, elem)
            on_target_high_centre_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighcentre has-goals":
            on_target_high_centre_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighcentre":
            on_target_high_centre = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowright has-goals has-goals-and-shots":  # right low
            on_target_low_right = get_text_excluding_children(driver, elem)
            on_target_low_right_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowright has-goals":
            on_target_low_right_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargetlowright":
            on_target_low_right = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighright has-goals has-goals-and-shots":  # right high
            on_target_high_right = get_text_excluding_children(driver, elem)
            on_target_high_right_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighright has-goals":
            on_target_high_right_goals = get_text_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone ontargethighright":
            on_target_high_right = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone missleft":#missed left
            miss_left = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone missright":#missed right
            miss_right = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone misshighcentre":#missed center
            miss_high_centre = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone misshighleft":#missed high left
            miss_high_left = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone misshighright":#missed high right
            miss_high_right=get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone postleft":#post left
            post_left = get_text_excluding_children(driver, elem)
        if elem.get_attribute("class").strip() == "shot-zone postright":#post right
            post_right = get_text_excluding_children(driver, elem)
    return [on_target_low_left,
        on_target_high_left,
        on_target_low_right,
        on_target_high_right,
        on_target_low_centre,
        on_target_high_centre,
        on_target_low_left_goals,
        on_target_high_left_goals,
        on_target_low_right_goals,
        on_target_high_right_goals,
        on_target_low_centre_goals,
        on_target_high_centre_goals,
        miss_left,
        miss_right,
        miss_high_left,
        miss_high_right,
        miss_high_centre,
        post_left,
        post_right]

def parse_yc_rc_goals(xpath_to_stat, driver):
    first_formation = "00000"
    second_formation = "00000"
    hf_goals = 0
    ft_goals = 0
    goals_at_0_15 = 0
    goals_at_15_30 = 0
    goals_at_30_45 = 0
    goals_at_45_60 = 0
    goals_at_60_75 = 0
    goals_at_75_90 = 0
    sub_in_at_0_15 = 0
    sub_in_at_15_30 = 0
    sub_in_at_30_45 = 0
    sub_in_at_45_60 = 0
    sub_in_at_60_75 = 0
    sub_in_at_75_90 = 0
    hf_sub_in = 0
    ft_yc = 0
    hf_yc = 0
    yc_at_0_15 = 0
    yc_at_15_30 = 0
    yc_at_30_45 = 0
    yc_at_45_60 = 0
    yc_at_60_75 = 0
    yc_at_75_90 = 0
    ft_rc = 0
    hf_rc = 0
    rc_at_0_15 = 0
    rc_at_15_30 = 0
    rc_at_30_45 = 0
    rc_at_45_60 = 0
    rc_at_60_75 = 0
    rc_at_75_90 = 0

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_to_stat)))
    elem = driver.find_elements_by_xpath(xpath_to_stat)
    for i in elem:
        try:
            if (i.get_attribute("title") == "Formation change" or i.get_attribute("data-minute") == "0") and (
                    first_formation == "00000" or second_formation == "00000"):
                if i.get_attribute("title") == "Formation change":
                    element = str(driver.execute_script(script_show_hidden_content, i).split(' ')[-1])
                    if not element.isdigit():
                        element=element[:-1]
                    second_formation = element+"00000"
                if i.get_attribute("data-minute") == "0":
                    element = str(driver.execute_script(script_show_hidden_content, i).split(' ')[-1])
                    if not element.isdigit():
                        element=element[:-1]
                    first_formation = element+"00000"
        except ValueError:
            first_formation = "42310"
            second_formation = "42310"
        if (i.get_attribute("title") == "Goal" or i.get_attribute("title")=="Own goal" or i.get_attribute("title")=="Penalty scored"):
            ft_goals += 1
            if int(i.get_attribute("data-minute")) <= 45:
                hf_goals += 1
            if int(i.get_attribute("data-minute")) <= 15:
                goals_at_0_15 += 1
            if int(i.get_attribute("data-minute")) > 15 and int(i.get_attribute("data-minute")) <= 30:
                goals_at_15_30 += 1
            if int(i.get_attribute("data-minute")) > 30 and int(i.get_attribute("data-minute")) <= 45:
                goals_at_30_45 += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) <= 60:
                goals_at_45_60 += 1
            if int(i.get_attribute("data-minute")) > 60 and int(i.get_attribute("data-minute")) <= 75:
                goals_at_60_75 += 1
            if int(i.get_attribute("data-minute")) > 75:
                goals_at_75_90 += 1
        if (i.get_attribute("title") == "Sub in"):
            if int(i.get_attribute("data-minute")) <= 45:
                hf_sub_in += 1
            if int(i.get_attribute("data-minute")) <= 15 :
                sub_in_at_0_15 += 1
            if int(i.get_attribute("data-minute")) > 15 and int(i.get_attribute("data-minute")) <= 30:
                sub_in_at_15_30 += 1
            if int(i.get_attribute("data-minute")) > 30 and int(i.get_attribute("data-minute")) <= 45:
                sub_in_at_30_45 += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) <= 60:
                sub_in_at_45_60 += 1
            if int(i.get_attribute("data-minute")) > 60 and int(i.get_attribute("data-minute")) <= 75:
                sub_in_at_60_75 += 1
            if int(i.get_attribute("data-minute")) > 75:
                sub_in_at_75_90 += 1
        if (i.get_attribute("title") == "Yellow Card"):
            ft_yc += 1
            if int(i.get_attribute("data-minute")) <= 45:
                hf_yc += 1
            if int(i.get_attribute("data-minute")) <= 15 :
                yc_at_0_15 += 1
            if int(i.get_attribute("data-minute")) > 15 and int(i.get_attribute("data-minute")) <= 30:
                yc_at_15_30 += 1
            if int(i.get_attribute("data-minute")) > 30 and int(i.get_attribute("data-minute")) <= 45:
                yc_at_30_45 += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) <= 60:
                yc_at_45_60 += 1
            if int(i.get_attribute("data-minute")) > 60 and int(i.get_attribute("data-minute")) <= 75:
                yc_at_60_75 += 1
            if int(i.get_attribute("data-minute")) > 75:
                yc_at_75_90 += 1
        if (i.get_attribute("title") == "Red Card"):
            ft_rc += 1
            if int(i.get_attribute("data-minute")) <= 45:
                hf_rc += 1
            if int(i.get_attribute("data-minute")) <= 15 :
                rc_at_0_15 += 1
            if int(i.get_attribute("data-minute")) > 15 and int(i.get_attribute("data-minute")) <= 30:
                rc_at_15_30 += 1
            if int(i.get_attribute("data-minute")) > 30 and int(i.get_attribute("data-minute")) <= 45:
                rc_at_30_45 += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) <= 60:
                rc_at_45_60 += 1
            if int(i.get_attribute("data-minute")) > 60 and int(i.get_attribute("data-minute")) <= 75:
                rc_at_60_75 += 1
            if int(i.get_attribute("data-minute")) > 75:
                rc_at_75_90 += 1

    if second_formation == "00000":
        second_formation = first_formation
    ff_line_1, ff_line_2, ff_line_3, ff_line_4, ff_line_5 = tuple(first_formation)[:5]
    sf_line_1, sf_line_2, sf_line_3, sf_line_4, sf_line_5 = tuple(second_formation)[:5]
    return [ft_goals,
            ff_line_1, ff_line_2, ff_line_3, ff_line_4, ff_line_5,
            sf_line_1, sf_line_2, sf_line_3, sf_line_4, sf_line_5,
            hf_goals, goals_at_0_15, goals_at_15_30, goals_at_30_45, goals_at_45_60, goals_at_60_75, goals_at_75_90,
            hf_sub_in,
            ft_yc, hf_yc, yc_at_0_15, yc_at_15_30, yc_at_30_45, yc_at_45_60, yc_at_60_75, yc_at_75_90,
            ft_rc, hf_rc, rc_at_0_15, rc_at_15_30, rc_at_30_45, rc_at_45_60, rc_at_60_75, rc_at_75_90
            ]

def parse_live_table(driver):
    MATCH_STAT = Temp_List()

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_raiting_team_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_raiting_team_home).text)

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_raiting_team_away).text)

    elem = driver.find_element_by_xpath(xpath_more_shots)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()

    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, xpath_woodwork_home)))
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_total_shots_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_total_shots_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_on_target_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_on_target_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_off_target_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_off_target_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_blocked_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_shots_blocked_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_woodwork_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_woodwork_away).text)

    elem = driver.find_element_by_xpath(xpath_more_possessions)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, xpath_touches_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_possession_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_possession_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_touches_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_touches_away).text)

    elem = driver.find_element_by_xpath(xpath_more_pass_success)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_accurate_passes_away)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_pass_success_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_pass_success_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_total_passes_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_total_passes_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_accurate_passes_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_accurate_passes_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_key_passes_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_key_passes_away).text)

    elem = driver.find_element_by_xpath(xpath_more_dribbles)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_dribbled_past_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbles_won_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbles_won_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbles_attempted_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbles_attempted_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbled_past_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dribbled_past_away).text)

    elem = driver.find_element_by_xpath(xpath_more_aerials_won)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_offensive_aerials_away)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_aerials_won_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_aerials_won_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_aerials_won_per_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_aerials_won_per_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_offensive_aerials_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_offensive_aerials_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_defensive_aerials_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_defensive_aerials_away).text)

    elem = driver.find_element_by_xpath(xpath_more_tackles)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_interceptions_away)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_successful_tackles_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_successful_tackles_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_tackles_attempted_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_tackles_attempted_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_was_dribbles_tackles_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_was_dribbles_tackles_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_interceptions_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_interceptions_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_clearances_total_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_clearances_total_away).text)

    elem = driver.find_element_by_xpath(xpath_more_corners)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_corner_accuracy_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corners_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corners_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corner_accuracy_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corner_accuracy_away).text)

    elem = driver.find_element_by_xpath(xpath_more_dispossessed)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,xpath_fouls_away)))

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dispossessed_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_dispossessed_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_errors_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_errors_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_fouls_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_fouls_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_offsides_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_offsides_away).text)

    elem = driver.find_element_by_xpath(xpath_more_dispossessed)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click(elem)
    action.perform()


    return MATCH_STAT

def parse_chalkboard(driver):
    MATCH_STAT = Temp_List()

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_to_shots_chalkboard)))
    elem = driver.find_element_by_xpath(xpath_to_shots_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()

    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, shots_situation_fastbreak_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_6_yard_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_6_yard_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_penalty_area_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_penalty_area_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_outside_of_box_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_zones_outside_of_box_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_open_play_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_open_play_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_fastbreak_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_fastbreak_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_set_pieces_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_set_pieces_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_penalty_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_penalty_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_own_goal_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_situation_own_goal_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_right_foot_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_right_foot_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_left_foot_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_left_foot_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_head_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_head_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_other_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(shots_body_part_other_away).text)

    elem = driver.find_element_by_xpath(xpath_to_passes_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, passes_throw_in_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(passes_cross_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_cross_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_freekick_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_freekick_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_through_ball_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_through_ball_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_throw_in_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_throw_in_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_lenght_long_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_lenght_long_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_lenght_short_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_lenght_short_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_height_chipped_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_height_chipped_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_height_ground_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_height_ground_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_body_parts_head_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_body_parts_head_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_body_parts_feet_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_body_parts_feet_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_forward_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_forward_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_backward_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_backward_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_left_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_left_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_right_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_direction_right_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_defensive_third_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_defensive_third_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_mid_third_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_mid_third_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_final_third_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(passes_target_zone_final_third_away).text)

    elem = driver.find_element_by_xpath(xpath_to_dribbles_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,dribbles_unsuccessful_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_successful_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_successful_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_unsuccessful_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_unsuccessful_away).text)

    elem = driver.find_element_by_xpath(xpath_to_tackles_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,tackles_was_dribbled_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(tackles_attempted_succesful_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(tackles_attempted_succesful_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(tackles_was_dribbled_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(tackles_was_dribbled_away).text)

    MATCH_STAT.append(driver.find_element_by_xpath(interceptions_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(interceptions_away).text)

    elem = driver.find_element_by_xpath(xpath_to_clearances_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH,clearances_body_parts_feet_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(clearances_total_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_total_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_off_the_line_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_off_the_line_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_body_parts_head_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_body_parts_head_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_body_parts_feet_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(clearances_body_parts_feet_away).text)

    elem = driver.find_element_by_xpath(xpath_to_blocks_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, blocked_crosses_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(blocked_shots_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_shots_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_crosses_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_crosses_away).text)

    elem = driver.find_element_by_xpath(xpath_to_errors_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    wait_res = WebDriverWait(driver, 30).until(element_has_text((By.XPATH, errors_leads_to_goal_home)))

    MATCH_STAT.append(driver.find_element_by_xpath(errors_leads_to_shot_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(errors_lead_to_shot_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(errors_leads_to_goal_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(errors_leads_to_goal_away).text)

    MATCH_STAT.append(driver.find_element_by_xpath(saves_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(saves_away).text)

    MATCH_STAT.append(driver.find_element_by_xpath(claim_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(claim_away).text)

    MATCH_STAT.append(driver.find_element_by_xpath(punches_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(punches_away).text)

    return MATCH_STAT

def parse_probable_stat(driver):
    MATCH_STAT = Temp_List()

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_probable_stat_goals_home)))

    # Probable stat
    MATCH_STAT.append(driver.find_element_by_css_selector(css_probable_stat_goals_home).text)
    MATCH_STAT.append(driver.find_element_by_css_selector(css_probable_stat_goals_away).text)
    MATCH_STAT.append(driver.find_element_by_css_selector(css_probable_stat_assists_home).text)
    MATCH_STAT.append(driver.find_element_by_css_selector(css_probable_stat_assists_away).text)

    # Тут надо поменять способ чтения
    elem = driver.find_element_by_css_selector(css_probable_stat_average_ratings_home)
    MATCH_STAT.append(str(elem.text).partition(")")[2].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_average_ratings_away)
    MATCH_STAT.append(str(elem.text).partition("(")[0].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_aerial_duel_success_home)
    MATCH_STAT.append(str(elem.text).partition(")")[2][:-1].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_aerial_duel_success_away)
    MATCH_STAT.append(str(elem.text).partition("(")[0][:-2].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_shotspg_home)
    MATCH_STAT.append(str(elem.text).partition(")")[2].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_shotspg_away)
    MATCH_STAT.append(str(elem.text).partition("(")[0].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_dribblespg_home)
    MATCH_STAT.append(str(elem.text).partition(")")[2].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_dribblespg_away)
    MATCH_STAT.append(str(elem.text).partition("(")[0].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_tacklespg_home)
    MATCH_STAT.append(str(elem.text).partition(")")[2].strip())
    elem = driver.find_element_by_css_selector(css_probable_stat_tacklespg_away)
    MATCH_STAT.append(str(elem.text).partition("(")[0].strip())

    return MATCH_STAT

def parse_characteristic(driver):
    MATCH_STAT = Temp_List()

    strongs_home = dict()
    strongs_away = dict()
    weakness_home = dict()
    weakness_away = dict()
    style_home = []
    style_away = []

    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_to_strongs_home)))
    elem = driver.find_elements_by_xpath(xpath_to_strongs_home)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Strong":
            strongs_home.update({str(texts.text).rpartition("\n")[0]:'1'})
        if str(texts.text).rpartition("\n")[2] == "Very Strong":
            strongs_home.update({str(texts.text).rpartition("\n")[0]:'2'})
    wait_res = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, xpath_to_strongs_away)))
    elem = driver.find_elements_by_xpath(xpath_to_strongs_away)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Strong":
            strongs_away.update({str(texts.text).rpartition("\n")[0]:'1'})
        if str(texts.text).rpartition("\n")[2] == "Very Strong":
            strongs_away.update({str(texts.text).rpartition("\n")[0]:'2'})
    wait_res = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_weakness_home)))
    elem = driver.find_elements_by_xpath(xpath_to_weakness_home)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Weak":
            weakness_home.update({str(texts.text).rpartition("\n")[0]:'1'})
        if str(texts.text).rpartition("\n")[2] == "Very Weak":
            weakness_home.update({str(texts.text).rpartition("\n")[0]:'2'})
    wait_res = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_weakness_away)))
    elem = driver.find_elements_by_xpath(xpath_to_weakness_away)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Weak":
            weakness_away.update({str(texts.text).rpartition("\n")[0]:'1'})
        if str(texts.text).rpartition("\n")[2] == "Very Weak":
            weakness_away.update({str(texts.text).rpartition("\n")[0]:'2'})
    wait_res = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_style_home)))
    elem = driver.find_elements_by_xpath(xpath_to_style_home)
    for texts in elem:
        style_home.append(str(texts.text))
    wait_res = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_style_away)))
    elem = driver.find_elements_by_xpath(xpath_to_style_away)
    for texts in elem:
        style_away.append(str(texts.text))
    for i in list_strongs:
        MATCH_STAT.append(strongs_home.pop(i, '0'))
    for i in list_strongs:
        MATCH_STAT.append(strongs_away.pop(i, '0'))
    for i in list_weakness:
        MATCH_STAT.append(weakness_home.pop(i, '0'))
    for i in list_weakness:
        MATCH_STAT.append(weakness_away.pop(i, '0'))
    for i in list_styles:
        if i in style_home:
            MATCH_STAT.append('1')
        else:
            MATCH_STAT.append('0')
    for i in list_styles:
        if i in style_away:
            MATCH_STAT.append('1')
        else:
            MATCH_STAT.append('0')
    return MATCH_STAT

def parse_whoscored(url, driver, db):

    URL = url
    MAIN_TABLE = []
    MAIN_TABLE_SQL = []
    CHARACTERISTIC_TABLE = []
    CHARACTERISTIC_TABLE_SQL = []
    HT_TABLE_STAT = []
    FT_TABLE_STAT = []
    STAT_SQL = []

    driver.get(url)
    try:
        wait_res = WebDriverWait(driver, 60).until(EC.url_contains("https://1xbet."))
    except TimeoutException:
        pass

    #driver.execute_script(script_scroll_down, 700)

    try:
        CHARACTERISTIC_TABLE += parse_characteristic(driver)
    except AssertionError:
        print(traceback.format_exc())
        CHARACTERISTIC_TABLE += parse_characteristic(driver)
    CHARACTERISTIC_TABLE_SQL += sql_columns_of_url
    CHARACTERISTIC_TABLE_SQL += sql_columns_of_characteristic
    assert len(CHARACTERISTIC_TABLE_SQL) == (len(CHARACTERISTIC_TABLE)+1)

    assert url.find("Show") != -1
    url = url.replace("Show", "Preview")
    driver.get(url)
    try:
        wait_res = WebDriverWait(driver, 60).until(EC.url_contains("https://1xbet."))
    except TimeoutException:
        pass

    try:
        CHARACTERISTIC_TABLE += parse_probable_stat(driver)
    except AssertionError:
        print(traceback.format_exc())
        CHARACTERISTIC_TABLE += parse_probable_stat(driver)

    CHARACTERISTIC_TABLE_SQL += sql_columns_of_probable_stat
    assert len(CHARACTERISTIC_TABLE_SQL) == (len(CHARACTERISTIC_TABLE)+1)

    assert url.find("Preview") != -1
    url = url.replace("Preview", "Live")
    driver.get(url)
    try:
        wait_res = WebDriverWait(driver, 60).until(EC.url_contains("https://1xbet."))
    except TimeoutException:
        pass

    CHARACTERISTIC_TABLE.insert(0, "'" + url + "'")
    MAIN_TABLE.append("'" + url + "'")
    HT_TABLE_STAT.append("'" + url + "'")
    FT_TABLE_STAT.append("'" + url + "'")

    MAIN_TABLE_SQL += sql_columns_of_url
    STAT_SQL += sql_columns_of_url
    assert len(MAIN_TABLE_SQL) == len(MAIN_TABLE)


    home_stat = parse_yc_rc_goals(xpath_to_home_stat, driver)
    away_stat = parse_yc_rc_goals(xpath_to_away_stat, driver)

    if home_stat[0] > away_stat[0]:
        MAIN_TABLE.append('1')
    elif home_stat[0] < away_stat[0]:
        MAIN_TABLE.append('2')
    elif home_stat[0] == away_stat[0]:
        MAIN_TABLE.append('0')
    MAIN_TABLE += home_stat
    MAIN_TABLE += away_stat

    MAIN_TABLE_SQL += sql_columns_of_time_stat
    assert len(MAIN_TABLE_SQL) == len(MAIN_TABLE)

    try:
        FT_TABLE_STAT += parse_live_table(driver)
    except AssertionError:
        print(traceback.format_exc())
        FT_TABLE_STAT += parse_live_table(driver)
    STAT_SQL += sql_columns_of_stat
    assert len(STAT_SQL) == len(FT_TABLE_STAT)

    # 1 to 45
    try:
        wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_to_time_scroll)))
        action = ActionChains(driver)
        elem = driver.find_elements_by_css_selector(css_to_time_scroll)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
    except MoveTargetOutOfBoundsException:
        print(traceback.format_exc())
        driver.execute_script(script_scroll_down, 1700)
        wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_to_time_scroll)))
        action = ActionChains(driver)
        elem = driver.find_elements_by_css_selector(css_to_time_scroll)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()


    try:
        HT_TABLE_STAT += parse_live_table(driver)
    except AssertionError:
        print(traceback.format_exc())
        HT_TABLE_STAT += parse_live_table(driver)
    assert len(HT_TABLE_STAT) == len(STAT_SQL)

    #driver.execute_script(script_scroll_down, 600)
    wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, referee)))

    try:
        referee_sub = "'" + driver.find_element_by_xpath(referee).text.strip() + "'"
    except:
        referee_sub = "'"+'Mike Dean'+"'"
    MAIN_TABLE.append(referee_sub)
    MAIN_TABLE_SQL += sql_columns_of_referee
    assert len(MAIN_TABLE) == len(MAIN_TABLE_SQL)

    FIRST_STAT = [str('"'+URL+'"')]
    SECOND_STAT = [str('"'+URL+'"')]
    THIRD_STAT = [str('"'+URL+'"')]
    FOURTH_STAT = [str('"'+URL+'"')]
    FIFTH_STAT = [str('"'+URL+'"')]
    SIX_STAT = [str('"'+URL+'"')]

    FIRST_STAT += move_part(driver, -323, parse_live_table, css_to_time_scroll)
    SECOND_STAT += move_part(driver, 156, parse_live_table, css_to_time_scroll)
    THIRD_STAT += move_part(driver, 154, parse_live_table, css_to_time_scroll)
    FOURTH_STAT += move_part(driver, 185, parse_live_table, css_to_time_scroll)
    FIFTH_STAT += move_part(driver, 170, parse_live_table, css_to_time_scroll)
    SIX_STAT += move_part(driver, 155, parse_live_table, css_to_time_scroll)


    elem = driver.find_element_by_xpath(xpath_to_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click(elem)
    action.perform()

##    driver.execute_script(script_scroll_down, 1100)
    # 1 to 90
    try:
        FT_TABLE_STAT += parse_chalkboard(driver)
        FT_TABLE_STAT += parse_shots_zones(driver,xpath_to_shots_detail_home)
        FT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_away)
    except AssertionError:
        print(traceback.format_exc())
        FT_TABLE_STAT += parse_chalkboard(driver)
        FT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_home)
        FT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_away)


    STAT_SQL += sql_columns_of_chulkboard
    assert len(STAT_SQL) == len(FT_TABLE_STAT)

    # 1 to 45
    try:
        wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_to_time_scroll_chalkboard)))
        elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
    #    time.sleep(5)
    except MoveTargetOutOfBoundsException:
        print(traceback.format_exc())
        driver.execute_script(script_scroll_down, 1700)
        wait_res = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_to_time_scroll_chalkboard)))
        elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
    #    time.sleep(5)

    try:
        HT_TABLE_STAT += parse_chalkboard(driver)
        HT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_home)
        HT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_away)
    except AssertionError:
        print(traceback.format_exc())
        HT_TABLE_STAT += parse_chalkboard(driver)
        HT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_home)
        HT_TABLE_STAT += parse_shots_zones(driver, xpath_to_shots_detail_away)
    assert len(HT_TABLE_STAT) == len(STAT_SQL)


    FIRST_STAT += move_part(driver, -323, parse_chalkboard, css_to_time_scroll_chalkboard)
    SECOND_STAT += move_part(driver, 155, parse_chalkboard, css_to_time_scroll_chalkboard)
    THIRD_STAT += move_part(driver, 155, parse_chalkboard, css_to_time_scroll_chalkboard)
    FOURTH_STAT += move_part(driver, 185, parse_chalkboard, css_to_time_scroll_chalkboard)
    FIFTH_STAT += move_part(driver, 170, parse_chalkboard, css_to_time_scroll_chalkboard)
    SIX_STAT += move_part(driver, 155, parse_chalkboard, css_to_time_scroll_chalkboard)


    print(MAIN_TABLE)
    print(CHARACTERISTIC_TABLE)
    print(FT_TABLE_STAT)
    print(HT_TABLE_STAT)
    print(FIRST_STAT)
    print(SECOND_STAT)
    print(THIRD_STAT)
    print(FOURTH_STAT)
    print(FIFTH_STAT)
    print(SIX_STAT)


    MAIN_TABLE_SQL_string = ""
    for sql_column, stat in zip(MAIN_TABLE_SQL, MAIN_TABLE):
        MAIN_TABLE_SQL_string += sql_column + "=" + str(stat) + ", "
    assert len(MAIN_TABLE_SQL_string)

    cursor = db.cursor()

    assert cursor.execute("SELECT * FROM " + tb_name_main + " WHERE url='" + URL + "';")
    sql = "UPDATE " + tb_name_main + " SET " + str(MAIN_TABLE_SQL_string[:-2]) + " WHERE url='" + URL + "';"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_characteristic+"(" + ",".join(CHARACTERISTIC_TABLE_SQL) + ") VALUES (" + ",".join(CHARACTERISTIC_TABLE)+ ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_full_time + "(" + ",".join(STAT_SQL) + ") VALUES (" + ",".join(
        FT_TABLE_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_half_time + "(" + ",".join(STAT_SQL) + ") VALUES (" + ",".join(
        HT_TABLE_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_1_15_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        FIRST_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_15_30_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        SECOND_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_30_45_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        THIRD_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_45_60_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        FOURTH_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_60_75_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        FIFTH_STAT) + ");"
    cursor.execute(sql)

    sql = "INSERT INTO " + tb_name_75_90_stat + "(" + ",".join(STAT_SQL[:-38]) + ") VALUES (" + ",".join(
        SIX_STAT) + ");"
    cursor.execute(sql)
    db.commit()

    print("DONE!")