# import for .env variables
import os, json, requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print('TOKEN empty, please create .env file with TOKEN="botToken".')
    quit()

APIURL = "https://lichess.org/api/"

with requests.Session() as s:
    # set the headers of the session.
    s.headers.update({ 'Authorization': f'Bearer {TOKEN}'})
    # get the stream of event that the bot is receiving.
    response = s.get(APIURL+'stream/event', stream=True)
    
    # response = s.get(APIURL+'users/status', params={ 'ids': "gyroskan,hyrionChessBot,AleexSaan,Hyrion"})
    # Print and check the request
    print("url: ", response.url)
    print("sent headers: ", response.request.headers)
    # print("headers:", response.headers)
    print("code:", response.status_code)
    if response.status_code != requests.codes.ok:
        print("error retrieving stream event: ", response.reason)
        print("response: ", response.text)
    else:
        # print(response.content)
        print('Valid response')
        # iter through the events, comming in real time (infinite loop if response.close is not called)
        for line in response.iter_lines():
            if line:
                event = json.loads(line.decode('utf8'))
                print(event['type'])


def game_start(gameID):
    resp = s.get(APIURL+'bot/game/stream/'+gameID)
    # iter through the events of the game
    for line in response.iter_lines:
        if line:
            event = json.loads(line)
            if event['type'] == 'chatLine':
                if event['room'] == 'player':
                    send_message(gameID, 'player', 'Hey '+event['username']+', don\'t you think you should surrender?')
            elif event['type'] == 'gameFull':
                # all info to create the game
                
            elif event['type'] == 'gameState':
                if event['status'] == 'started':
                    #handle moves
                elif event['status'] == 'resign':
                    if event['winner'] == self:
                        send_message(gameID, 'player', 'GG EZ')
                    else:
                        send_message(gameID, 'player', 'GG WP')

def send_message(gameID, chan, msg):
    """ 
    Send a message to the room 'chan' with content 'msg'
    """
    rep = s.post(APIURL+'bot/game/'+gameID+'/chat', params={ 'room': chan, 'text': msg })
    if rep.status_code != 200:
        print('send_messages requests not ok, code: ', rep.status_code, '\nerror: ', rep.content['error'], '\nreason: ', rep.text)
    rep.close()


def send_move(gameID, move, draw=False):
    with requests.post(APIURL+'bot/game/'+gameID+'/move/'+move, params={ 'offeringDraw': draw }) as rep:
        if rep.status_code != 200 :
            print('send_move requests not ok, code: ', rep.status_code, '\nerror: ', rep.content['error'], '\nreason: ', rep.text)
        return rep.content['ok']



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