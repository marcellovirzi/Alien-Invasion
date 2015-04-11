__author__ = 'marcellovirzi'

import pickle


class Game():
    def __init__(self):
        self._score = 0
        self._aliens_killed = 0
        self._para_saved = 0
        self._level = 1

    def update_score(self, amount):
        self._score += amount * self._level

    def get_score(self):
        return self._score

    def update_aliens_killed(self):
        self._aliens_killed += 1

    def get_aliens_killed(self):
        return self._aliens_killed

    def update_para_saved(self):
        self._para_saved += 1

    def get_para_saved(self):
        return self._para_saved

    def update_level(self, amount):
        self._level += amount

    def get_level(self):
        return self._level

    def save_game(self):
        save_data = {'score': self._score, 'level': self._level}
        save_file = open("savedata.dat", "wb")
        pickle.dump(save_data, save_file)

    def load_game(self):
        progress_file = open("savedata.dat", "rb")
        progress_data = pickle.load(progress_file)
        self._score = progress_data['score']
        self._level = progress_data['level']