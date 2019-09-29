# Import the necessary libraries
import requests
import datetime
import re


def calculate_friends():

    # get user id
    user_ids = input("Enter id or username: ")

    # request to vk.com
    url = 'https://api.vk.com/method/users.get'
    payload = dict(v="5.71", access_token="17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711",
                   user_ids=user_ids, fields="bdate")
    my_request = requests.get(url, params=payload).json()

    # get user full name
    user = str(my_request["response"][0]["id"])

    # request to get user's friends
    url_f = 'https://api.vk.com/method/friends.get'
    par_f = dict(v='5.71', access_token='17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711',
                 user_id=user, fields='bdate')

    request_friends = requests.get(url_f, params=par_f)

    # have the friend's items
    friends_items = request_friends.json()["response"]['items']

    # make the list of age
    years_list = []
    for i in friends_items:
        if 'bdate' in i and re.match(r"([\d]+\.[\d]+\.[\d]+)", i['bdate']):
            old = find_year(i['bdate'])
            if old < 80:
                years_list.append(old)

    # make the final list of tuples sorted by age
    final_list = []
    for years in years_list:
        item = years, count_years(years_list, years)
        if item not in final_list:
            final_list.append(item)
    final_list.sort(key=lambda x: x[1])

    print("It's a list with friend's age and quantity:")
    print(final_list)


# function to find the age in friend's items
def find_year(line):
    year = int(datetime.datetime.now().year)
    b_day = int(re.search(r"(\d+){3}", line).group())
    return int(year - b_day)


# function that count the quantity of friend with same age
def count_years(ls, year):
    count = 0
    for n in ls:
        if n == year:
            count += 1
    return count


# call main function to start program
calculate_friends()

