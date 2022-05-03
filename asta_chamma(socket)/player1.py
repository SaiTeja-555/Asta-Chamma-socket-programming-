import pygame

safe_points=(0,4,8,12,24)
turn_points=(2,6,10,14,15,20,22,23,18,24)
size = 50

class sub_Player:
    def __init__(self,parent,x,y,num):
        self.rect = pygame.Rect(parent.home[0],parent.home[1],2*size,2*size)
        self.parent = parent
        self.num=num
        self.eligible = False
        self.dir=parent.home_dir[0]
        self.last_dir=parent.home_dir[1]
        self.score=0
        self.past_pos = (self.rect.x,self.rect.y)
        self.past_dir = self.dir
        self.past_last_dir =self.last_dir
        self.past_score = self.score 
        self.blitted = False

    def move(self):
        if self.score in turn_points:
            if self.score!=turn_points[-2]:
                self.dir,self.last_dir=(-self.last_dir[0],-self.last_dir[1]),self.dir
            else:
                self.dir,self.last_dir=self.last_dir,self.dir
        self.score+=1
        self.rect.x += 2*size*self.dir[0]
        self.rect.y += 2*size*self.dir[1]
    
    def check_eligiblity(self,step):
        self.eligible = True
        to_score = self.score + step
        if to_score > self.parent.limit:
            self.eligible = False
        elif to_score not in safe_points:
            for player in self.parent.sub_players:
                if player.score == to_score:
                    self.eligible = False
                    break
    
    def calculate_gang(self,players):
        gang = []
        for player in players:
            if player.num != self.parent.num:
                for sub_player in player.sub_players:
                    if self.rect.x == sub_player.rect.x and self.rect.y == sub_player.rect.y:
                        if self.score in safe_points:
                            if self.num == sub_player.num:
                                gang.append(sub_player)
                        else:
                            gang += [player.num,sub_player.num]
                            break
        return gang

    def check_kill(self,players):
        if self.score not in safe_points:
            gang = self.calculate_gang(players[0])
            if len(gang):
                killed_player_num,killed_sub_player_num = gang[0],gang[1]
                for player_set in players:
                    player_set[killed_player_num-1].sub_players[killed_sub_player_num-1].killed()
                if not self.parent.kills:
                    for player_set in players:
                        player_set[self.parent.num-1].limit = 24
                for player_set in players:
                    player_set[self.parent.num-1].kills += 1
                return True
        return False

    def update_past(self):
        self.past_pos = (self.rect.x,self.rect.y)
        self.past_dir = self.dir
        self.past_last_dir =self.last_dir
        self.past_score = self.score

    def cancel(self):
        self.rect.x = self.past_pos[0]
        self.rect.y = self.past_pos[1]
        self.dir = self.past_dir
        self.last_dir = self.past_last_dir
        self.score = self.past_score

    def killed(self):
        self.rect.x = self.parent.home[0]
        self.rect.y = self.parent.home[1]
        self.dir=self.parent.home_dir[0]
        self.last_dir=self.parent.home_dir[1]
        self.score = 0
    
    def draw(self,screen,game,player_small_imgs,player_big_imgs,num_img,p1):
            
        if self.score in safe_points:
            if self.num == 1:
                pos = (self.rect.x,self.rect.y)
            elif self.num == 2:
                pos = (self.rect.x+size,self.rect.y)
            elif self.num == 3:
                pos = (self.rect.x,self.rect.y+size)
            else:
                pos = (self.rect.x+size,self.rect.y+size)
        else:
            pos = (self.rect.x+size//2,self.rect.y+size//2)

        if self.score in safe_points:
            gang = self.calculate_gang(game.players[p1-1])
        else:
            gang = []

        if not self.blitted:

            if self.parent.num == game.active_player:
                img = player_big_imgs[self.parent.num-1]
                y_gap = -15
            else:
                img = player_small_imgs[self.parent.num-1]
                y_gap = 5
            img_size = img.get_size()

            if not len(gang):
                if game.active_player == p1 and self.eligible and game.blink_count > 5:
                    pygame.draw.circle(screen,(0,255,0),(pos[0]+size//2,pos[1]+y_gap+img_size[1]),6)
                
                screen.blit(img,(pos[0]+(size-img_size[0])//2,pos[1]+y_gap))
                if game.active_player == p1 and self.eligible:
                    screen.blit(num_img,(pos[0]+size//2-num_img.get_size()[0]//2-2,pos[1]+img_size[1]//2+y_gap-15))
            else:
                img2_size = player_small_imgs[0].get_size()
                y2_gap = 5
                if self.parent.num == game.active_player:
                    x_adjust_size = (size-(size//(2*(len(gang)+1))+img_size[0]//2))//len(gang)
                else:
                    x_adjust_size = size//(len(gang)+1)
                x2_addjust_size = size//(len(gang)+1)
                for player_index in range(len(gang)):
                    screen.blit(player_small_imgs[gang[player_index].parent.num-1],(pos[0]+player_index*x_adjust_size+(x_adjust_size-img2_size[0])//2,pos[1]+y2_gap))
                    gang[player_index].blitted = True
                
                if game.active_player == p1 and self.eligible and game.blink_count > 5 :
                    pygame.draw.circle(screen,(0,255,0),(pos[0]+size-size//(2*(len(gang)+1)),pos[1]+y_gap+img_size[1]),6)
                screen.blit(img,(pos[0]+len(gang)*x2_addjust_size+(x2_addjust_size-img_size[0])//2,pos[1]+y_gap))
                if game.active_player ==p1 and self.eligible:
                    screen.blit(num_img,(pos[0]+size-size//(2*(len(gang)+1))-num_img.get_size()[0]//2-2,pos[1]+img_size[1]//2+y_gap-15))

class Player:

    def __init__(self,num,x,y,dirn,last_dir):
        self.num = num
        self.home = (10+x*2*size,10+y*2*size)
        self.sub_players=[]
        self.kills=0
        self.limit = 15  ###should be changed if there is a kill
        self.home_dir=(dirn,last_dir)
        self.past_kills = 0
        k=1
        for i in range(2):
            for j in range(2):
                self.sub_players.append(sub_Player(self,x,y,k))
                k+=1
        self.sub_players=tuple(self.sub_players)

    # def move(self,player):
    #     self.sub_players[player-1].move()
    
    def update_past(self):
        self.past_kills = self.kills
        for player in self.sub_players:
            player.update_past()

    def cancel(self):
        self.kills = self.past_kills
        for player in self.sub_players:
            player.cancel()
        
    def draw(self,screen,game,player_small_imgs,player_big_imgs,p1,nums = [None,None,None,None]):
        for player in self.sub_players:
            player.draw(screen,game,player_small_imgs,player_big_imgs,nums[player.num-1],p1)
                
