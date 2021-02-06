# import for .env variables
import os, json, requests, dotenv
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
        self.__bot_events()

    def __bot_events(self):
        """ Handle all events related to the bot only """
        rep = self.s.get(APIURL+'stream/event', stream=True)
        if rep.status_code != 200:
            print(f'error retrieving stream event: {rep.reason}, response: {rep.text}')
        else:
            print('Valid response')
            # iter through the events, comming in real time (infinite loop if response.close is not called)
            for line in rep.iter_lines():
                if line:
                    event = json.loads(line.decode('utf8'))
                    # print(event)
                    if event['type'] == 'gameStart':
                        self.__game_start(event['game']['id'])
                    elif event['type'] == 'challenge':
                        self.__handle_challenge(event['challenge'])
                    elif event['type'] == 'gameFinish':
                        self.__handle_endofgame(event['game']['id'])
        # close connection when bot stream end
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
                    if False and event['room'] == 'player' and event['username'] not in (self.user['username'], 'lichess'):
                        self.__send_message(gameID, 'player', 'Hey '+event['username']+', don\'t you think you should resign?')
                elif event['type'] == 'gameFull':
                    if event['state']['status'] == 'started':
                        current = self.__create_game(event)
                elif event['type'] == 'gameState':
                    # number of moves even ==> white turn else black turn
                    if event['status'] == 'started':
                        moves = event['moves'].split(' ')
                        if self.ongoingGames[gameID].lastmove == moves[-1]:
                            self.__handle_draw(gameID, event['wdraw'], event['bdraw'])
                        else:
                            current.make_move(moves[-1])
                            current.lastmove = moves[-1]
                            if current.turn % 2 == current.siWhite:
                                botMove = current.get_move()
                                if not self.__send_move(gameID, botMove):
                                    self.__send_resign(gameID)
                                    self.__send_message(gameID, "player", 'I wasn\'t able to do anythin on this, well played!')
                                    print('invalid move, *resigning*, need to redo code!')
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
            if move != '':
                game.make_move(move)
        game.lastmove = moves[-1]
        return game

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

    def __handle_challenge(self, challenge):
        """ accept or reject a challenge depending of its settings and log main infos of the challenge """
        timeControl = challenge['timeControl']['type'] if challenge['timeControl']['type'] != 'clock' else challenge['timeControl']['show']
        print(f'Recieved challenge. ID: {challenge["id"]}, Challenger: {challenge["challenger"]["id"]}, Game type: {challenge["variant"]["name"]}, Rated: {challenge["rated"]}, Time: {timeControl}.')
        if (challenge['rated']):
            self.__reject_challenge(challenge['id'])
        else:
            self.__accept_challenge(challenge['id'])

    def __send_draw(self, gameID):
        rep = self.s.post(f'{APIURL}bot/game/{gameID}/move/', data={ 'offeringDraw': True})
        if rep.status_code != 200:
            print(f'send_draw request not ok, code: {rep.status_code}, reason: {rep.text}')
        rep.close()

    def __handle_draw(self, gameID, wdraw, bdraw):
        current = self.ongoingGames[gameID]
        if (bdraw and current.isWhite or wdraw and not current.isWhite) and current. current.accept_draw():
            self.__send_draw(gameID)

    def __send_move(self, gameID, move, draw=False):
        """ Send a move to make for the game with gameID, if offeringDraw, draw=True """
        with self.s.post(APIURL+'bot/game/'+gameID+'/move/'+move, data={ 'offeringDraw': draw }) as rep:
            if rep.status_code != 200 :
                print(f'send_move requests not ok, code: {rep.status_code}, error: {rep.reason}, \nreason: {rep.text}')
                return False
            return True

    def __send_message(self, gameID, chan, msg):
        """ 
        Send a message to the room 'chan' with content 'msg'
        """
        rep = self.s.post(APIURL+'bot/game/'+gameID+'/chat', data={ 'room': chan, 'text': msg })
        if rep.status_code != 200:
            print(f'send_messages requests not ok, code: {rep.status_code}, error: {rep.reason}, \nreason: {rep.text}')
        rep.close()

    def __send_resign(self, gameID):
        """ Send a resign request fro the game with gameID """
        rep = self.s.post(f'{APIURL}bot/game/{gameID}/resign')
        if rep.status_code != 200:
            print(f'send_resign request not ok, code: {rep.status_code}\nerror: {rep.text}')
        rep.close()

    def __handle_endofgame(self, gameID):
        del self.ongoingGames[gameID]
        # add anything to do after receiving end of game event

if __name__=="__main__":
    dotenv.load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        print('TOKEN empty, please create .env file with TOKEN="botToken".')
        quit()
    bot = Lichess_Bot(TOKEN)
    bot.start()