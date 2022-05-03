import pygame
import random
from network import Network
from menu import Button

pygame.init()
width=870
height=530
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("ASTA CHAMMA")
colors = {"white":pygame.Color("white"),
            "black":pygame.Color("black"),
              "red":pygame.Color("red"),
              "green":pygame.Color("green"),
              "blue":pygame.Color("blue"),
              "yellow":pygame.Color("yellow"),
              "pink":pygame.Color("pink"),
              "brown":pygame.Color("brown"),
              "grey":pygame.Color("grey"),
              "violet":pygame.Color("violet")}


font = pygame.font.SysFont("comicsans",40)
small_font = pygame.font.SysFont("comicsans",20)
home_text = font.render("HOME",1,colors["red"])
waiting_text = font.render("Waiting for another player...",1,colors["red"])
p1_text = font.render("YOUR TURN:",1,colors["green"])
p2_text = font.render("OPPONENT\'s TURN:",1,colors["red"])
win_text = font.render("YOU WON",1,colors["green"])
lose_text = font.render("YOU LOST",1,colors["red"])
text_rect_pos = (530,10)
text_rect_size = (320,100)

dice=[]
dice_nums = (8,1,2,3,4)
small_dice = []
for i in range(5):
    dice.append(pygame.image.load("n/"+str(i)+".png").convert())
    small_dice.append(pygame.image.load("n/s"+str(i)+".png").convert())
dice = tuple(dice)
small_dice = tuple(small_dice)
dice_size = dice[0].get_size()
small_dice_size = dice[0].get_size()
dice_pos =(530,120)
dice_rect = pygame.Rect(dice_pos,dice_size)

board_width = 500
size = 50
rows = board_width//size

nums=[] 
player_big_imgs = []
player_small_imgs = []
for i in range(1,5):
    nums.append(small_font.render(str(i),1,colors["red"]))
    player_big_imgs.append(pygame.image.load("players/b"+str(i)+".png"))
    player_small_imgs.append(pygame.image.load("players/s"+str(i)+".png"))

network = Network()
p1 = int(network.getP())
clock = pygame.time.Clock()

def drawGrid(screen,x,y):
    pygame.draw.rect(screen,colors["white"],(x,y,board_width,board_width))
    screen.fill(colors["grey"],(x+2*2*size,y,2*size,2*size))
    screen.fill(colors["grey"],(x+2*2*size,y+4*2*size,2*size,2*size))
    screen.fill(colors["grey"],(x,y+2*2*size,2*size,2*size))
    screen.fill(colors["grey"],(x+4*2*size,y+2*2*size,2*size,2*size))
    screen.fill(colors["grey"],(x+2*2*size,y+2*2*size,2*size,2*size))
    for i in range(rows//2+1):
            pygame.draw.line(screen,colors["black"],(x,y+i*2*size),(board_width+x,y+i*2*size),5)
            pygame.draw.line(screen,colors["black"],(x+i*2*size,y),(x+i*2*size,board_width+y),5)

def redraw_screen(screen,game = None):

    screen.fill(colors["yellow"])
    if game.winner:
        if game.winner == p1:
            text = win_text
            text_size = win_text.get_size()
        else:
            text = lose_text
            text_size = lose_text.get_size()
        screen.fill(colors["grey"])
        screen.blit(text,((width-text_size[0])//2,(height-text_size[1])//2))
            
    elif game.connected:
        pygame.draw.rect(screen,colors["black"],(dice_pos[0],dice_pos[1],dice_size[0]+20,dice_size[1]+20))
        drawGrid(screen,10,10)
        text_size = home_text.get_size()
        screen.blit(home_text,(10+2*2*size+size-text_size[0]//2,10+2*2*size+size-text_size[1]//2))
        screen.fill(colors["black"],(text_rect_pos[0],text_rect_pos[1],text_rect_size[0],text_rect_size[1]))
        if game.active_player == p1:
            text = p1_text
            text_size = p1_text.get_size()
        else:
            text = p2_text
            text_size = p2_text.get_size()
        screen.blit(text,(text_rect_pos[0]+(text_rect_size[0]-text_size[0])//2,text_rect_pos[1]+(text_rect_size[1]-text_size[1])//2))
        
        if game.blink_count > 3:
            pygame.draw.rect(screen,colors["green"],(game.players[p1-1][game.active_player-1].home,(2*size,2*size)),4)
   
        game.players[p1-1][game.active_player-1].draw(screen,game,player_small_imgs,player_big_imgs,p1,nums)
        for player in game.players[p1-1]:
            if game.active_player != player.num:
                player.draw(screen,game,player_small_imgs,player_big_imgs,p1)

        screen.blit(dice[game.dice_index],(dice_pos[0]+10,dice_pos[1]+10))
        for index in range(len(game.moves)):
            screen.fill(colors["black"],game.move_rects[index])
            if game.moves[index] > 4:
                screen.blit(small_dice[0],(game.move_rects[index].x+10,game.move_rects[index].y+10))
            else:
                screen.blit(small_dice[game.moves[index]],(game.move_rects[index].x+10,game.move_rects[index].y+10))
            if game.move_counts[index] > 1:
                count_text = small_font.render("x"+str(game.move_counts[index]),1,colors["red"])
                screen.blit(count_text,(game.move_rects[index].x+10,game.move_rects[index].y+10))
                ###
        if game.move_selected:
            pygame.draw.rect(screen,colors["green"],game.move_rects[game.moves.index(game.step)],3)
        if game.eligibility_checked:
            for index in range(len(game.moves)):
                if game.moves[index] not in game.eligible_moves:
                    pygame.draw.rect(screen,colors["red"],game.move_rects[index],3)
        if game.guddees:
            for i in range(1,4):
                pygame.draw.rect(screen,colors["red"],game.move_rects[i],3)
        
    else:
        text_size = waiting_text.get_size()
        screen.blit(waiting_text,((width-text_size[0])//2,(height-text_size[1])//2))
    pygame.display.update()

def draw_menu(screen,buttons):
    screen.fill((255,255,255))
    for button in buttons:
        button.draw(screen)
    pygame.display.update()

def menu():
    running = True
    buttons = [Button(1,(100,200),(300,200),(255,0,0),font.render("Two Players",1,(0,0,0))) ,
                Button(2,(470,200),(300,200),(255,0,0),font.render("Four Players",1,(0,0,0)))]
    
    num_of_players = 0
    while(running):
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos):
                        num_of_players = button.num*2
                        running = False
                        break

        draw_menu(screen,buttons)
    return num_of_players
        

def main():
    running = True
    
    print("You are player",p1)
    
    while(running):
        clock.tick(10)
        try:
            game = network.send("get")
        except:
            running = False
            print("Could not get the game")
            break

        game = network.send("eligible_blink")
        if p1 == game.active_player:
            if game.winner:
                redraw_screen(screen,game=game)
                pygame.time.delay(4000)
                return
                ###
            elif game.pawn_selected:
                game = network.send("move")
            elif game.move_selected:
                player_num = 0
                #automatic pawn selection
                for sub_player in game.players[0][game.active_player-1].sub_players:
                    if sub_player.eligible:
                        # dice_eligibility = True
                        if player_num:
                            player_num = 0
                            break
                        else:
                            player_num = sub_player.num
                if player_num:
                    game = network.send("pawn_selection_"+str(player_num))           
            elif game.dice_rotate:
                game = network.send("dice_increase")
            else:
                print("a")
                print(game.moves,game.eligible_moves)
                if not game.eligibility_checked and len(game.moves):
                    print("b")
                    game = network.send("dice_eligibility")
                    print(game.moves,game.eligible_moves)
                    if not len(game.eligible_moves) and len(game.moves):
                        redraw_screen(screen,game = game)
                        pygame.time.delay(1000)
                        game = network.send("dice_cancel")
                        print("sss")

                    elif len(game.eligible_moves) == 1:     # automatic dice selection
                        game = network.send("dice_selection_"+str(game.eligible_moves[0]))            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game.pawn_selected and game.connected and p1 == game.active_player and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if game.dice_rotate:
                    if dice_rect.collidepoint(pos):
                        step = 0
                        for i in range(4):
                            step += random.choice([0,1])
                        if not step:
                            step = 8
                        game = network.send("dice_click_"+str(step))
                        redraw_screen(screen,game = game)
                        pygame.time.delay(1000)
                else:
                    f = 0
                    if game.move_selected:
                        for sub_player in game.players[p1-1][game.active_player-1].sub_players:
                            if sub_player.eligible and sub_player.rect.collidepoint(pos):
                                f = 1
                                game = network.send("pawn_select_"+str(sub_player.num))
                                break
                    if not f:
                        for index in range(len(game.move_rects)):
                            if game.moves[index] in game.eligible_moves:
                                if game.move_rects[index].collidepoint(pos):
                                    game = network.send("dice_selection_"+str(game.moves[index]))
                                    break
                                
        redraw_screen(screen,game = game)

if p1 == 1:
    num_of_players = menu()
    print(num_of_players)
    none_object = network.send(str(num_of_players))
main()
pygame.quit()
        


        
