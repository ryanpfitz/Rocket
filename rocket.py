import pygame

class Game:

	def __init__ (self, width, height, fps):
		pygame.init()
		self.windowWidth=width
		self.windowHeight=height
		self.fps=fps
		self.rocket=Rocket(self.windowWidth/2,self.windowHeight-40,30,2000,-1800)
		self.space=Space()
		self.freeze=False
		self.gameSurface = pygame.display.set_mode((width,height))
		self.clock = pygame.time.Clock()
		self.reset = True
		print (pygame.font.get_fonts())

	def gameLoop(self):
		exit=False
		white=(255,255,255)
		red=(255,0,0)
		green=(0,255,0)
		yellow=(255,255,0)
		while not exit:
			elapsedTime=self.clock.tick(self.fps)/1000.0
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit=True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and self.freeze == False and self.rocket.crash == False and self.rocket.landed == False:
						self.rocket.startFire()
						self.reset=False
					elif event.key == pygame.K_RETURN and self.freeze == False and self.rocket.crash == True:
						self.rocket.crashReset()
						self.reset=False
					elif event.key == pygame.K_RETURN and self.freeze == False and self.rocket.landed == True:
						self.rocket.landReset()
						self.reset=False
					elif event.key == pygame.K_LEFT and self.freeze == False and self.rocket.landed == False and self.rocket.crash == False:
						self.rocket.thrustLeft()
						self.reset=False
					elif event.key == pygame.K_RIGHT and self.freeze == False and self.rocket.landed == False and self.rocket.crash == False:
						self.rocket.thrustRight()
						self.reset=False
					elif event.key == pygame.K_q:
						exit=True
					elif event.key == pygame.K_p and self.freeze == False:
						self.freeze = True
						self.reset=False
					elif event.key == pygame.K_p and self.freeze == True:
						self.freeze = False
						self.reset = False
				
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						self.rocket.stopFire()
					elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						self.rocket.noThrust()    
			
			if self.freeze == False and self.rocket.crash == False and self.rocket.landed == False:
				self.rocket.update(elapsedTime)
			
			self.clearWindow()
			self.space.draw(self.gameSurface)
			self.rocket.draw(self.gameSurface)
			
			if self.rocket.landed:
				self.writeMessage('Nice landing! Press Enter to reset or Q to quit',green, 25)
			elif self.rocket.crash:
				self.writeMessage('You Crashed! Press Enter to reset or Q to quit',red, 25)
			elif self.reset:
				self.writeMessage('Controls: SPACE to fire rocket, Left/Right Keys to move side-ways', yellow, 20)
			
			pygame.display.update()
			
		
		pygame.quit()
		
	
	def clearWindow(self):
		self.gameSurface.fill((0,0,0))


		
	def writeMessage(self,message,color, size):
		largeFont = pygame.font.SysFont('couriernew',size, True)
		textSurface = largeFont.render(message, True, color)
		textRect = textSurface.get_rect()
		textRect.center = ((self.windowWidth/2),(self.windowHeight/2))
		self.gameSurface.blit(textSurface,textRect)
		

class Space:

	def __init__ (self):
		self.starsImg = pygame.image.load('stars.png')
		self.moonImg = pygame.image.load('moon.png')
		
	def draw (self,surface):
		surface.blit(self.moonImg,(surface.get_width()/2-self.moonImg.get_width()/2,surface.get_height()-self.moonImg.get_height()))
		surface.blit(self.starsImg,(0,0))
		
class Rocket:

	def __init__(self,x_init_pos,y_init_pos,mass,rocketforce,gravityforce):
		self.rocketImg = pygame.image.load('rocket.png')
		self.crashed_rocketImg = pygame.image.load('crashedrocket.png')
		self.fireImg = []
		self.fireImg.append(pygame.image.load('flame1.png'))
		self.fireImg.append(pygame.image.load('flame2.png'))
		self.fireImg.append(pygame.image.load('flame3.png'))
		self.leftThrustImg = []
		self.leftThrustImg.append(pygame.image.load('rightThrust1.png'))
		self.leftThrustImg.append(pygame.image.load('rightThrust2.png'))
		self.rightThrustImg = []
		self.rightThrustImg.append(pygame.image.load('leftThrust1.png'))
		self.rightThrustImg.append(pygame.image.load('leftThrust2.png'))
		self.current_x_pos = self.x_init_pos = x_init_pos
		self.current_y_pos = self.y_init_pos = y_init_pos
		self.current_y_velocity = 0
		self.current_y_accel = 0
		self.current_x_accel = 0
		self.current_x_velocity = 0
		self.current_y_accel = 0
		self.fire=False
		self.crash=False
		self.landed=False
		self.rocketMass=mass
		self.thrustForce=rocketforce
		self.gravityForce=gravityforce
		self.max_y_velocity = 120
		self.flameCount=0
		self.thrustCount=0
		self.leftThrust=False
		self.rightThrust=False
	
	def crashReset(self):
		self.crash=False
		self.current_y_pos = self.y_init_pos
		self.current_y_accel = 0
		self.current_y_velocity = 0
		self.current_x_pos = self.x_init_pos
		self.current_x_velocity =0
		self.current_x_accel = 0
		
	def landReset(self):
		self.landed=False
		self.current_y_pos = self.y_init_pos
		self.current_x_pos = self.x_init_pos
		self.current_y_accel = 0
		self.current_y_velocity = 0
		self.current_x_velocity =0
		self.current_x_accel = 0
	
	def thrustLeft(self):
		self.leftThrust=True
		
	def thrustRight(self):
		self.rightThrust=True
	
	def noThrust(self):
		self.leftThrust=False
		self.rightThrust=False
	
	def startFire(self):
		self.fire=True
		
	def stopFire(self):
		self.fire=False
	

	def update(self,time):
		if self.fire == True and self.crash == False and self.landed == False:
			self.current_y_accel = (self.thrustForce - self.gravityForce) / self.rocketMass
		
		if self.fire == False and self.crash == False and self.landed == False:
			self.current_y_accel = (self.gravityForce) / self.rocketMass
		
		if (self.current_y_accel < 0 and self.current_y_pos == self.y_init_pos) :
			self.current_y_accel = 0
		
		self.current_y_pos = self.current_y_pos - (self.current_y_velocity * time + (self.current_y_accel * time * time) / 2)
		self.current_y_velocity = self.current_y_velocity + self.current_y_accel * time
		
		if self.current_y_velocity > self.max_y_velocity:
			self.current_y_velocity = self.max_y_velocity
	
		if self.y_init_pos - self.current_y_pos < 5 and self.current_y_velocity < 0:	
			if self.current_y_velocity > -60  and abs(self.current_x_pos - self.x_init_pos) < 80:
				self.landed = True
				self.current_y_pos = self.y_init_pos
			else:
				self.crash = True
		
		
			
		thrustForce = 2000

		if self.leftThrust == False and self.rightThrust == False:
			self.current_x_accel = 0
		
		if self.leftThrust == True and self.crash == False and self.landed == False and self.current_y_pos != self.y_init_pos:
			self.current_x_accel = -1 * thrustForce / self.rocketMass

			
		if self.rightThrust == True and self.crash == False and self.landed == False and self.current_y_pos != self.y_init_pos:
			self.current_x_accel = thrustForce / self.rocketMass
		
		self.current_x_pos = self.current_x_pos + (self.current_x_velocity * time + (self.current_x_accel * time * time) / 2)
		self.current_x_velocity = self.current_x_velocity + self.current_x_accel * time
		
		if self.current_x_velocity > 60:
			self.current_x_velocity = 60
			
		if self.current_x_velocity < -60:
			self.current_x_velocity = -60
		
		self.flameCount = self.flameCount+1
		if self.flameCount==3:
			self.flameCount=0
			
		self.thrustCount = self.thrustCount+1
		if self.thrustCount==2:
			self.thrustCount=0
		
		
		
	def draw (self,surface):
		x_draw_pos = self.current_x_pos-self.rocketImg.get_width()/2
		y_draw_pos = self.current_y_pos-self.rocketImg.get_height()
		if self.crash:
			surface.blit(self.crashed_rocketImg,(x_draw_pos,y_draw_pos))
		else:
			surface.blit(self.rocketImg,(x_draw_pos,y_draw_pos))
		
		if self.fire:
			surface.blit(self.fireImg[self.flameCount],(x_draw_pos+self.rocketImg.get_width()/2-self.fireImg[self.flameCount].get_width()/2,y_draw_pos+self.rocketImg.get_height()))
			
		if self.rightThrust:
			surface.blit(self.leftThrustImg[self.thrustCount],(x_draw_pos-self.leftThrustImg[self.thrustCount].get_width()+11,y_draw_pos+30))
			
		if self.leftThrust:
			surface.blit(self.rightThrustImg[self.thrustCount],(x_draw_pos+self.rocketImg.get_width()-11,y_draw_pos+30))
		

game=Game(800,800,60)
game.gameLoop()
quit()


		