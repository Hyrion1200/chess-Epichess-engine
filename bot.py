# import for .env variables
import os, json, requests
from dotenv import load_dotenv
import game as Game

APIURL = "https://lichess.org/api/"

class Lichess_Bot:
    """ Instance of the bot connected to the lichess API """


    
    def __init__(self, TOKEN):
        if TOKEN in (None, ""):
            raise Exception('Token is empty!')
        self.s = requests.Session()
        self.s.headers.update({ 'Authorization': f'Bearer {TOKEN}'})
        self.user = self.s.get(APIURL+'account').json()
        self.ongoingGames = dict()



    def start(self):
        # set the headers of the session.
        # get the stream of event that the bot is receiving.
        self.__bot_events()

    def __bot_events(self):
        """ Handle all events related to the bot only """
        response = self.s.get(APIURL+'stream/event', stream=True)
        
        # response = s.get(APIURL+'users/status', params={ 'ids': "gyroskan,hyrionChessBot,AleexSaan,Hyrion"})
        # Print and check the request
        # print("url: ", response.url)
        # print("sent headers: ", response.request.headers)
        # print("code:", response.status_code)
        if response.status_code != 200:
            print("error retrieving stream event:", response.reason)
            print("response:", response.text)
        else:
            print('Valid response')
            # iter through the events, comming in real time (infinite loop if response.close is not called)
            for line in response.iter_lines():
                if line:
                    event = json.loads(line.decode('utf8'))
                    print(event)
                    if event['type'] == 'gameStart':
                        self.__game_start(event['game']['id'])
                    elif event['type'] == 'challenge':
                        self.__handle_challenge(event['challenge'])

        self.s.close()


    def __game_start(self, gameID):
        rep = self.s.get(APIURL+'bot/game/stream/'+gameID, stream=True)
        if rep.status_code != 200:
            print('Game stream couldn\'t be reived. Error code:', rep.status_code, 'Error message:', rep.reason)
        else:
            print('Game {', gameID, '} stream has been received!')
        # iter through the events of the game
        current = None
        for line in rep.iter_lines():
            if line:
                event = json.loads(line)
                print(event)
                if event['type'] == 'chatLine':
                    if False and event['room'] == 'player' and event['username'] != self.user['username']:
                        self.__send_message(gameID, 'player', 'Hey '+event['username']+', don\'t you think you should resign?')
                elif event['type'] == 'gameFull':
                    if event['state']['status'] == 'started':
                        self.__create_game(event)
                elif event['type'] == 'gameState':
                    # number of moves even ==> white turn else black turn
                    if event['status'] == 'started':
                        moves = event['moves'].split(' ')
                        if self.ongoingGames[gameID].lastmove == moves[-1]:
                            # Handle Draw events
                            # TODO
                            print('TODO Draw events')
                        else:
                            current.make_move(moves[-1])
                            botMove = current.get_move()
                            if not self.__send_move(gameID, botMove):
                                print('invalid move, need to redo code!')
                    elif event['status'] == 'resign':
                        if event['winner'] == self:
                            self.__send_message(gameID, 'player', 'GG EZ')
                        else:
                            self.__send_message(gameID, 'player', 'GG WP')

    def __create_game(self, event):
        """ Create a chessGame from the event given """
        game = Game.ChessGame(event['id'], event)
        self.ongoingGames[event['id']] = game
        game.isWhite = event['white']['id'] == self.user['id']
        moves = event['state']['moves'].split(' ')
        for move in moves:
            game.make_move(move)
            game.turn += 1
        game.lastmove = moves[-1]
        return game

    def __send_message(self, gameID, chan, msg):
        """ 
        Send a message to the room 'chan' with content 'msg'
        """
        rep = self.s.post(APIURL+'bot/game/'+gameID+'/chat', data={ 'room': chan, 'text': msg })
        if rep.status_code != 200:
            print('send_messages requests not ok, code: ', rep.status_code, '\nerror: ', rep.reason, '\nreason: ', rep.text)
        rep.close()


    def __send_move(self, gameID, move, draw=False):
        with self.s.post(APIURL+'bot/game/'+gameID+'/move/'+move, data={ 'offeringDraw': draw }) as rep:
            if rep.status_code != 200 :
                print('send_move requests not ok, code: ', rep.status_code, '\nerror: ', rep.reason, '\nreason: ', rep.text)
                return False
            return True

    #region Challenges

    def __handle_challenge(self, challenge):
        
        timeControl = challenge['timeControl']['type'] if challenge['timeControl']['type'] != 'clock' else challenge['timeControl']['show']
        print('Recieved challenge. id:', challenge['id'], 'Challenger:', challenge['challenger']['id'], 'Game type:', challenge['variant']['name'], 'Rated:', challenge['rated'], 'Time', timeControl)
        if (challenge['rated']):
            self.__reject_challenge(challenge['id'])
        else:
            self.__accept_challenge(challenge['id'])


    def __accept_challenge(self, challengeID):
        """ Send an request to accept the challenge and log usefull data. """

        rep = self.s.request('POST', APIURL+'challenge/'+challengeID+'/accept')
        if (rep.status_code != 200):
            print('Challenge couldn\'t be accepted. Error code:', rep.status_code, 'Error message:', json.loads(rep.content)['error'])
        else:
            print('Challenge accepted.\n')
        rep.close()

    def __reject_challenge(self, challengeID):
        """ Send an request to reject the challenge and log usefull data. """

        rep = self.s.request('POST', APIURL+'challenge/'+challengeID+'/reject')
        if (rep.status_code != 200):
            print('Challenge couldn\'t be rejected. Error code:', rep.status_code, 'Error message:', rep.json()['error'])
        else:
            print('Challenge rejected.\n')
        rep.close()

    #endregion

if __name__=="__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        print('TOKEN empty, please create .env file with TOKEN="botToken".')
        quit()
    bot = Lichess_Bot(TOKEN)
    bot.start()

#region lychess api
""" Lychess lib api
# import for command lines arguments
import sys, getopt

# Lichess api library
import berserk

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

# try:
#     opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
# except getopt.GetoptError:
#     print 'test.py -i <inputfile> -o <outputfile>'
#     sys.exit(2)
if sys.argv[1] == '-u':
    client.account.upgrade_to_bot()
"""
#endregion