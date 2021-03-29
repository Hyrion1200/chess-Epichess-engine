import os
import sys
import dotenv
import logging
import lichessGame
import berserk
import argparse
import time


class Lichess_Bot:
    """ Instance of the bot connected to the lichess API """

    def __init__(self, TOKEN):
        if TOKEN in (None, ""):
            raise Exception('Token is empty!')
        try:
            session = berserk.TokenSession(TOKEN)
        except Exception as e:
            print(f'Could not create session: {e}')
            sys.exit(-1)
        try:
            self.client = berserk.Client(session=session)
        except Exception as e:
            print(f'Could not create client: {e}')
            sys.exit(-1)
        self.profile = self.client.account.get()
        print(f'Logged in as {self.profile["username"]}')

    def start(self):
        print("started")

    def __handle_events(self):
        while True:
            try:
                for event in self.client.bots.stream_incoming_events():
                    if event['type'] == 'gameStart':
                        game = lichessGame.LichessGame(
                            self.client, event['game']['id'])
                        game.start()
                    elif event['type'] == 'challenge':
                        self.__handle_challenge(event)
                    elif event['type'] == 'gameFinish':
                        logging.debug(f'Game ended: {event}')
            except berserk.exceptions.ResponseError as e:
                logging.error('Invalid server response: {e}')
                if 'Too Many Requests for url' in str(e):
                    time.sleep(10)

    def __handle_challenge(self, event):
        if event['timeControl']['type'] != 'clock':
            timeControl = event['timeControl']['type']
        else:
            timeControl = event['timeControl']['show']
        logging.info(f'Recieved challenge. ID: {event["id"]}, Challenger: {event["challenger"]["id"]},',
                     f'Game type: {event["variant"]["name"]}, Rated: {event["rated"]}, Time: {timeControl}.')
        try:
            if (event['challenge']['rated']):
                self.client.bots.decline_challenge(event['id'])
            else:
                self.client.bots.accept_challenge(event['id'])
        except berserk.exceptions.ResponseError as e:
            print(f'ERROR: Invalid server response: {e}')
            logging.info('Invalid server response: {e}')
            if 'Too Many Requests for url' in str(e):
                time.sleep(10)


if __name__ == "__main__":
    dotenv.load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        print('TOKEN empty, please create .env file with TOKEN="botToken" or if in Docker, use run -e TOKEN="botToken".')
        quit()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity and show board for each move", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    bot = Lichess_Bot(TOKEN)
    bot.start()
