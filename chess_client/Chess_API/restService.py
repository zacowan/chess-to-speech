'''
Created on Oct 11, 2021

@author: Legacy
'''
import requests
import theMain
import gameEngine


def setupRestService():
    while theMain.init_complete:
        x = 5  # Wait for other threads to get Setup
    while True:
        response = requests.post("url", "data", "json")  # TODO:Fill in With Proper @IgnorePep8
        gameEngine.board = response.headers["Board"]
