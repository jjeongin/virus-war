import os, random
path = os.getcwd()
add_library("sound")
bgm = SoundFile(this, path + "/sound/" + "bgm1.mp3")
diceSound = SoundFile(this, path + "/sound/" + "dice.mp3")
BOARD_SIZE = 600
SQUARE_SIDE = 6 # number of squares on each side of the board
SQUARE_W = BOARD_SIZE/(SQUARE_SIDE+4) # width of each square
SQUARE_H = SQUARE_W*2 # height of each square
NUM_PLAYERS = 4
HEALTH = 500
VACCINES = 100
RESOLUTION_W = 900
RESOLUTION_H = BOARD_SIZE

class Land:
    def __init__(self, i):
        self.i = i # land index (starting point: 0, ...27)
        
        # width and height of the land
        if self.i%(SQUARE_SIDE+1) == 0:
            self.w = SQUARE_H
        else:
            self.w = SQUARE_W
        self.h = SQUARE_H
            
        self.coordinates = [[540,540],[450,540],[390,540],[330,540],[270,540],[210,540],[150,540],[60,540],[60,450],[60,390],[60,330],[60,270],[60,210],[60,150],[60,60],[150,60],[210,60],[270,60],[330,60],[390,60],[450,60],[540,60],[540,150],[540,210],[540,270],[540,330],[540,390],[540,450]]
        for c in self.coordinates:
            c[0] += (RESOLUTION_W-BOARD_SIZE)/2
        
        self.x = self.coordinates[self.i][0]
        self.y = self.coordinates[self.i][1]
                    
    def __eq__(self, other):
        return self.i == other.i
            
class HarmfulLand(Land):
    def __init__(self, i, h):
        Land.__init__(self, i)
        self.h = h
        
    # deduct player's health
    def deduct_health(self, player):
        player.health -= self.h
        player.updated = True
        
class PossessibleLand(Land):
    def __init__(self, i, h, v):
        Land.__init__(self, i)
        self.h = h
        self.v = v
        self.owner = None
        
    #checking whether play can buy the possessible land or not
    def buy_or_not(self, player):
        if player.health > self.h: 
            game.display_message("Buy this land? Y/N")
            if game.key_handler['Y'] == True:
                game.key_handler['Y'] = False
                player.health -= self.h
                self.owner = player
                player.properties.append(self)
                player.updated = True
            elif game.key_handler['N'] == True:
                game.key_handler['N'] = False
                player.updated = True
        elif player.health <= self.h:
            player.updated = True
     
     #making the player pay the toll fee for the land that the other player possesses
    def pay_fee(self, player):
        player.vaccines -= self.v
        self.owner.vaccines += self.v
        player.updated = True

class Hospital(Land):
    def __init__(self, i):
        Land.__init__(self, i)
        
    #health cure whenever a player lands on hospital
    def health_cure(self, player):
        player.health += player.vaccines*2
        player.updated = True
        
class Jail(Land):
    def __init__(self, i):
        Land.__init__(self, i)
        
    #whenever a player gets in jail, the player has to stay there until the fourth turn
    def imprison(self, player):
        if player.imprisoned_turn == 4:
            player.imprisoned = False
            player.imprisoned_turn = 0
        else:
            player.imprisoned = True
            player.imprisoned_turn += 1
            
        player.updated = True
        
class ChanceCard(Land):
    def __init__(self,i):
        Land.__init__(self,i)
        self.cards = ["Health Gain", "Health Reduce", "Random Health Exchance", "Plane Ticket", "Imprisonment"]
        self.chosen_card = None
        
    #drawing card for the chance card land, and then implementing it
    def draw_card(self, player):
        if self.chosen_card == None:
            self.chosen_card = random.choice(self.cards)
            game.frame = 0
            game.frame = frameCount
            
        game.display_message(self.chosen_card)

        if frameCount >= game.frame+120:
            if self.chosen_card == self.cards[0]:
                player.health += 20
                player.updated = True
                        
            elif self.chosen_card == self.cards[1]:
                player.health -= 20
                player.updated = True
                
            elif self.chosen_card == self.cards[2]:
                temp_h = player.health
                nums = []
                for i in range(NUM_PLAYERS):
                    nums.append(i)
                nums.remove(player.num)
                rand_num = random.choice(nums)
                player.health = game.players[rand_num].health
                game.players[rand_num].health = temp_h
                player.updated = True
                
            elif self.chosen_card == self.cards[3]:
                player.location = Land(game.board.airplane.i)
                
            elif self.chosen_card == self.cards[4]:
                player.location = Land(game.board.jail.i)
                
            self.chosen_card = None
        
class Airplane(Land):
    def __init__(self, i):
        Land.__init__(self, i)

    #player can choose where to fly when they land on airplane
    def fly(self, player):
        posx = mouseX
        posy = mouseY
        
        game.display_message("Click the land you want to go.")
        
        if mousePressed:
            if 630<= posx <750 and 480<= posy <600:
                player.location = Land(0)
                
            elif 570<= posx <630 and 480<= posy <600:
                player.location = Land(1)

            elif 510<= posx <570 and 480<= posy < 600:
                player.location = Land(2)
            
            elif 450<= posx <510 and 480<= posy < 600:
                player.location = Land(3)
            
            elif 390<= posx <450 and 480<= posy < 600:
                player.location = Land(4)
            
            elif 330<= posx <390 and 480<= posy < 600:
                player.location = Land(5)
            
            elif 270<= posx <330 and 480<= posy < 600:
                player.location = Land(6)
                
            elif 150<= posx < 270 and 480<= posy < 600:
                player.location = Land(7)
                
            elif 150<= posx < 270 and 420<= posy < 480:
                player.location = Land(8)
                
            elif 150<= posx < 270 and 360<= posy < 420:
                player.location = Land(9)
                
            elif 150<= posx < 270 and 300<= posy <360:
                player.location = Land(10)
            
            elif 150<= posx < 270 and 240<= posy <300:
                player.location = Land(11)
                
            elif 150<= posx < 270 and 180<= posy <240:
                player.location = Land(12)
                
            elif 150<= posx <270 and 120<= posy <180:
                player.location = Land(13)
                
            elif 150<= posx <270 and 0<= posy <120:
                player.location = Land(14)
            
            elif 270<= posx <330 and 0<= posy <120:
                player.location = Land(15)
                
            elif 330<= posx <390 and 0<= posy <120:
                player.location = Land(16)
                
            elif 390<= posx <450 and 0<= posy <120:
                player.location = Land(17)
                
            elif 450<= posx <510 and 0<= posy <120:
                player.location = Land(18)
                
            elif 510<= posx <570 and 0<= posy <120:
                player.location = Land(19)
                
            elif 570<= posx <630 and 0<= posy <120:
                player.location = Land(20)
                
            elif 630<= posx <750 and 120<= posy <180:
                player.location = Land(22)
                
            elif 630<= posx <750 and 180<= posy <240:
                player.location = Land(23)
                
            elif 630<= posx <750 and 240<= posy <300:
                player.location = Land(24)
                
            elif 630<= posx <750 and 300<= posy <360:
                player.location = Land(25)
                
            elif 630<= posx <750 and 360<= posy <420:
                player.location = Land(26)
                
            elif 630<= posx <750 and 420<= posy <480:
                player.location = Land(27)

class Board:
    def __init__(self):
        self.w = BOARD_SIZE
        self.h = BOARD_SIZE
        self.img = loadImage(path + "/images/" + "board.png")
        
        # add lands to the board
        self.lands = []
        for i in range(27):
            self.lands.append(Land(i))
        
        self.harmful_lands = []
        self.harmful_lands.append(HarmfulLand(1,5))
        self.harmful_lands.append(HarmfulLand(4,10))
        self.harmful_lands.append(HarmfulLand(9,15))
        self.harmful_lands.append(HarmfulLand(11,20))
        self.harmful_lands.append(HarmfulLand(16,35))
        self.harmful_lands.append(HarmfulLand(19,55))
        self.harmful_lands.append(HarmfulLand(22,75))
        self.harmful_lands.append(HarmfulLand(27,100))
        
        self.possessible_lands = []
        self.possessible_lands.append(PossessibleLand(2,10,12))
        self.possessible_lands.append(PossessibleLand(5,20,25))
        self.possessible_lands.append(PossessibleLand(6,15,20))
        self.possessible_lands.append(PossessibleLand(10,25,30))
        self.possessible_lands.append(PossessibleLand(12,30,40))
        self.possessible_lands.append(PossessibleLand(13,35,40))
        self.possessible_lands.append(PossessibleLand(15,50,55))
        self.possessible_lands.append(PossessibleLand(17,60,65))
        self.possessible_lands.append(PossessibleLand(18,55,57))
        self.possessible_lands.append(PossessibleLand(20,60,70))
        self.possessible_lands.append(PossessibleLand(23,80,90))
        self.possessible_lands.append(PossessibleLand(24,50,70))
        self.possessible_lands.append(PossessibleLand(26,70,95))
        
        self.hospitals = []
        self.hospitals.append(Hospital(0))
        self.hospitals.append(Hospital(14))
        
        self.chanceCards = []
        self.chanceCards.append(ChanceCard(3))
        self.chanceCards.append(ChanceCard(8))
        self.chanceCards.append(ChanceCard(25))
        
        self.jail = Jail(7)
        self.airplane = Airplane(21)
        
    def display(self):
        # display the board
        image(self.img, (RESOLUTION_W-BOARD_SIZE)/2, 0, self.w, self.h)
                    
class Player:
    def __init__(self, num):
        self.num = num
        self.health = HEALTH
        self.vaccines = VACCINES
        self.location = Land(0)
        self.properties = []
        self.imprisoned_turn = 0
        self.imprisoned = False
        self.moved = False
        self.updated = False
        self.img = loadImage(path + "/images/player" + str(self.num+1) + ".png")
        
    def display(self):
        # display player information
        textSize(15)
        if self.num == 0:
            fill(168, 126, 229)
        elif self.num == 1:
            fill(45, 179, 179)
        elif self.num == 2:
            fill(126, 161, 229)
        elif self.num == 3:
            fill(242, 170, 206)
        textAlign(TOP, LEFT)
        text("Player " + str(self.num+1) + "\nHealth: " + str(self.health) + "\nVaccines: " + str(self.vaccines), 10, 20+self.num*120)
        
        # display player's properties
        for p in self.properties:
            if p.i < SQUARE_SIDE+1:
                circle(p.x, p.y-70, 10)
            elif p.i < 2*(SQUARE_SIDE+1):
                circle(p.x+70, p.y, 10)
            elif p.i < 3*(SQUARE_SIDE+1):
                circle(p.x, p.y+70, 10)
            elif p.i < 4*(SQUARE_SIDE+1):
                circle(p.x-70, p.y, 10)
            
        # display player on the board
        image(self.img, self.location.x-20, self.location.y-20, 40, 40)
        
    def move(self):
        # roll the dice
        diceSound.play()
        if self.imprisoned == False:
            game.dice1 = random.randint(1,6)
            game.dice2 = random.randint(1,6)

            self.location.i = (self.location.i + game.dice1 + game.dice2)%(SQUARE_SIDE*4+4)
            self.location = Land(self.location.i)
                
    def update(self):
        for l in game.board.harmful_lands:
            if self.location.i == l.i:
                l.deduct_health(self)
                
        for l in game.board.possessible_lands:
            if self.location.i == l.i:
                if l.owner == None and self.health > l.h:
                    l.buy_or_not(self)
                elif l.owner != None:
                    l.pay_fee(self)
                        
        for l in game.board.hospitals:
            if self.location.i == l.i:
                l.health_cure(self)
        
        for l in game.board.chanceCards:
            if self.location.i == l.i:
                l.draw_card(self)
                
        if self.location == game.board.jail:
            game.board.jail.imprison(self)
                
        if self.location == game.board.airplane:
            game.board.airplane.fly(self)
                
class Game:
    def __init__(self):
        self.board = Board()
        self.key_handler = {'Y':False, 'N':False, 'SPACE':False}
        self.frame = 0
        self.players = []
        for i in range(NUM_PLAYERS):
            self.players.append(Player(i))
        self.player = random.choice(self.players) # current player
        
        self.dice1 = 0
        self.dice2 = 0
        self.dice_imgs = []
        for i in range(6):
            self.dice_imgs.append(loadImage(path + "/images/dice" + str(i+1) + ".png"))
        
    def display(self):
        # display the board
        self.board.display()
        
        # display the existing players
        for p in self.players:
            p.display()
        
        # player rolls the dice and moves   
        if self.player.moved == False:
            self.display_message("Player " + str(self.player.num) + ", roll the dice")
            if self.key_handler['SPACE'] == True:
                self.player.move()
                self.frame = frameCount
                self.player.moved = True
                self.key_handler['SPACE'] = False
        
        if self.player.moved == True:
            # display dice number
            if self.frame < frameCount < self.frame+80:
                image(self.dice_imgs[self.dice1-1], 350, RESOLUTION_H-SQUARE_H-70, 50, 50)
                image(self.dice_imgs[self.dice2-1], 500, RESOLUTION_H-SQUARE_H-70, 50, 50)
            else:
                # update the players status based on their new location
                self.player.update()
        
        if self.player.updated == True:
            # check if the player is dead
            if self.player.health <= 0:
                if self.player in self.players:
                    self.players.remove(self.player)
                    
            # if the game hasn't ended yet, change the turn
            if self.check_end() == False:
                self.player.moved = False
                self.player.updated = False
                
                turn = self.player.num
                turn = (turn + 1) % NUM_PLAYERS
                for p in self.players:
                    if p.num == turn:
                        self.player = p
                
    # display message on the screen
    def display_message(self, msg):
        textSize(15)
        fill(0,0,0)
        textAlign(CENTER)
        text(msg, RESOLUTION_W/2, RESOLUTION_H*2/3)
              
    # check if the game has ended
    def check_end(self): 
        if len(self.players) == 1:
            clear()
            textSize(20)
            textAlign(CENTER)
            fill(255,255,255)
            text("Player " + str(self.player.num+1) + " WON \nClick the screen to restart the game.", RESOLUTION_W/2, RESOLUTION_H/3)
            return True
        else:
            return False
    
game = Game()

def setup():
    bgm.loop()
    size(RESOLUTION_W, RESOLUTION_H)
    background(255, 255, 255)
    
def draw():
    clear()
    background(255, 255, 255)
    game.display()
    if game.check_end() == True:
        noLoop()
    
def mouseClicked():
    game.mouse_clicked = True
    
def keyReleased():
    if key == 'y' or key == 'Y':
        game.key_handler['Y'] = True
    elif key == 'n' or key == 'N':
        game.key_handler['N'] = True
    elif key == ' ' and game.player.moved == False:
        game.key_handler['SPACE'] = True
    
# reset the game when the game is over by a mouse click    
def mousePressed():
    if game.check_end() == True:
        global game
        game = Game()
        loop()
