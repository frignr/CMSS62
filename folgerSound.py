# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:17:42 2018

@author: seung
"""

import requests
import bs4
import csv

webpageFront = 'http://www.folgerdigitaltexts.org/'
funNameSounds = '/sounds'
playCodeList = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4', 'H5', 
             '1H6','2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac', 'MM', 'MV',
             'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3','Rom', 'Shr', 'Tmp', 
             'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK','WT']

playCodes = {'AWW': 'All\'s Well That Ends Well',
             'Ant': 'Antony and Cleopatra',
             'AYL': 'As You Like It', 
             'Err': 'The Comedy of Errors',
             'Cor': 'Coriolanus',
             'Cym': 'Cymbeline', 
             'Ham': 'Hamlet',
             '1H4': 'Henry IV, Part 1',
             '2H4': 'Henry IV, Part 2',
             'H5': 'Henry V',
             '1H6': 'Henry VI, Part 1',
             '2H6': 'Henry VI, Part 2',
             '3H6': 'Henry VI, Part 3',
             'H8': 'Henry VIII',
             'JC': 'Julius Caesar',
             'Jn': 'King John',
             'Lr': 'King Lear',
             'LLL': 'Love\'s Labor\'s Lost',
             'Mac': 'Macbeth',
             'MM': 'Measure for Measure',
             'MV': 'The Merchant of Venice',
             'Wiv': 'The Merry Wives of Windsor',
             'MND': 'A Midsummer Night\'s Dream',
             'Ado': 'Much Ado About Nothing',
             'Oth': 'Othello',
             'Per': 'Pericles',
             'R2': 'Richard II',
             'R3': 'Richard III',
             'Rom': 'Romeo and Juliet',
             'Shr': 'The Taming of the Shrew',
             'Tmp': 'The Tempest',
             'Tim': 'Timon of Athens',
             'Tit': 'Titus Andronicus',
             'Tro': 'Troilus and Cressida',
             'TN': 'Twelfth Night',
             'TGV': 'Two Gentlemen of Verona',
             'TNK': 'Two Noble Kinsmen',
             'WT': 'The Winter\'s Tale'}

#for play in playCodeList:
    
#Return the webpage for sounds of the playCode
def soundWeb(playCode):
    return webpageFront + playCode + funNameSounds

#Return the number of sounds in each act. 0 = induction, 1-5 = act 1-5, 6 = total
def findNumSound(playCode):
    webpage = soundWeb(playCode)
    soup = bs4.BeautifulSoup(requests.get(webpage).text)
    
    numSounds = [0] * 6
    checkSD = False
    checkNum = False
    for c in soup.text:
        if checkNum:
            if c == 'I':
                numSounds[0] +=1
                checkNum = False
            if c.isdigit():
                numSounds[int(c)] +=1
                checkNum = False
        elif checkSD:
            if c == 'D':
                checkNum = True
            checkSD = False
        elif c == 'S':
            checkSD = True
    numSounds.append(sum(numSounds))
    return numSounds

playNumSounds = {}
for play in playCodeList:
    playNumSounds[play] = findNumSound(play)
    
with open('playSounds.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, dialect = 'excel')
    writer.writerow(['Play Code', 'Induction', 'Act 1', 'Act 2', 'Act 3', 
                     'Act 4', 'Act 5', 'Total'])
    for play in playCodeList:
        writer.writerow([play] + playNumSounds[play])
    