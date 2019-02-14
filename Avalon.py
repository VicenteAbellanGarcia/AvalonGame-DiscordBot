import discord
import random


client = discord.Client()
 
def checkNumberOfPlayers(msg):
    return msg.content.startswith('!Number')

def checkYesNo(msg):
    return msg.content.startswith('!Yes') or msg.content.startswith('!No')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("------------")
    
@client.event
async def on_message(message):
    if message.content.startswith('!Avalon'):
        await client.send_message(message.channel, "Let's start a Avalon game!")
        game = Game(client, message.author, message.channel)
        while(game):
            await client.send_message(message.channel,'A game is starting!')
            
            #Number of Players
            await client.send_message(message.channel,'How many players will be play? Use !NumberX where X is a number between 5-10')
            numberOfPlayers = await client.wait_for_message(check=checkNumberOfPlayers(message))
            game.setNumberPlayers(numberOfPlayers)
            if game.numberofPlayers == 0:
                 await client.send_message(message.channel, 'Error with the number of players')
                 break
        
            await client.send_message(message.channel, '2 roles for game will be Asassin and Merlin, the next roles will be optionals for the game, the other rols will be filled with Paladin for the Allies and Esbirro for the Enemies')
            
            #Play with Mordred
            await client.send_message(message.channel, 'You wanna play with Mordred? Mordred is a enemie and his identity is unknow for Merlin. Use !Yes or !No')
            msg1 = await client.wait_for_message(check=checkYesNo(message))
            if msg1.content=="!Yes":
                game.Mordred=True
            
            #Play with Percival
            await client.send_message(message.channel, 'You wanna play with Percival? Percival is a allie and he knows who is Merlin. Use !Yes or !No')
            msg2 = await client.wait_for_message(check=checkYesNo(message))
            if msg2.content=="!Yes":
                game.Percival=True
            
            #Play with Morgana
            await client.send_message(message.channel, 'You wanna play with Morgana? Morgana is a enemie and she pretends to be Merlin. Use !Yes or !No')
            msg3 = await client.wait_for_message(check=checkYesNo(message))
            if msg3.content=="!Yes":
                game.Morgana=True
            
            #Play with Oberon
            await client.send_message(message.channel, 'You wanna play with Oberon? Oberon is a enemie who doesnt know who are the others enemies and they dont know who is him. Use !Yes or !No')
            msg4 = await client.wait_for_message(check=checkYesNo(message))
            if msg4.content=="!Yes":
                game.Oberon=True
                
            game.defineRoles()
            await client.send_message(message.channel, 'The number of players is '+str(game.numberofPlayers)+'. Who will be playing? Use !me for join to the game')
            
            for x in range(0,game.numberofPlayers):
                msg = await client.wait_for_message(content="!me")
                game.parseMessage(msg.content, msg.author)
                await client.send_message(message.channel, 'Next Player?')
           
            await client.send_message(message.channel, 'All ready for start!')
            roles=game.giveRoles()
            for x in roles.keys():
                await client.send_message(x, "Your role this game is "+game.usersRoles[x])
                await client.send_message(x, "What you have to do this game? "+str(game.whatIDo(game.usersRoles[x])))
            game = None
    
    

    
        
#        for key in game.giveRoles().keys():
#            await client.send_message(message.channel, key.name)
        
        

class Game(object):
    #Object for the entire game.

    def __init__(self, client, owner, channel):
        

        self.client = client
        self.owner = owner
        self.channel = channel
        self.users = []
        self.usersRoles  = {}
        self.roles = []
        self.usersSet = False
        self.rolesSet = False
        self.numberofPlayers = 0
        self.Mordred = False
        self.Percival = False
        self.Morgana = False
        self.Oberon = False
        
    # Work out who's playing. 
    def setNumberPlayers(self,n):
        if n.content == "!Number5":
            self.numberofPlayers = 5
        elif n.content == "!Number6":
            self.numberofPlayers = 6
        elif n.content == "!Number7":
            self.numberofPlayers = 7
        elif n.content == "!Number8":
            self.numberofPlayers = 8
        elif n.content == "!Number9":
            self.numberofPlayers = 9
        elif n.content == "!Number10":
            self.numberofPlayers = 10
        else:
            self.numberofPlayers = 0
    
    #Set roles of the players
    def defineRoles(self):
        good=1
        bad=1
        self.roles.append("Merlin")
        self.roles.append("Asesino")
        if self.Morgana==True:
            self.roles.append("Morgana")
            bad+=1
        if self.Mordred==True:
            self.roles.append("Mordred")
            bad+=1
        if self.Oberon==True:
            self.roles.append("Oberon")
            bad+=1
        if self.Percival==True:
            self.roles.append("Percival")
            good+=1
        n=len(self.roles)
        if self.numberofPlayers>n:
            if self.numberofPlayers==5:
                cont=1
                while good < 3:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 2:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1
            elif self.numberofPlayers==6:
                cont=1
                while good < 4:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 2:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1
            elif self.numberofPlayers==7:
                cont=1
                while good < 4:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 3:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1
            elif self.numberofPlayers==8:
                cont=1
                while good < 5:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 3:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1
            elif self.numberofPlayers==9:
                cont=1
                while good < 6:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 3:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1
            elif self.numberofPlayers==10:
                cont=1
                while good < 6:
                    self.roles.append("Paladin"+str(cont))
                    good+=1
                    cont+=1
                cont=1
                while bad < 4:
                    self.roles.append("Esbirro"+str(cont))
                    bad+=1
                    cont+=1

            
        
    def giveRoles(self):
        return self.usersRoles
    
    def whatIDo(self, rol):
        EnemiesWithMordred = []
        EnemiesWithoutMordred = []
        MerlinAndMorgana = []
        Merlin = None
        for x in self.usersRoles.keys():
            if self.usersRoles[x] == "Merlin":
                Merlin = x.name
                MerlinAndMorgana.append(x.name)
            if self.usersRoles[x] == "Asesino":
                EnemiesWithMordred.append(x.name)
                EnemiesWithoutMordred.append(x.name)
            if self.usersRoles[x] == "Mordred":
                EnemiesWithMordred.append(x.name)
            if self.usersRoles[x] == "Morgana":
                MerlinAndMorgana.append(x.name)
        
        if rol=="Merlin":
            return ("You are part of the allies, you know who is the Enemies except Mordred, the enemies are " + str(EnemiesWithoutMordred))
        if rol=="Asesino":
            return ("You form part of the enemies and you know who are your mates, in this case the enemies are "+str(EnemiesWithMordred))
        if rol=="Mordred":
            return ("You form part of the enemies and you know who are your mates, in this case the enemies are "+str(EnemiesWithMordred))
        if rol=="Morgana":
            return ("You form part of the enemies and you know who are your mates, in this case the enemies are "+str(EnemiesWithMordred))
        if rol=="Percival":
            random.shuffle(MerlinAndMorgana)
            return ("You are part of the allies, you know who the players who are Morgana and Merlin, but not who is each one " + str(MerlinAndMorgana))
    
        
    def parseMessage(self, message, author):
        if self.usersSet == False:
            if message == "!me":
                print("received")
                self.users.append(author)
            if len(self.users)==self.numberofPlayers:
                self.usersSet = True
        if self.rolesSet == False and self.usersSet==True:
            for x in self.users:
                print(self.roles)
                rol0=  random.choice(self.roles)
                self.usersRoles[x] = rol0
                self.roles.remove(rol0)
            self.rolesSet=True
            
                    

client.run('Key for discord Bot')



