from player1 import sub_Player,Player
import pygame

#cancelling the moves
####winner
#guddees
#arrows blitting
#4 players
#blinking

dice = [8,1,2,3,4]
lucky_dice = [8,4]
move_rect_pos = (800,120)
move_rect_size =(52,70)
safe_points=(0,4,8,12,24)

class Game:
    def __init__(self,id,num_of_players):
        self.id = id
        self.connected = False
        self.num_of_players = num_of_players
        if self.num_of_players == 2:
            self.players = [[Player(1,2,4,(1,0),(0,1)),
                            Player(2,2,0,(-1,0),(0,-1))],
                            [Player(1,2,0,(-1,0),(0,-1)),
                            Player(2,2,4,(1,0),(0,1))]]
        elif self.num_of_players == 4:
            self.players = [[Player(1,2,4,(1,0),(0,1)),
                            Player(2,4,2,(0,-1),(1,0)),
                            Player(3,2,0,(-1,0),(0,-1)),
                            Player(4,0,2,(0,1),(-1,0))],

                            [Player(1,0,2,(0,1),(-1,0)),
                            Player(2,2,4,(1,0),(0,1)),
                            Player(3,4,2,(0,-1),(1,0)),
                            Player(4,2,0,(-1,0),(0,-1))],

                            [Player(1,2,0,(-1,0),(0,-1)),
                            Player(2,0,2,(0,1),(-1,0)),
                            Player(3,2,4,(1,0),(0,1)),
                            Player(4,4,2,(0,-1),(1,0))],

                            [Player(1,4,2,(0,-1),(1,0)),
                            Player(2,2,0,(-1,0),(0,-1)),
                            Player(3,0,2,(0,1),(-1,0)),
                            Player(4,2,4,(1,0),(0,1))]]

        self.dice_rotate = True
        self.active_player = 1
        self.dice_index = 0
        self.moves = []
        self.move_counts = []
        self.move_rects = []
        self.eligible_moves = []
        self.extra_chance = False
        self.pawn_selected = False
        self.move_selected = False
        self.step = None
        self.moving_player = 0
        self.current_step = 0
        self.guddees = False
        self.step_counts_4_8 = [0,0]
        self.blink_count = 0
        self.winner = 0
        self.eligibility_checked = True

    def move(self):
        for player_set in self.players:
            player_set[self.active_player-1].sub_players[self.moving_player-1].move()
        self.current_step += 1
        if self.current_step == self.step: #moving completed
            ### code for kill
            if self.players[0][self.active_player-1].sub_players[self.moving_player-1].check_kill(self.players):
                self.extra_chance = True
                self.dice_rotate = True

            ## to delete the finished move
            index = self.moves.index(self.step)
            self.reset_play()
            if self.move_counts[index] > 1:
                self.move_counts[index] -= 1
            else:
                self.move_rects.pop() 
                self.move_counts.pop(index)
                self.moves.pop(index)
                if not len(self.moves) and not self.extra_chance:
                    #checking for winner
                    f = 1
                    for sub_player in self.players[0][self.active_player-1].sub_players:
                        if sub_player.score != 24:
                            f = 0
                            break
                    if f:
                        self.winner = self.active_player
                        ###
                    for player_set in self.players:
                        player_set[self.active_player-1].update_past()
                    self.switch_player()
                    self.dice_rotate = True
    
    def reset_play(self,just_dice_selection_reset = False):
        if not just_dice_selection_reset:
            self.current_step = 0 # resetting everything
            self.moving_player = 0
            self.pawn_selected = False
            self.eligibility_checked = False
        self.step = None
        self.move_selected = False      
        for player_set in self.players:
            for sub_player in player_set[self.active_player-1].sub_players: 
                if sub_player.eligible:
                    sub_player.eligible = False
    
    def reset_player_blitting(self):
        for player_set in self.players:
            for player in player_set:
                for sub_player in player.sub_players:
                    if sub_player.blitted:
                        sub_player.blitted = False 

    def pawn_selection(self,sub_p):
        self.moving_player = sub_p
        self.pawn_selected = True
    
    def dice_increase(self):
        #resetting guddees
        if self.guddees:
            self.guddess = False
            self.step_counts_4_8 = [0,0]

        self.dice_index += 1
        if self.dice_index > 4:
            self.dice_index = 0
    def dice_click(self,step):
        self.dice_rotate = False

        #inserting step into moves
        if step not in self.moves:
            self.moves.append(step)
            self.move_counts.append(1)
            self.move_rects.append(pygame.Rect((move_rect_pos[0],move_rect_pos[1]+(move_rect_size[1]+10)*len(self.move_rects)),move_rect_size))
        else:
            self.move_counts[self.moves.index(step)] += 1
        #fixing the dice_index
        if step > 4:
            self.dice_index = 0
        else:
            self.dice_index = step 
        if step in lucky_dice:
            self.extra_chance = True
            self.dice_rotate = True
        else:
            if self.extra_chance:
                self.extra_chance = False
            self.eligibility_checked = False
        #for guddees
        if step == 4:
            self.step_counts_4_8[0] += 1
        else:
            self.step_counts_4_8[0] = 0
        if step == 8:
            self.step_counts_4_8[1] += 1
        else:
            self.step_counts_4_8[1] = 0
        if 3 in self.step_counts_4_8:
            self.guddees = True

    def dice_eligibility(self):
        self.eligible_moves.clear()
        for step in self.moves:
            self.dice_selection(step)
            eligible = False
            for sub_player in self.players[0][self.active_player-1].sub_players:
                if sub_player.eligible:
                    eligible = True
                    break
            self.reset_play(just_dice_selection_reset = True)
            if eligible:
                self.eligible_moves.append(step)
        self.eligibility_checked = True
                
    def dice_selection(self,step):
        self.step = step
        self.move_selected = True
        for player_set in self.players:
            for sub_player in player_set[self.active_player-1].sub_players:
                sub_player.check_eligiblity(self.step)
        
    def switch_player(self):

        self.active_player += 1
        if self.active_player > self.num_of_players:
            self.active_player = 1
        print(self.active_player,self.num_of_players)
    
    def dice_cancel(self):
        for player_set in self.players: 
            for player in player_set:
                player.cancel()
        self.moves.clear()
        self.move_rects.clear()
        self.move_counts.clear()
        self.reset_play()
        self.switch_player()
        self.dice_rotate = True
    
    def blink_increase(self):
        self.blink_count += 1
        if self.blink_count > 10:
            self.blink_count = 0




        
        
