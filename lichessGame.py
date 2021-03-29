import threading
import berserk
import logging
import time
import game as Game
import chess as chess


class LichessGame(threading.Thread):
    def __init__(self, client: berserk.Client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client

    def run(self):
        while True:
            try:
                for event in self.client.bots.stream_game_state(self.game_id):
                    if event['type'] == 'gameFull':
                        self.__create_game(event)
                    elif event['type'] == 'gameState':
                        self.__handle_state_change(event)
                    elif event['type'] == 'chatLine':
                        self.__handle_chat_line(event)
            except berserk.exceptions.ResponseError as e:
                logging.error('Invalid server response: {e}')
                if 'Too Many Requests for url' in str(e):
                    time.sleep(10)

    def __handle_state_change(self, event):
        if event['status'] == "started":
            moves = event['moves'].split(' ')
            if self.game.lastmove != moves[-1]:
                self.game.make_move(chess.Move.from_uci(moves[-1]))
                self.game.lastmove = moves[-1]
                if (self.game.board.turn and self.game.isWhite) or (not self.game.isWhite and not self.game.board.turn):
                    self.__bot_move(event)

    def __create_game(self, event):
        """ Create a chessGame from the event given """
        self.game = Game.ChessGame(event['id'], event)
        self.game.isWhite = event['white']['id'] == self.client.account.get()[
            'id']
        moves = event['state']['moves'].split(' ')
        for move in moves:
            if move != '':
                self.game.make_move(chess.Move.from_uci(move))
        self.game.lastmove = moves[-1]
        if (self.game.board.turn and self.game.isWhite) or (not self.game.isWhite and not self.game.board.turn):
            self.__bot_move(event)

    def __bot_move(self, event):
        botMove = self.game.get_move()
        try:
            if not self.client.bots.make_move(self.game_id, botMove):
                self.client.bots.resign_game(self.game_id)
                self.client.bots.post_message(
                    self.game_id, 'I wasn\'t able to do anything on this, well played!')
                logging.info(
                    f"Resigned game {self.game_id}, could not make a move.")
                logging.debug('invalid move, *resigning*, need to redo code!')
        except berserk.exceptions.ResponseError as e:
            logging.error('Invalid server response: {e}')
            if 'Too Many Requests for url' in str(e):
                time.sleep(10)

    def __handle_chat_line(self, event):
        # TODO
        pass
