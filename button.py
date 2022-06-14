import pygame 

pygame.init()

# A class for the interface menu buttons
class Button():
    def __init__(self, image, x_pos, y_pos, text_input, font_size):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.button_font = pygame.font.SysFont("arial", font_size)
        self.text = self.button_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)
        
    def checkMousePos(self, pos):
        return pos[0] in range(self.rect.left, self.rect.right) and\
			 pos[1] in range(self.rect.top, self.rect.bottom)

    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and\
            pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.button_font.render(self.text_input, True, 'yellow')
        else:
            self.text = self.button_font.render(self.text_input, True, "white")
            
    def draw(self, surface):
        self.update(surface)
        self.changeColor(pygame.mouse.get_pos())
        pygame.display.update()
