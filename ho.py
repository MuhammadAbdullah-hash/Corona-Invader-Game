import pygame
import time
from itertools import zip_longest



my_img = pygame.image.load('cor.jpg')
super_sayian = pygame.image.load('super.gif')
blast_img = pygame.image.load('blast_2.png')
back_img = pygame.image.load('b_2.jpg')
exp_img = pygame.image.load('exp.jpg')

my_img = pygame.transform.scale(my_img, (50,50))
my_img_2 = pygame.transform.scale(my_img, (20,20))
my_img_3 = pygame.transform.scale(super_sayian , (70,70))
my_img_4 = pygame.transform.scale(blast_img , (20,20))
my_img_5 = pygame.transform.scale(back_img , (500,500))
my_img_6 = pygame.transform.scale(exp_img , (60,60))


class Bullet:
	def __init__(self , root ,x , y  , face ,obj  , name):
		self.root , self.x , self.y = root , x , y 
		self.face = face	
		self.obj = obj
		self.name = name
	def is_colide(self):
		self.a , self.b = False , False
		if (((self.obj.x+self.obj.w)>= (self.x) >= self.obj.x) and ((self.obj.y+self.obj.h)>= (self.y) >= self.obj.y)) or ((self.obj.x+self.obj.w)>= (self.x) >= self.obj.x) and ((self.obj.y-self.obj.h)>= (self.y) >= self.obj.y):
			print(' ############ COLLIDE ######### ')
			return True		
		return False

	def draw(self):	
		self.y+=(5*self.face)
		self.root.blit(self.name , (self.x , self.y))

class Player:
	def __init__(self, root , x , y  , w,  h):
		self.root , self.x , self.y  = root,  x ,y
		self.w , self.h = w  , h
	def draw_me(self , x4):
		self.x  = x4 
		self.root.blit(my_img_3 , (self.x , self.y))
		pygame.display.update()

class Enemy:
	def __init__(self, root , x , y , w , h ):
		self.root , self.x , self.y = root,  x ,y 
		self.face = -1
		self.w , self.h = w , h
	def draw_it(self):
		self.x+=(3*self.face)
		if self.x<=0:
			self.face = 1
		if (self.x+self.w) >= 500:
			self.face = -1			
		self.root.blit(my_img , (self.x , self.y))	
		pygame.display.update()

def transition(itr , dire , itr2):
	for i in itr:
		i.draw()
		if dire == -1:
			if i.y<0:
				itr.pop(itr.index(i))
		if dire == 1:
			if i.y>500:
				itr.pop(itr.index(i))


def add_obj(surf, x2 , y2 , itr , dire  , obj  , name):
	if len(itr) == 0:
		itr.append(Bullet(surf , x2 , y2 ,   dire   , obj , name ))
	else:
		if len(itr) < 8:
			if  itr[-1].y < (p.y - 20):
				itr.append(Bullet(surf , x2 , y2  , dire  , obj  , name))		
def check_collison():
	global score , score_en
	for i in lis:
		if i.is_colide():
			coll_snd.play()
			lis.pop(lis.index(i))
			score+=1
	for i in lis_e:
		if i.is_colide():
			coll_snd.play()
			lis_e.pop(lis_e.index(i))
			score_en+=1
	z = list(zip_longest(lis , lis_e , fillvalue = 'X'))
	for j in z:
		if j[0]!='X' and j[1]!='X':
			if (j[0].y == j[1].y) or (j[0].x == j[1].x):
				try:
					coll_snd.play()				
					lis.pop(z.index(j))
					lis_e.pop(z.index(j))
				except:
					print(' ************************* ERRROR ********************************** ')	
				
def cal_time():
	global minute ,set_min , sec
	tim = pygame.time.get_ticks()
	sec = tim/1000
	if int(sec)%60 == 0 and int(sec) !=0:
		lis_min.append(int(sec))
		tim = 0
	if lis_min.count(int(sec)) == 1 :	
		minute+=1
		tim = 0
         

pygame.init()
wind = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

coll_snd = pygame.mixer.Sound('mus.wav')

music = pygame.mixer.music.load('back.mp3')
pygame.mixer.music.play(-1)

x , y = 200,450
x_e , y_e = 100,70 
vel , run , hit = 5 , True , False
lis ,lis_e ,count =[], [] , 0 
font = pygame.font.SysFont('comicsans' , 30  , True , 	True)
score , score_en = 0 , 0
minute , lis_min = 0 , []
e = Enemy(wind ,x_e , y_e , 50,50 )
p = Player(wind , x,y  , 70,70)	

while run:
	clock.tick(40)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	wind.blit(my_img_5 , (0,0))		

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and x>0:
		x-=vel
	if keys[pygame.K_RIGHT] and (x+70) < 500:
		x+=vel	
	if keys[pygame.K_SPACE]:
		x2 , y2 = p.x , p.y
		add_obj(wind , x2,y2,lis , -1  , e , my_img_4)
		hit = True
	if hit:	
		transition(lis , -1 , lis_e)
	e.draw_it()		
	p.draw_me(x)
	if count%15 == 0:
		x3 , y3 =  e.x , e.y
		add_obj(wind , x3 , y3 , lis_e , 1  , p , my_img_2)
	transition(lis_e , 1 , lis)	
	
	check_collison()
	text = font.render('You : '+str(score) , 1 , (0,255,255))
	text_2 = font.render('Corona : '+str(score_en) , 1 , (255,100,150))
	wind.blit(text , (400,     30))
	wind.blit(text_2 , (10,30))
	cal_time()
	text_3 = font.render(str(minute)+' : '+str(int(sec)) , 1 , (255,200,200))
	wind.blit(text_3 , (200 , 30))		
	pygame.display.update()
	wind.fill((0,0,0))		
	count+=1

pygame.quit()






