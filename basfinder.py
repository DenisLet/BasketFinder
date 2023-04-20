from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from functools import reduce
from statistics import mean

def creation():
    try:
        url = "https://www.basketball24.com"
        browser = webdriver.Chrome()
        browser.get(url)
        resume = input("Select matches and press enter to continue(Add to favorite) ")
        browser.implicitly_wait(1)
        matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_3']")
        checklist = list()
        for i in matches:
            link = i.get_attribute("id")
            urls = f"https://www.basketball24.com/match/{link[4:]}"
            checklist.append(urls)
    finally:
        browser.quit()
    return checklist

schedule = creation()

def main(url):

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps,options=options)
    browser.get(url)
    browser.implicitly_wait(1)
    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
            "href") + "results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
            "href") + "results/"
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text

    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            # print(line)
            if "(" in line or "Awrd" in line or "Abn" in line:
                continue
            if len([i for i in line.split() if i.isdigit()]) < 6:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser,link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_3']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches,team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)

    team1_name = games[2].split()
    team2_name = games[3].split()

    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        print(team_)
        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches

    team1_home, team1_away = separation_home_away(team1_name, games[0])
    team2_home, team2_away = separation_home_away(team2_name, games[1])



    def get_scores(results):
        scorelines = []
        for match in results:
            if len([ i for i in match if i.isdigit() ]) < 10:
                continue
            if "AOT" in match:
                scoreline = match[-13:-1]
            else:
                scoreline = match[-11:-1]
            scorelines.append(list(map(int,scoreline)))
        return scorelines

    team1_results_home = get_scores(team1_home)
    team1_results_away = get_scores(team1_away)
    team2_results_home = get_scores(team2_home)
    team2_results_away = get_scores(team2_away)

    def win1q(data,loc):
        win, matches = 0, len(data)

        for scores in data:
            if loc == 'home':
                if scores[2]>scores[3]:
                    win += 1
            if loc == "away":
                if scores[3]>scores[2]:
                    win += 1

        return win, matches

    def win2q(data,loc):
        win, matches = 0, len(data)

        for scores in data:
            if loc == 'home':
                if scores[4]>scores[5]:
                    win += 1
            if loc == "away":
                if scores[5]>scores[4]:
                    win += 1

        return win, matches

    def win3q(data,loc):
        win, matches = 0, len(data)

        for scores in data:
            if loc == 'home':
                if scores[6]>scores[7]:
                    win += 1
            if loc == "away":
                if scores[7]>scores[6]:
                    win += 1

        return win, matches

    def win4q(data,loc):
        win, matches = 0, len(data)

        for scores in data:
            if loc == 'home':
                if scores[8]>scores[9]:
                    win += 1
            if loc == "away":
                if scores[9]>scores[8]:
                    win += 1

        return win, matches

    team1_win1q_home, team1_win1q_away = win1q(team1_results_home, loc='home'), win1q(team1_results_away, loc='away')
    team1_win2q_home, team1_win2q_away = win2q(team1_results_home, loc='home'), win1q(team1_results_away, loc='away')
    team1_win3q_home, team1_win3q_away = win3q(team1_results_home, loc='home'), win1q(team1_results_away, loc='away')
    team1_win4q_home, team1_win4q_away = win4q(team1_results_home, loc='home'), win1q(team1_results_away, loc='away')

    team2_win1q_home, team2_win1q_away = win1q(team2_results_home, loc='home'), win1q(team2_results_away, loc='away')
    team2_win2q_home, team2_win2q_away = win2q(team2_results_home, loc='home'), win1q(team2_results_away, loc='away')
    team2_win3q_home, team2_win3q_away = win3q(team2_results_home, loc='home'), win1q(team2_results_away, loc='away')
    team2_win4q_home, team2_win4q_away = win4q(team2_results_home, loc='home'), win1q(team2_results_away, loc='away')


    def condition_home(data1,data2):
        if data1[0]/data1[1] > 0.65 and data1[1]>=18:
            if data2[0]/data2[1] <0.37 and data2[1]>=18:
                print(url)
                print("1 QWT WIN HOME TEAM")
                print(data1,data2)


    def condition_away(data1, data2):
        if data2[0]/data2[1] > 0.65 and data2[1]>=18:
            if data1[0]/data1[1] <0.37 and data1[1]>=18:
                print(url)
                print("1 QWT WIN AWAY TEAM")
                print(data1,data2)


    def home_win_one_of3(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[2]>data[3] or data[4]>data[5] or data[6]>data[7]:
                win+=1
        return win, matches


    def away_win_one_of3(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[3]>data[2] or data[5]>data[4] or data[7]>data[6]:
                win+=1
        return win, matches


    def home_win_all3(data):
        win, matches = 0, len(data)

        for match in data:
            if match[2]>match[3] and match[4] > match[5] and match[6] > match[7]:
                win += 1

        return win, matches


    def away_win_all3(data):
        win, matches = 0, len(data)

        for match in data:
            if match[3] > match[2] and match[5] > match[4] and match[7] > match[6]:
                win += 1

        return win, matches


    def home_lose_one_of3(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[2]<scores[3] or scores[4]<scores[5] or scores[6]<scores[7]:
                lose += 1
        return lose, matches


    def away_lose_one_of3(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[3] < scores[2] or scores[5] < scores[4] or scores[7] < scores[6]:
                lose += 1
        return lose, matches


    team1_win1of3_home, team1_win1of3_away = home_win_one_of3(team1_results_home), away_win_one_of3(team1_results_away)
    team1_win3of3_home, team1_win3of3_away = home_win_all3(team1_results_home), away_win_all3(team1_results_away)
    team1_lose1of3_home, team1_lose1of3_away = home_lose_one_of3(team1_results_home), away_lose_one_of3(team1_results_away)

    team2_win1of3_home, team2_win1of3_away = home_win_one_of3(team2_results_home), away_win_one_of3(team2_results_away)
    team2_win3of3_home, team2_win3of3_away = home_win_all3(team2_results_home), away_win_all3(team2_results_away)
    team2_lose1of3_home, team2_lose1of3_away = home_lose_one_of3(team2_results_home), away_lose_one_of3(team2_results_away)


    def case_3_home(data1,data2,data3,data4):
        if data1[1] - data1[0]<2 and data1[1]>18:
            if data2[1] - data2[0] < 2 and data2[1]>=15:
                print(url)
                print("TEAM1 WIN ONE OF FIRST 3 QWTS... NORNAL")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)

    def case_3_away(data1,data2,data3,data4):
        if data1[1] - data1[0]<2 and data1[1]>18:
            if data2[1] - data2[0] < 2 and data2[1]>=15:
                print(url)
                print("TEAM2 WIN ONE OF FIRST 3 QWTS...NORNAL")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)


    # def case_with_lose_3_home(data1,data2):
    #     if data1[1] - data1[0]<2 and data1[1]>18:
    #         if data2[1] - data2[0]<1 and data2[1]>15:
    #             print(url)
    #             print("TEAM1 WIN ONE OF 3 QWTS (INCLUDING LOSES OPPONENTS)")
    #             print(data1,data2)
    #
    # def case_with_lose_3_away(data1,data2):
    #     if data1[1] - data1[0]<2 and data1[1]>18: # team win one of 3
    #         if data2[1] - data2[0]<1 and data2[1]>15: # team lose one of 3
    #             print(url)
    #             print("TEAM2 WIN ONE OF 3 QWTS (INCLUDING LOSES OPPONENTS)")
    #             print(data1,data2)


    def home_second_if_lose_first(data):
        win, matches = 0, 0

        for scores in data:
            if scores[2]<scores[3]:
                matches += 1
                if scores[4]>scores[5]:
                    win += 1
        return win, matches

    def away_second_if_lose_first(data):
        win, matches = 0, 0

        for scores in data:
            if scores[3] < scores[2]:
                matches += 1
                if scores[5] > scores[4]:
                    win += 1
        return win, matches


    def home_second_if_win_first(data):
        lose, matches = 0, 0

        for scores in data:
            if scores[2] > scores[3]:
                matches += 1
                if scores[4] < scores[5]:
                    lose += 1
        return lose, matches


    def away_second_if_win_first(data):
        lose, matches = 0, 0

        for scores in data:
            if scores[3] > scores[2]:
                matches += 1
                if scores[5] < scores[4]:
                    lose += 1
        return lose, matches


    team1_win2_after_lose1_home = home_second_if_lose_first(team1_results_home)
    team1_win2_after_lose1_away = away_second_if_lose_first(team1_results_away)
    team1_lose2_after_win1_home = home_second_if_win_first(team1_results_home)
    team1_lose2_after_win1_away = away_second_if_win_first(team1_results_away)

    team2_win2_after_lose1_home = home_second_if_lose_first(team2_results_home)
    team2_win2_after_lose1_away = away_second_if_lose_first(team2_results_away)
    team2_lose2_after_win1_home = home_second_if_win_first(team2_results_home)
    team2_lose2_after_win1_away = away_second_if_win_first(team2_results_away)


    def case_home_win_2_after_lose_1(data1,data2):
        if data1[0]/data1[1] > 0.75 and data1[1]>5:
            if data2[0]/data2[1] > 0.75 and data2[1]>5:
                print(url)
                print("TEAM1 WILL WIN 2 QWT")

    def case_away_win_2_after_lose_1(data1,data2):
        if data1[0]/data1[1] > 0.75 and data1[1]>5:
            if data2[0]/data2[1] > 0.75 and data2[1]>5:
                print(url)
                print("TEAM2 WILL WIN 2 QWT")



    # print("AFTER 1Q WIN SECOND AT HOME ",team1_win2_after_lose1_home)
    # print("LOSE AFTER WIN 1Q           ", team2_lose2_after_win1_away)


    case_home_win_2_after_lose_1(team1_win2_after_lose1_home,team2_lose2_after_win1_away)
    case_away_win_2_after_lose_1(team2_win2_after_lose1_away,team1_lose2_after_win1_home)

    # case_with_lose_3_home(team1_win1of3_home, team2_lose1of3_away)
    # case_with_lose_3_away(team2_win1of3_away, team1_lose1of3_home)

    case_3_home(team1_win1of3_home,team2_lose1of3_away,team1_win1of3_away, team2_lose1of3_home)
    case_3_away(team2_win1of3_away,team1_lose1of3_home, team2_win1of3_home, team1_lose1of3_away)

    print('TEAM1 Whome/Waway, TEAM2 Lhome/Laway ',team1_win1of3_home,team1_win1of3_away, team2_lose1of3_home,team2_lose1of3_away )

    condition_home(team1_win1q_home, team2_win1q_away)
    condition_away(team1_win1q_home, team2_win1q_away)

    # print(team1_win1of3_home, team2_lose1of3_away)
    # print(team2_win1of3_away, team1_lose1of3_home)

    # print(team1_win1of3_home,team2_win3of3_away)
    # print(team2_win1of3_away,team1_win3of3_home)
    #

    def home_lose1_win23(data):
        win = 0
        count = 0

        for match in data:
            if match[2] <= match[3]:
                count += 1
                if match[4] > match[5] or match[6] > match[7]:
                    win += 1

        return  win, count

    def away_lose1_win23(data):
        win = 0
        count = 0

        for match in data:
            if match[3] <= match[2]:
                count += 1
                if match[5] > match[4] or match[7] > match[6]:
                    win += 1

        return win, count

    def home_win1_lose23(data):
        lose = 0
        count = 0

        for match in data:
            if match[2] >= match[3]:
                count += 1
                if match[4] < match[5] or match[6] < match[7]:
                    lose += 1


        return  lose, count

    def away_win1_lose23(data):
        lose = 0
        count = 0

        for match in data:
            if match[3] >= match[2]:
                count += 1
                if match[5] < match[4] or match[7] < match[6]:
                    lose += 1

        return lose, count


    team1_win23_home = home_lose1_win23(team1_results_home)
    team1_win23_away = away_lose1_win23(team1_results_away)
    team2_win23_home = home_lose1_win23(team2_results_home)
    team2_win23_away = away_lose1_win23(team2_results_away)

    team1_lose23_home = home_win1_lose23(team1_results_home)
    team1_lose23_away = away_win1_lose23(team1_results_away)
    team2_lose23_home = home_win1_lose23(team2_results_home)
    team2_lose23_away = away_win1_lose23(team2_results_away)



    def case_win23_home(data1,data2):
        print('-'*30)
        print(f'{data1}:{data2}')
        print('-' * 30)
        if data1[1] > 7 and data2[1]> 7:
            if data1[1] - data1[0] < 2:
                if data2[1] - data2[0] < 2:
                    print(url)
                    print(f'TEAM1 WILL WIN 2-3 QUARTERS NEXT    ')

    def case_win23_away(data1,data2):
        print('-' * 30)
        print(f'{data1}:{data2}')
        print('-' * 30)
        if data1[1] > 7 and data2[1]> 7:
            if data1[1] - data1[0] < 2:
                if data2[1] - data2[0] < 2:
                    print(url)
                    print(f'TEAM2 WILL WIN 2-3 QUARTERS NEXT    ')

    # case_win23_home(team1_win23_home, team2_lose23_away)
    # case_win23_away(team2_win23_away, team1_lose23_home)


    def home_win_one_of4(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[2]>data[3]+2 or data[4]>data[5]+2 or data[6]>data[7]+2 or data[8]>data[9]+2:
                win+=1
        return win, matches


    def away_win_one_of4(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[3]>data[2]+2 or data[5]>data[4]+2 or data[7]>data[6]+2 or data[9]>data[8]+2:

                win+=1
        return win, matches

    def home_lose_one_of4(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[2]+2<scores[3] or scores[4]+2<scores[5] or scores[6]+2<scores[7] or scores[8]+2<scores[9]:
                lose += 1
        return lose, matches


    def away_lose_one_of4(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[3]+2 < scores[2] or scores[5]+2 < scores[4] or scores[7]+2 < scores[6] or scores[9]+2 < scores[8]:
                lose += 1
        return lose, matches

    team1_win1of4_home, team1_win1of4_away = home_win_one_of4(team1_results_home), away_win_one_of4(team1_results_away)
    team1_lose1of4_home, team1_lose1of4_away = home_lose_one_of4(team1_results_home), away_lose_one_of4(team1_results_away)

    team2_win1of4_home, team2_win1of4_away = home_win_one_of4(team2_results_home), away_win_one_of4(team2_results_away)
    team2_lose1of4_home, team2_lose1of4_away = home_lose_one_of4(team2_results_home), away_lose_one_of4(team2_results_away)


    def case_4_home(data1,data2,data3,data4):
        if data1[1] - data1[0]<2 and data1[1]>18:
            if data2[1] - data2[0]<2 and data2[1]>=15:
                print(url)
                print("TEAM1 WIN ONE OF 4 QWTS...With handicap")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)

    def case_4_away(data1,data2,data3,data4):
        if data1[1] - data1[0]<2 and data1[1]>18:
            if data2[1] - data[2]<2 and data2[1]>=15:
                print(url)
                print("TEAM2 WIN ONE OF 4 QWTS...With handicap")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)


    case_4_home(team1_win1of4_home,team2_lose1of4_away, team1_win1of4_away, team2_lose1of4_home)
    case_4_away(team2_win1of4_away, team1_lose1of4_home, team2_win1of4_home, team1_lose1of4_away)
    print()
    print(team1_win1of4_home,team2_lose1of4_away, team1_win1of4_away, team2_lose1of4_home)
    print(team2_win1of4_away,team1_lose1of4_home, team2_win1of4_home, team1_lose1of4_away)
    print()

    def home_win_one_of2(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[2] > data[3] or data[4] > data[5]:
                win += 1
        return win, matches

    def away_win_one_of2(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[3] > data[2] or data[5] > data[4]:
                win += 1
        return win, matches


    def home_lose_one_of2(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[2]<scores[3] or scores[4]<scores[5]:
                lose += 1
        return lose, matches


    def away_lose_one_of2(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[3] < scores[2] or scores[5] < scores[4]:
                lose += 1
        return lose, matches



    team1_win1of2_home, team1_win1of2_away = home_win_one_of2(team1_results_home), away_win_one_of2(team1_results_away)
    team2_lose1of2_home, team2_lose1of2_away = home_lose_one_of2(team2_results_home), away_lose_one_of2(team2_results_away)




    print('*'*50)
    print()
    print(team1_win1of2_home, team1_win1of2_away)
    print(team2_lose1of2_home, team2_lose1of2_away)
    print(url)
    print('*'*50)



for i in schedule:
    try:
        main(i)
    except:
        continue