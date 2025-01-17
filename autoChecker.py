import argparse
import re
import time

import requests
import random
from bs4 import BeautifulSoup
from twilio.rest import Client



def main():
    args = parseArgs()
    url = constructUrl(args)

    while True:
        seats = startChecking(url)
        if (seats > 0):
            break

def parseArgs():
    parser = argparse.ArgumentParser("ubc course checker")
    parser.add_argument("course", help="ex:CPSC210", type=str)
    parser.add_argument("section", help="ex:101", type=str)
    parser.add_argument("-num", help="if you want to be texted when course is available", type=str)
    args = parser.parse_args()

    return args


def constructUrl(args):
    dept = args.course[:int(re.search("\d", args.course).start())]
    id = args.course[int(re.search("\d", args.course).start()):]
    section = args.section

    return "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=" + dept + "&course=" + id + "&section=" + section


def startChecking(url):
    print("checking")
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        tables = soup.find_all('table', class_="'table")  # single quote in 'table
        seats = tables[0].select("td strong")
        seatNum = seats[0].get_text()
        print("seat number:", seatNum)
    except Exception as e:
        print("error::", e)
        raise

    if int(seatNum) > 0:
        print("seat available! It has " + seatNum + " seats.")
        account_sid = "ACa46aa4ea5147d47ee80418541319a289"
        auth_token = "f4b40a7eeb7ea5b6b54103b5babcc54c"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+8613862252454",
            from_="+12058595106",
            body = ("your course is available with " + seatNum + " seats left, register at " + url)
            )
        return int(seatNum)
    else:
        rand_delay = random.randint(33, 60)
        print ("Putting program to sleep for " + str(rand_delay) + " seconds.")
        time.sleep(rand_delay)  # does not account for function execution time
        seats = 0
        return seats

if __name__ == "__main__":
    main()