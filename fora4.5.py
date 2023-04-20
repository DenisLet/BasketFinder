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




    def get_average_1q(data1,data2):

        scores = []
        for i in data1:
            scores.append(int(i[2])+int(i[3]))

        for i in data2:
            scores.append(int(i[2])+int(i[3]))

        return mean(scores)


    print('1Q mean::')
    print(get_average_1q(team1_results_home,team2_results_away))

    average_value = get_average_1q(team1_results_home,team2_results_away)

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
    team1_lose1of3_home, team1_lose1of3_away = home_lose_one_of3(team1_results_home), away_lose_one_of3(team1_results_away)

    team2_win1of3_home, team2_win1of3_away = home_win_one_of3(team2_results_home), away_win_one_of3(team2_results_away)
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

    # case_3_home(team1_win1of3_home,team2_lose1of3_away,team1_win1of3_away, team2_lose1of3_home)
    # case_3_away(team2_win1of3_away,team1_lose1of3_home, team2_win1of3_home, team1_lose1of3_away)


    def home_win_one_of3_FORA(scores):
        matches = len(scores)
        handycap = dict()
        for i in range(3,7):

            win = 0
            for data in scores:
                if data[2]-i>data[3] or data[4]-i>data[5] or data[6]-i>data[7]:
                    win+=1
            handycap[f'+{i-1}.5'] =  win
        handycap['len'] = matches
        print(handycap)
        return handycap




    # home_win_one_of3_FORA(team1_results_home)




    def away_win_one_of3_FORA(scores):
        matches = len(scores)
        handycap = dict()
        for i in range(3,7):

            win = 0
            for data in scores:
                if data[3]-i>data[2] or data[5]-i>data[4] or data[7]-i>data[6]:
                    win+=1
            handycap[f'+{i-1}.5'] =  win

        handycap['len'] = matches
        print(handycap)
        return handycap

    # away_win_one_of3_FORA(team1_results_away)



    def home_lose_one_of3_FORA(scores):
        matches = len(scores)
        handycap = dict()
        for i in range(3,7):

            win = 0
            for data in scores:
                if data[3]-i>data[2] or data[5]-i>data[4] or data[7]-i>data[6]:
                    win+=1
            handycap[f'+{i-1}.5'] =  win
        handycap['len'] = matches
        print(handycap)
        return handycap



    def away_lose_one_of3_FORA(scores):
        matches = len(scores)
        handycap = dict()
        for i in range(3,7):
            win = 0
            for data in scores:
                if data[2]-i>data[3] or data[4]-i>data[5] or data[6]-i>data[7]:
                    win+=1
                    print(data)
            print()
            handycap[f'+{i-1}.5'] =  win
        handycap['len'] = matches
        print(handycap)
        return handycap


    t1_case_home = home_win_one_of3_FORA(team1_results_home)
    t1_case_away = away_win_one_of3_FORA(team1_results_away)
    t2_case_home = home_win_one_of3_FORA(team2_results_home)
    t2_case_away = away_win_one_of3_FORA(team2_results_away)


    def prepair_To(data1,data2,data3,data4) -> dict:

        case_dict = dict()


        for key,val in data1.items():
            if key == 'len':
                continue
            if data1['len'] - val <= 2:
                l = data1['len']

                case_dict[f'TEAM1 HOME WIN: {key}'] = f'{val}/{l}'

        for key,val in data2.items():
            if key == 'len':
                continue
            if data2['len'] - val <= 2:
                l = data2['len']

                case_dict[f'TEAM1 AWAY WIN: {key}'] = f'{val}/{l}'

        for key,val in data3.items():
            if key == 'len':
                continue
            if data3['len'] - val <= 2:
                l = data3['len']

                case_dict[f'TEAM2 HOME LOSE: {key}'] = f'{val}/{l}'


        for key,val in data4.items():
            if key == 'len':
                continue
            if data4['len'] - val <= 2:
                l = data4['len']

                case_dict[f'TEAM2 AWAY LOSE: {key}'] = f'{val}/{l}'

        if 'TEAM1' in str(case_dict.keys()):
            if 'TEAM2' in str(case_dict.keys()):
                print(url)
                print(case_dict)

    prepair_To(t1_case_home,t1_case_away,t2_case_home,t2_case_away)


    print()

    # print(team1_results_home)

    def try_it_over(data1,ave):
        dict_results_more1= dict()
        dict_results_less1 = dict()
        print(len(data1),'of matches was checked')
        for val in range(round(ave)-2,round(ave)+2):
            scored = 0
            for i in data1:
                if (int(i[2])+ int(i[3])) > val or (int(i[4])+int(i[5])) > val or (int(i[6])+int(i[7]) > val) and len(data1)>=60:
                    scored += 1
            dict_results_more1[f'{val}'] = round(scored/len(data1),3)*100 if len(data1)!= 0 else None

        for val in range(round(ave)-2,round(ave)+2):
            count = 0
            between = []

            for i in data1:
                if (int(i[2])+ int(i[3])) < val or (int(i[4])+int(i[5])) < val or (int(i[6])+int(i[7]) < val) and len(data1)>=70:
                    count += 1
            dict_results_less1[f'{val}'] = round(count/len(data1),3)*100

        for i,j in dict_results_more1.items():
            if j >= 97:
                print('MORE::',i,j)
                print(url)

        for i,j in dict_results_less1.items():
            if j >= 97:
                print('LESS::',i,j)
                print(url)

    try_it_over(team1_results_home+team1_results_away+team2_results_home+team2_results_away,average_value)



    def try_1_quarter(data1, data2, average):
        long = len(data1)+len(data2)
        values1q = 0
        values2q = 0
        for i in data1:
            q1 = int(i[2]) + int(i[3])
            q2 = int(i[4]) + int(i[5])
            if q1 > average or q2 > average:
                values2q += 1
                if q1 > average:
                    values1q += 1

        for i in data2:
            q1 = int(i[2]) + int(i[3])
            q2 = int(i[4]) + int(i[5])
            if q1 > average or q2 > average:
                values2q += 1
                if q1 > average:
                    values1q += 1

        return round(values1q/long,2)*100, round(values2q/long,2)*100


    def one_low_two_high(data1,data2,average):
        long = len(data1) + len(data2)
        cases1, cases2 = 0, 0

        for i in data1:
            q1 = int(i[2]) + int(i[3])
            q2 = int(i[4]) + int(i[5])
            if q1 < average:
                cases1 += 1
                if q2 > average:
                    cases2 += 1

        for i in data2:
            q1 = int(i[2]) + int(i[3])
            q2 = int(i[4]) + int(i[5])
            if q1 < average :
                cases1 += 1
                if q2 > average:
                    cases2 += 1
        return round(cases2/cases1,2)*100 , cases1


    checker1_2 = try_1_quarter(team1_results_home+team1_results_away,team2_results_away+team2_results_home, average_value)
    checker2 = one_low_two_high(team1_results_home+team1_results_away,team2_results_away+team2_results_home, average_value)
    if checker1_2[0] > 50:
        if checker1_2[1] > 75:
            if checker2[0] > 55:
                print('DATA:::')
                print(checker1_2)
                print(checker2)
                print('2 quarter MORE MORE MORE MORE MORE',average_value)
                print(url)

    if checker1_2[0] < 40:
        if checker1_2[1] > 60:
            if checker2[0] < 40:
                print('DATA:::')
                print(checker1_2)
                print(checker2)
                print('2 quarter LESS LESS LESS LESS LESS',average_value)
                print(url)

    # print("1 quarter ---- 2 quarter  more then ave///")
    # print(try_1_quarter(team1_results_home+team1_results_away,team2_results_away+team2_results_home, average_value))
    # print('One low Two high///')
    # print(one_low_two_high(team1_results_home+team1_results_away,team2_results_away+team2_results_home, average_value))






for i in schedule:
    try:
        main(i)
    except:
        continue