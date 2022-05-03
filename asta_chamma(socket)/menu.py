import pygame

class Button:
    def __init__(self,num,pos,size,bg_color,text_img):
        self.num = num
        self.rect = pygame.Rect(pos,size)
        self.bg_color = bg_color
        self.text_img = text_img
        self.text_size = text_img.get_size()
    def click(self,pos):
        return self.rect.collidepoint(pos) 
    def draw(self,screen):
        pygame.draw.rect(screen,self.bg_color,self.rect)
        screen.blit(self.text_img,(self.rect.x+(self.rect.width-self.text_size[0])//2,self.rect.y+(self.rect.height-self.text_size[1])//2))

