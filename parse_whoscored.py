from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time
import pymysql
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from constant_path import *

class Temp_List(list):
    def append(self, item=None):
        assert item is not None
        super().append(item)

def parse_yc_rc_goals(xpath_to_stat, driver):
    first_formation = 0
    second_formation = 0
    goals_at_hf = 0
    goals_total = 0
    goals_at_60_ft = 0
    goals_at_45_to_60 = 0
    sub_in_45_to_60 = 0
    sub_in_until_45 = 0
    sub_in_60_ft = 0
    yc_total = 0
    yc_45_to_60 = 0
    yc_until_45 = 0
    yc_60_ft = 0
    rc_total = 0
    rc_45_to_60 = 0
    rc_until_45 = 0
    rc_60_ft = 0
    elem = driver.find_elements_by_xpath(xpath_to_stat)
    for i in elem:
        try:
            if (i.get_attribute("title") == "Formation change" or i.get_attribute("data-minute") == "0") and (
                    first_formation == 0 or second_formation == 0):
                if (i.get_attribute("title") == "Formation change"):
                    element = driver.execute_script(script_show_hidden_content, i).split(' ')
                    second_formation = int(element[-1])
                if i.get_attribute("data-minute") == "0":
                    element = driver.execute_script(script_show_hidden_content, i).split(' ')
                    first_formation = int(element[-1])
        except ValueError:
            first_formation = 4231
            second_formation = 4231
        if (i.get_attribute("title") == "Goal"):
            goals_total += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) < 61:
                goals_at_45_to_60 += 1
            if int(i.get_attribute("data-minute")) <= 45:
                goals_at_hf += 1
            if int(i.get_attribute("data-minute")) > 60:
                goals_at_60_ft += 1
        if (i.get_attribute("title") == "Sub in"):
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) < 61:
                sub_in_45_to_60 += 1
            if int(i.get_attribute("data-minute")) <= 45:
                sub_in_until_45 += 1
            if int(i.get_attribute("data-minute")) > 60:
                sub_in_60_ft += 1
        if (i.get_attribute("title") == "Yellow Card"):
            yc_total += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) < 61:
                yc_45_to_60 += 1
            if int(i.get_attribute("data-minute")) <= 45:
                yc_until_45 += 1
            if int(i.get_attribute("data-minute")) > 60:
                yc_60_ft += 1
        if (i.get_attribute("title") == "Red Card"):
            rc_total += 1
            if int(i.get_attribute("data-minute")) > 45 and int(i.get_attribute("data-minute")) < 61:
                rc_45_to_60 += 1
            if int(i.get_attribute("data-minute")) <= 45:
                rc_until_45 += 1
            if int(i.get_attribute("data-minute")) > 60:
                rc_60_ft += 1


    if second_formation == 0:
        second_formation = first_formation
    return [goals_total,
            first_formation, second_formation,
            goals_at_hf,
            #goals_at_45_to_60, goals_at_60_ft,
            sub_in_until_45,
            #sub_in_45_to_60, sub_in_60_ft,
            yc_total, yc_until_45,
            #yc_45_to_60, yc_60_ft,
            rc_total, rc_until_45,
            #rc_45_to_60, rc_60_ft
            ]

def parse_live_table(driver):
    MATCH_STAT = Temp_List()

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_raiting_team_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_raiting_team_away).text)

    elem = driver.find_element_by_xpath(xpath_more_shots)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    time.sleep(1)

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
    time.sleep(1)

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_possession_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_possession_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_touches_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_touches_away).text)

    elem = driver.find_element_by_xpath(xpath_more_pass_success)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1.5)

    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corners_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corners_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corner_accuracy_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(xpath_corner_accuracy_away).text)

    elem = driver.find_element_by_xpath(xpath_more_dispossessed)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.double_click(elem)
    action.perform()
    time.sleep(1.5)

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
    time.sleep(1)

    return MATCH_STAT

def parse_chalkboard(driver):
    MATCH_STAT = Temp_List()

    elem = driver.find_element_by_xpath(xpath_to_shots_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1)

    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_successful_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_successful_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_unsuccessful_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(dribbles_unsuccessful_away).text)

    elem = driver.find_element_by_xpath(xpath_to_tackles_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1)

    MATCH_STAT.append(driver.find_element_by_xpath(blocked_shots_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_shots_away).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_crosses_home).text)
    MATCH_STAT.append(driver.find_element_by_xpath(blocked_crosses_away).text)

    elem = driver.find_element_by_xpath(xpath_to_errors_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem)
    action.click()
    action.perform()
    time.sleep(1)

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


    elem = driver.find_elements_by_xpath(xpath_to_strongs_home)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Strong":
            strongs_home.update({str(texts.text).rpartition("\n")[0]:1})
        if str(texts.text).rpartition("\n")[2] == "Very Strong":
            strongs_home.update({str(texts.text).rpartition("\n")[0]:2})
    elem = driver.find_elements_by_xpath(xpath_to_strongs_away)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Strong":
            strongs_away.update({str(texts.text).rpartition("\n")[0]:1})
        if str(texts.text).rpartition("\n")[2] == "Very Strong":
            strongs_away.update({str(texts.text).rpartition("\n")[0]:2})
    elem = driver.find_elements_by_xpath(xpath_to_weakness_home)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Weak":
            weakness_home.update({str(texts.text).rpartition("\n")[0]:1})
        if str(texts.text).rpartition("\n")[2] == "Very Weak":
            weakness_home.update({str(texts.text).rpartition("\n")[0]:2})
    elem = driver.find_elements_by_xpath(xpath_to_weakness_away)
    for texts in elem:
        if str(texts.text).rpartition("\n")[2] == "Weak":
            weakness_away.update({str(texts.text).rpartition("\n")[0]:1})
        if str(texts.text).rpartition("\n")[2] == "Very Weak":
            weakness_away.update({str(texts.text).rpartition("\n")[0]:2})
    elem = driver.find_elements_by_xpath(xpath_to_style_home)
    for texts in elem:
        style_home.append(str(texts.text))
    elem = driver.find_elements_by_xpath(xpath_to_style_away)
    for texts in elem:
        style_away.append(str(texts.text))
    for i in list_strongs:
        MATCH_STAT.append(strongs_home.pop(i, 0))
    for i in list_strongs:
        MATCH_STAT.append(strongs_away.pop(i, 0))
    for i in list_weakness:
        MATCH_STAT.append(weakness_home.pop(i, 0))
    for i in list_weakness:
        MATCH_STAT.append(weakness_away.pop(i, 0))
    for i in list_styles:
        if i in style_home:
            MATCH_STAT.append(1)
        else:
            MATCH_STAT.append(0)
    for i in list_styles:
        if i in style_away:
            MATCH_STAT.append(1)
        else:
            MATCH_STAT.append(0)
    return MATCH_STAT

def parse_whoscored(url, driver):
    MATCH_STAT = []
    SQL_TEMPLATE = []
    driver.get(url)

    driver.execute_script(script_scroll_down, 700)
    time.sleep(2)
    try:
        MATCH_STAT += parse_characteristic(driver)
    except AssertionError:
        print(traceback.format_exc())
        MATCH_STAT += parse_characteristic(driver)
    SQL_TEMPLATE += sql_columns_of_characteristic
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    url = url.replace("Show", "Preview")
    driver.get(url)
    time.sleep(1)

    HOME = driver.find_element_by_css_selector(css_team_home).text
    AWAY = driver.find_element_by_css_selector(css_team_away).text

    driver.execute_script(script_scroll_down, 550)
    time.sleep(1.5)

    try:
        MATCH_STAT += parse_probable_stat(driver)
    except AssertionError:
        print(traceback.format_exc())
        MATCH_STAT += parse_probable_stat(driver)

    SQL_TEMPLATE += sql_columns_of_probable_stat
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    url = url.replace("Preview", "Live")
    driver.get(url)
    time.sleep(2)

    MATCH_STAT.append("'" + url + "'")
    SQL_TEMPLATE += sql_columns_of_url
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    elem = str(driver.find_element_by_css_selector(css_season).text)
    SEASON = "20" + str((elem.strip()[-2:]))
    if str((elem.strip()[-6:-3])) in ("May", "Jan", "Feb", "Mar", "Apr"):
        SEASON = int(SEASON) - 1

    driver.execute_script(script_scroll_down, 1000)
    time.sleep(3)

    home_stat = parse_yc_rc_goals(xpath_to_home_stat, driver)
    away_stat = parse_yc_rc_goals(xpath_to_away_stat, driver)
    if home_stat[0] > away_stat[0]:
        MATCH_STAT.append('1')
    elif home_stat[0] < away_stat[0]:
        MATCH_STAT.append('2')
    elif home_stat[0] == away_stat[0]:
        MATCH_STAT.append('0')
    MATCH_STAT += home_stat
    MATCH_STAT += away_stat


    SQL_TEMPLATE += sql_columns_of_time_stat
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    # 1 to 90
    MATCH_STAT += parse_live_table(driver)
    SQL_TEMPLATE += sql_columns_of_full_time_stat
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    # 1 to 45
    try:
        action = ActionChains(driver)
        elem = driver.find_elements_by_css_selector(css_to_time_scroll)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
        time.sleep(5)
    except MoveTargetOutOfBoundsException:
        driver.execute_script(script_scroll_down, 1300)
        time.sleep(1.5)
        action = ActionChains(driver)
        elem = driver.find_elements_by_css_selector(css_to_time_scroll)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
        time.sleep(5)


    try:
        MATCH_STAT += parse_live_table(driver)
    except AssertionError:
        print(traceback.format_exc())
        MATCH_STAT += parse_live_table(driver)
    SQL_TEMPLATE += sql_columns_of_half_time_stat
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    """
    # 45 to 90
    elem = driver.find_elements_by_css_selector(css_to_time_scroll)
    action = ActionChains(driver)
    action.move_to_element(elem[1])
    action.drag_and_drop_by_offset(elem[1], 497, 0)
    action.move_to_element(elem[0])
    action.drag_and_drop_by_offset(elem[0], 495, 0)
    action.perform()
    time.sleep(5)
    
    parse_live_table(MATCH_STAT, driver)
    # 60 to 90
    elem = driver.find_elements_by_css_selector(css_to_time_scroll)
    action = ActionChains(driver)
    action.move_to_element(elem[0])
    action.drag_and_drop_by_offset(elem[0], 150, 0)
    action.perform()
    time.sleep(5)
    
    parse_live_table(MATCH_STAT, driver)
    """

    try:
        driver.execute_script(script_scroll_down, 600)
        time.sleep(1)

        MATCH_STAT.append("'" + driver.find_element_by_xpath(referee).text.strip() + "'")
        SQL_TEMPLATE += sql_columns_of_referee
        assert len(SQL_TEMPLATE) == len(MATCH_STAT)

        elem = driver.find_element_by_xpath(xpath_to_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem)
        action.click(elem)
        action.perform()
        time.sleep(1)
    except NoSuchElementException:
        print(traceback.format_exc())

        driver.execute_script(script_scroll_down, 800)
        time.sleep(1)

        MATCH_STAT.append("'" + driver.find_element_by_xpath(referee).text.strip() + "'")
        SQL_TEMPLATE += sql_columns_of_referee
        assert len(SQL_TEMPLATE) == len(MATCH_STAT)

        elem = driver.find_element_by_xpath(xpath_to_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem)
        action.click(elem)
        action.perform()
        time.sleep(1)

    # 1 to 90
    try:
        driver.execute_script(script_scroll_down, 1100)
        time.sleep(3)
        MATCH_STAT += parse_chalkboard(driver)
    except AssertionError as ex:
        print(traceback.format_exc())
        MATCH_STAT += parse_chalkboard(driver)
    except NoSuchElementException as ex:
        print(traceback.format_exc())
        driver.execute_script(script_scroll_down, 1300)
        time.sleep(3)
        MATCH_STAT += parse_chalkboard(driver)

    SQL_TEMPLATE += sql_columns_of_full_time_chulkboard
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)


    # 1 to 45
    try:
        elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
        time.sleep(1)
    except MoveTargetOutOfBoundsException:
        print(traceback.format_exc())
        driver.execute_script(script_scroll_down, 1300)
        time.sleep(3)

        elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
        action = ActionChains(driver)
        action.move_to_element(elem[1])
        action.drag_and_drop_by_offset(elem[1], -497, 0)
        action.perform()
        time.sleep(1)
    try:
        MATCH_STAT += parse_chalkboard(driver)
    except:
        print(traceback.format_exc())
        MATCH_STAT += parse_chalkboard(driver)
    SQL_TEMPLATE +=sql_columns_of_half_time_chulkboard
    assert len(SQL_TEMPLATE) == len(MATCH_STAT)

    """
    # 45 to 90
    elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem[1])
    action.drag_and_drop_by_offset(elem[1], 497, 0)
    action.move_to_element(elem[0])
    action.drag_and_drop_by_offset(elem[0], 495, 0)
    action.perform()
    time.sleep(1)
    
    parse_chalkboard(MATCH_STAT, driver)
    
    # 60 to 90
    elem = driver.find_elements_by_css_selector(css_to_time_scroll_chalkboard)
    action = ActionChains(driver)
    action.move_to_element(elem[0])
    action.drag_and_drop_by_offset(elem[0], 150, 0)
    action.perform()
    time.sleep(1)
    
    parse_chalkboard(MATCH_STAT, driver)
    """

    print(MATCH_STAT)

    k = 0
    SQL_string = ""
    for i in MATCH_STAT:
        SQL_string += SQL_TEMPLATE[k] + "=" + str(i) + ", "
        k += 1
    assert len(SQL_string)


    db = pymysql.connect(host=db_host, port=db_port, user=db_usr, passwd=db_passwd, db=db_name)
    cursor = db.cursor()
    assert cursor.execute("SELECT * FROM " + db_name + " WHERE home='" + HOME + "' && away='" + AWAY + "' && season='" + str(SEASON) + "';")
    sql = "UPDATE "+str(db_name)+" SET " + str(SQL_string[:-2]) + " WHERE home='" + HOME + "' && away='" + AWAY + "' && season=" + str(SEASON) +";"
    cursor.execute(sql)
    db.commit()