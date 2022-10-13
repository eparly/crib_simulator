
#crib hand analyzer
from distutils.util import convert_path
import itertools
from operator import itemgetter
import random as r
import re
from statistics import mean

class Card:
    def __init__(self, value, suit):
        self.numbers=value
        self.suit=suit
        self.value = value if (int(value) < 10) else 10
                    
class Hand:
    def __init__(self, hand):
        self.hand=hand
        
    def getSuits(self):
        suits =[]
        for i in self.hand:
           suits.append(i.suit)
        return suits
    
    def getValues(self):
        values=[]
        for i in self.hand:
            if int(i.value)>10:
                values.append(10)
            else:
                values.append(int(i.value))
        return values
    
    def getNumbers(self):
        numbers = []
        for i in self.hand:
            numbers.append(int(i.numbers))
        return numbers

    def getCombos(self):
        suits = self.getSuits()
        values = self.getNumbers()
        suitValues = []
        for i in range(len(suits)):
            suitValues.append(str(values[i])+suits[i])
        combos = list(itertools.combinations(suitValues, 4))
        return combos

    def getSums(self):
        score = 0
        for i in range (len(self.getValues())+1):
            for sublist in itertools.combinations(self.getValues(), i):
                if sum(sublist) == 15:
                    score+=2
        return score

    def getPairs(self):
        score = 0
        cards = self.getNumbers()
        for i in range(len(cards)):
            for j in range(i): 
                if cards[i] == cards[j]:
                    score+=2
        return score
    
    def getRuns(self):
        score = 0
        runs = True
        cards =self.getNumbers()
        cards = sorted(cards)
        threeCombo = list(itertools.combinations_with_replacement(cards, 3))
        fourCombo = list(itertools.combinations_with_replacement(cards, 4))
        fiveCombo = list(itertools.combinations_with_replacement(cards, 5))

        if(runs):
            for i in fiveCombo:
                if(i[4]==i[3]+1 and i[3]==i[2]+1 and i[2]==i[1]+1 and i[1]==i[0]+1):
                    runs = False
                    score+=5
        if(runs):
            for i in fourCombo:
                if(i[3]==i[2]+1 and i[2]==i[1]+1 and i[1]==i[0]+1):
                    runs = False
                    score+=4
        if(runs):
            for i in threeCombo:
                if (i[2] == i[1]+1 and i[1]==i[0]+1):
                    runs = False
                    score+=3
        return score
    
    def getFlush(self):
        score = 0
        suits = self.getSuits()
        for i in range(len(suits)-1):
            dCount = suits.count('d')
            cCount = suits.count('c')
            sCount = suits.count('s')
            hCount = suits.count('h')
        score = max(dCount, cCount, hCount, sCount)
        if score >= 4:
            if suits[4]==suits[0]:
                score+=1
            return score
        return 0
        
    def jacks(self):
        score=0
        if self.getNumbers()[4] == 11:
            score+=2
        return score

    def getScore(self):
        score = 0
        score+= self.getPairs()
        score+= self.getFlush() 
        score+= self.getRuns() 
        score+= self.getSums()
        score+= self.jacks()
        return score

    


    

    
    #next steps:
    #find ev for 4+1 flipped card combos
    #get all groups of 4,
    #add every possible card to each group of 4
    #find score of that specific hand
    #find average score for group of 4 cards
    #find highest average score

class Deck:
    def __init__(self, cards):
        deck=[]
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        suits = ['h', 'd', 's', 'c']
        for i in numbers:
            for j in suits:
                deck.append(i+j)
        self.deck = deck
        self.cards = cards
    
    def getAvailableCards(self):
        deck = self.deck
        suits = self.cards.getSuits()
        values = self.cards.getNumbers()
        for i in range(len(suits)):
            suitValues = str(values[i])+suits[i]
            if deck.__contains__(suitValues):
                deck.remove(suitValues)
        return deck

    def getFlippedCard(self, idx):
        deck = self.getAvailableCards()
        return deck[idx]



def convertToHand(cards):
    hand=[]
    for i in cards:
        value = re.split('(\d+)', i)[1]
        suit = re.split('(\d+)', i)[2]
        hand.append(Card(value, suit))
    fiveHand = Hand(hand)
    return fiveHand

def getFiveCardHand(deck, hand):
    fiveCombos = []
    cardsAvailable = deck.getAvailableCards()
    for i in cardsAvailable:
        fiveCombos.append(hand + (i,))
    return fiveCombos



def getEV(hand, deck):
    fourCardCombos = hand.getCombos()
    scores = []
    for i in fourCardCombos:
        score = 0
        fiveCardCombos = getFiveCardHand(deck, i)
        for j in fiveCardCombos:
            if ('11c' in i):
                if j[4][-1] == 'c':
                    score+=1
            if ('11d' in i):
                if j[4][-1] == 'd':
                    score+=1
            if ('11s' in i):
                if j[4][-1] == 's':
                    score+=1
            if ('11h' in i):
                if j[4][-1] == 'h':
                    score+=1
            score+= convertToHand(j).getScore()
        scores.append(score)
    maxValue = max(scores)
    idxOfMax = scores.index(maxValue)
    maxValueHand = fourCardCombos[idxOfMax]
    return maxValueHand, maxValue/46

while(1):
    print("Enter cards in the order '#suit' ")
    handInput = input('enter 6 cards: \n').split(' ')
    hand = []
    deck = []
    for i in handInput:
        value = re.split('(\d+)', i)[1]
        suit = re.split('(\d+)', i)[2]
        hand.append(Card(value, suit))

    _hand =convertToHand(list(handInput))
    deck = Deck(_hand)

    
    print(getEV(_hand, deck))