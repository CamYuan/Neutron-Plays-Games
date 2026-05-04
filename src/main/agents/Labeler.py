def labeler(dealerCard, softScore, hardScore, card1, canSplit, canDoubleDown):
    #TODO: Make this not so horrendous
    # print(dealerCard.rank, softScore, hardScore, card1.rank, card2.rank)
    choice = -1
    # if(card1.rank == card2.rank or (card1.rank > 9 and card2.rank > 9)):
    # basic strategy says to never split 10s so we won't include that in the check
    if(canSplit):
        #at this point, we know that the cards are splittable
        if(dealerCard.rank == 1): #breaking this out so I don't have to put it in every other if statemet
            if(card1.rank == 1 or card1.rank == 8):
                choice = 3
        else:
            if(card1.rank == 1):
                choice = 3
            elif(card1.rank == 2):
                if(dealerCard.rank < 8):
                    choice = 3
            elif(card1.rank == 3):
                if(dealerCard.rank < 8):
                    choice = 3
            elif(card1.rank == 4):
                if(dealerCard.rank == 5 or dealerCard.rank == 6):
                    choice = 3
            elif(card1.rank == 5):
                pass
            elif(card1.rank == 6):
                if(dealerCard.rank < 7):
                    choice = 3
            elif(card1.rank == 7):
                if(dealerCard.rank < 8):
                    choice = 3
            elif(card1.rank == 8):
                choice = 3
            elif(card1.rank == 9):
                if(dealerCard.rank < 7):
                    choice = 3
                elif(dealerCard.rank == 8 or dealerCard.rank == 9):
                    choice = 3
            '''elif(card1.rank > 9):
                pass '''
    if(choice == -1): #Check if the split logic was hit. Not all splittable pairs result ina split
    #----------HARDSCORE-----------------
        if (softScore == hardScore): #hardscore table since they are the same
            if(dealerCard.rank == 1): #breaking this out so I don't have to put it in every other if statemet
                if(hardScore >= 17):
                    choice = 0
                elif(canDoubleDown and hardScore == 11):
                    choice = 2
                else:
                    choice = 1
            else:
                if(hardScore >= 17):
                    choice = 0
                elif(hardScore == 16):
                    if(dealerCard.rank < 7):
                        choice = 0
                    else:
                        choice = 1
                elif(hardScore == 15):
                    if(dealerCard.rank < 7):
                        choice = 0
                    else:
                        choice = 1
                elif(hardScore == 14):
                    if(dealerCard.rank < 7):
                        choice = 0
                    else:
                        choice = 1
                elif(hardScore == 13):
                    if(dealerCard.rank < 7):
                        choice = 0
                    else:
                        choice = 1
                elif(hardScore == 12):
                    if(dealerCard.rank < 7 and dealerCard.rank > 3): #4,5,6
                        choice = 0
                    else:
                        choice = 1
                elif(hardScore == 11):
                    if(canDoubleDown):
                        choice = 2
                    else:
                        choice = 1
                elif(hardScore == 10):
                    if(canDoubleDown and dealerCard.rank < 10 ):
                        choice = 2
                    else:
                        choice = 1
                elif(hardScore == 9):
                    if(canDoubleDown and dealerCard.rank > 2 and dealerCard.rank < 7): #3,4,5,6
                        choice = 2
                    else:
                        choice = 1
                elif(hardScore < 9):
                    choice = 1
        #----------SOFTSCORE-----------------
        else: #softscore basic strategy
            if(dealerCard.rank == 1): #breaking this out so I don't have to put it in every other if statemet
                if(softScore >= 19):
                    choice = 0
                else:
                    choice = 1
            else:
                if(softScore >= 20):
                    choice = 0
                if(softScore == 19):
                    if(canDoubleDown and dealerCard.rank == 6):
                        choice = 2
                    else:
                        choice = 0
                elif(softScore == 18):
                    if(canDoubleDown and dealerCard.rank < 7):
                        choice = 2
                    elif(dealerCard.rank > 8):
                        choice = 1
                    else:
                        choice = 0
                elif(softScore == 17):
                    if(canDoubleDown and dealerCard.rank < 7 and dealerCard.rank > 2): #3,4,5,6
                        choice = 2
                    else:
                        choice = 1
                elif(softScore == 16):
                    if(canDoubleDown and dealerCard.rank < 7 and dealerCard.rank > 3): #4,5,6
                        choice = 2
                    else:
                        choice = 1
                elif(softScore == 15):
                    if(canDoubleDown and dealerCard.rank < 7 and dealerCard.rank > 3): #4,5,6
                        choice = 2
                    else:
                        choice = 1
                elif(softScore == 14):
                    if(canDoubleDown and dealerCard.rank < 7 and dealerCard.rank > 4): #5,6
                        choice = 2
                    else:
                        choice = 1
                elif(softScore == 13):
                    if(canDoubleDown and dealerCard.rank < 7 and dealerCard.rank > 4): #5,6
                        choice = 2
                    else:
                        choice = 1
                elif(softScore < 12):
                    choice = 1
    return choice
