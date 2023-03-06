import os
import bs4
import requests
from twilio.rest import Client
import time
from dotenv import load_dotenv

load_dotenv()

# Twilio account information
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
TO_NUMBER = os.environ.get("TO_NUMBER")

URL1 = 'https://proticketing.com/lionssports/en_US/tickets'
URL2 = 'https://www.fanzone.pro'


def send_message(url, error=False):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if error:
        client.messages.create(
            body="Error has occured",
            from_=TWILIO_NUMBER,
            to=TO_NUMBER
        )
    else:
        client.messages.create(
            body=f'Website has been updated !\n'
                 f'{url}',
            from_=TWILIO_NUMBER,
            to=TO_NUMBER
        )


def main():
    data = {}
    prev_data = None

    # Main loop
    print('Ticket checker starting!')
    while True:
        try:
            print("new loop")
            # Retrieve the website content
            headers = {'User-Agent': 'Mozilla/5.0'}
            response1 = requests.get(URL1, headers=headers)
            soup1 = bs4.BeautifulSoup(response1.content, 'html.parser')
            response2 = requests.get(URL2, headers=headers)
            soup2 = bs4.BeautifulSoup(response1.content, 'html.parser')
            print(response1.status_code, response2.status_code)
            if response1.status_code != 200 or response2.status_code != 200:
                send_message(url=None, error=True)

            # Extract the relevant data
            data[1] = str(soup1)
            data[2] = str(soup2)

            # Compare to previous data
            if prev_data is not None and data.values() != prev_data.values():
                if data[1] != prev_data[1]:
                    send_message(URL1)
                    print(f'\n{time.strftime("%Y-%m-%d %H:%M:%S")} - Website 1 updated - message sent!\n')
                if data[2] != prev_data[2]:
                    send_message(URL2)
                    print(f'\n{time.strftime("%Y-%m-%d %H:%M:%S")} - Website 2 updated - message sent!\n')

            prev_data = data.copy()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
