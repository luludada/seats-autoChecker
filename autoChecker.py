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

    notifyUser(args)


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
    except Exception as e:
        print("error::", e)
        raise

    if int(seatNum) > 0:
        print("seat available! It has " + seatNum + " seats.")
        account_sid = "AC9f9b849bc649d570b8afe992b4a9c2ae"
        auth_token = "976e4ee394ad3aabe976a146ff6d21a0"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="17787239821",
            from_="+13024166955",
            body = ("your course is available with " + seatNum + " seats left, register at " + url)
            )
        return seatNum
    else:
        print("no seat")
        rand_delay = random.randint(33, 60)
        print ("Putting program to sleep for " + str(rand_delay) + " seconds.")
        time.sleep(rand_delay)  # does not account for function execution time



if __name__ == "__main__":
    main()
