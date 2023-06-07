from pygame import *


#переменные картинок
img_player1 = 'tank1.png' #картинка 1 игрока 
img_player2 = 'tank3.png' #картинка 2 игрока
img_back = 'purple.png'
img_bullet = 'bomb.png'

#Создание окон победы разных игроков
font.init()
font1 = font.Font(None, 80)
win1 = font1.render('RIGHT TANK WIN!', True, (10, 10, 255))
win2 = font1.render('LEFT TANK WIN!', True, (255, 10, 10))

#длина/ширина окна
win_width = 1400
win_height = 700

#создание окна
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#название окна
display.set_caption("Tanks")

#флаги
game_over = False #флаг окончиния цикла
win = False #флаг победы одного из игроков

#Создание группы стен
walls = sprite.Group()
#Создание группы пуль
bullets = sprite.Group()

#Основной класс 
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      sprite.Sprite.__init__(self)

      self.image = transform.scale(image.load(player_image), (size_x, size_y))
      self.speed = player_speed

      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
   def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

#Класс игрока
class Player(GameSprite):
   def player_move_two(self):
      keys = key.get_pressed()
      if keys[K_UP] and self.rect.y > 10:
         self.rect.y -= self.speed
      if keys[K_DOWN] and self.rect.y < win_height - 60:
         self.rect.y += self.speed
      if keys[K_LEFT] and self.rect.x > 10:
         self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < win_width - 60:
         self.rect.x += self.speed
   
   def fire_one(self):
      keys = key.get_pressed()
      if keys[K_SPACE]:
         if img_player1 == 'tank4.png':
            bullet = Bullet(img_bullet,self.rect.top+5,self.rect.centery, 10,10, 5)
            bullets.add(bullet)
         if img_player1 == 'tank2.png':
            bullet = Bullet(img_bullet,self.rect.buttom+5,self.rect.centery, 10,10, 5)
            bullets.add(bullet)
         if img_player1 == 'tank3.png':
            bullet = Bullet(img_bullet,self.rect.left+5,self.rect.centery, 10,10, 5)
            bullets.add(bullet)
         if img_player1 == 'tank1.png':
            bullet = Bullet(img_bullet,self.rect.right+5,self.rect.centery, 10,10, 5)
            bullets.add(bullet)
            
   
   def fire_two(self):
      keys = key.get_pressed()
      if keys[K_RSHIFT]:
         bullet = Bullet(img_bullet,self.rect.left-5,self.rect.centery, 10,10, -5)
         bullets.add(bullet)


   def player_move_one(self):
      keys = key.get_pressed()
      if keys[K_w] and self.rect.y > 10 or sprite.spritecollide(player_one, walls, False):
         self.rect.y -= self.speed
         img_player1 = 'tank4.png'
      if keys[K_s] and self.rect.y < win_height - 60 or sprite.spritecollide(player_one, walls, False):
         self.rect.y += self.speed
         img_player1 = 'tank2.png'
      if keys[K_a] and self.rect.x > 10 or sprite.spritecollide(player_one, walls, False):
         self.rect.x -= self.speed
         img_player1 = 'tank3.png'
      if keys[K_d] and self.rect.x < win_width - 60 or sprite.spritecollide(player_one, walls, False):
         self.rect.x += self.speed
         img_player1 = 'tank1.png'

#Класс стен
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_width = wall_width
        self.wall_height = wall_height
        #Картинка стены - прямоугольник нужных размеров и цвета
        self.image = Surface((self.wall_width, self.wall_height))
        self.image.fill((color_1, color_2, color_3))
        #Каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс пуль
class Bullet(GameSprite):
   def update(self):
       self.rect.x += self.speed
       if self.rect.y < 0 or self.rect.x < 0 or sprite.groupcollide(bullets, walls, True, False):
           self.kill()

#Экземпляры классов Player
player_one = Player(img_player1,100,100,50,50,10)
player_two = Player(img_player2,200,200,50,50,10)
#Экземпляры классов Wall
wall1 = Wall(240,240,240,200,300,10,200)
walls.add(wall1)


#игровой цикл
while not game_over:
    

   for e in event.get():
      if e.type == QUIT:
         game_over = True  
    
   if not win: 
      window.blit(background,(0,0))

      #Отрисовка и управление игроками
      player_one.player_move_one()
      player_one = Player(img_player1,player_one.rect.x,player_one.rect.y,50,50,10)
      player_one.reset()

      player_two.player_move_two()
      player_two.reset()

      #Стрельба первого игрока
      player_one.fire_one()
      #Стрельба второго игрока
      player_two.fire_two()



      #Отрисовка стен
      wall1.draw_wall()
      walls.draw(window)

      #Отрисовка пуль
      bullets.update()
      bullets.draw(window)
            
      #Проигрыш игроков
      if sprite.spritecollide(player_one, bullets, False):
         win = True
         window.blit(win1, (470,250))

      if sprite.spritecollide(player_two, bullets, False):
         win = True
         window.blit(win2,(470,250))

      display.update()
   time.delay(50)

