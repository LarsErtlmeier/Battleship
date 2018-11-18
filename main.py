import player
player.init()

try:
    #mainloop
    while True:
        player.humanPlayer.turn()
        player.aiPlayer.turn()

        
except player.Victory:
    if aiPlayer.playerDefeatFlag:
        print("Congratulations!")
    elif humanPlayer.playerDeafeatFlag:
        print("Maybe next time?")
except:    
    raise Exception("I'm sorry. Something went wrong")




