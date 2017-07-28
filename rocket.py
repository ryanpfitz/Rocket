import pygame

class Game:

	def __init__ (self, width, height, fps):
		pygame.init()
		self.windowWidth=width
		self.windowHeight=height
		self.fps=fps
		self.gameSurface = pygame.display.set_mode((width,height))
		self.clock = pygame.time.Clock()


		
	def gameInit(self):
		self.space=Space()
		self.landingPad1=LandingPad()
		self.landingPad1.set_pos(self.windowWidth/3,self.windowHeight-self.landingPad1.padImg.get_height())
		self.landingPad2=LandingPad()
		self.landingPad2.set_pos((self.windowWidth/3)*2,self.windowHeight-self.landingPad1.padImg.get_height())
		self.rocket=Rocket(self.windowWidth/3,self.windowHeight-self.landingPad1.padImg.get_height(),30,2000,-1800)
		self.freeze=False
		self.reset = True
		self.gameTimeElapsed=0.0
		
	def gameLoop(self):
		exit=False
		white=(255,255,255)
		red=(255,0,0)
		green=(0,255,0)
		blue=(135,206,250)
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
						self.gameTimeElapsed=0.0
					elif event.key == pygame.K_RETURN and self.freeze == False and self.rocket.landed == True:
						self.rocket.landReset()
						self.reset=False
						self.gameTimeElapsed=0.0
					elif event.key == pygame.K_r:
						self.rocket.changeRocket()
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
			
			
			if self.rocket.current_y_pos > self.landingPad2.y_pos + 2 and self.rocket.current_y_velocity < 0:
				if self.rocket.current_y_velocity > -60 and abs(self.rocket.current_x_pos - self.landingPad2.x_pos) < 80:
					self.rocket.landed = True
				else:
					self.rocket.crash = True
			
			self.clearWindow()
			self.space.draw(self.gameSurface)
			self.rocket.draw(self.gameSurface)
			self.landingPad1.draw(self.gameSurface)
			self.landingPad2.draw(self.gameSurface)
			
			
			if self.rocket.landed == False and self.rocket.crash == False and self.reset == False:
				self.gameTimeElapsed = self.gameTimeElapsed + elapsedTime
			
			
			timeMessage = str('Time Elapsed: ' + str(int(self.gameTimeElapsed)) + ' sec')
			self.writeText(timeMessage, yellow, 25, self.windowWidth - 200, 60)
			
			if self.rocket.landed:
				self.writeMessage('Nice landing!',green, 30, (self.windowHeight/2))
				self.writeMessage('Press Enter to play again or Q to quit',green, 25, (self.windowHeight/2)+ 40)
				
			elif self.rocket.crash:
				self.writeMessage('You Crashed! Press Enter to play again or Q to quit',red, 25, (self.windowHeight/2))
			elif self.reset:
				self.writeMessage('Welcome to Rocket!', yellow, 40, (self.windowHeight/2)-90)
				self.writeMessage('Your mission:', blue, 30, (self.windowHeight/2))
				self.writeMessage('Launch the rocket and land safely on the other landing pad', blue, 20, (self.windowHeight/2)+30)
				self.writeMessage('You must land gently to avoid crashing!', blue, 20, (self.windowHeight/2)+50)
				self.writeMessage('Use <SPACE> to fire rocket, Left/Right Keys to move side-ways', white, 20, (self.windowHeight/2)+100)
			
			pygame.display.update()
			
		
		pygame.quit()
		
	
	def clearWindow(self):
		self.gameSurface.fill((0,0,0))


		
	def writeMessage(self,message,color, size,y):
		largeFont = pygame.font.SysFont('couriernew',size, True)
		textSurface = largeFont.render(message, True, color)
		textRect = textSurface.get_rect()
		textRect.center = ((self.windowWidth/2),y)
		self.gameSurface.blit(textSurface,textRect)
	
	def writeText(self,string,color,size,x,y):
		font = pygame.font.SysFont('couriernew',size, True)
		textSurface = font.render(string, True, color)
		textRect = textSurface.get_rect()
		textRect.center = (x,y)
		self.gameSurface.blit(textSurface,textRect)
		

class Space:

	def __init__ (self):
		self.starsImg = pygame.image.load('stars.png')
		self.moonImg = pygame.image.load('moon.png')
		self.asteroidImg = pygame.image.load('asteroid1.png')
		
	def draw (self,surface):
		surface.blit(self.moonImg,(surface.get_width()/2-self.moonImg.get_width()/2,surface.get_height()-self.moonImg.get_height()))
		surface.blit(self.starsImg,(0,0))
		surface.blit(self.asteroidImg,(100,100))
		
class Rocket:

	def __init__(self,x_init_pos,y_init_pos,mass,rocketforce,gravityforce):
		self.rocketImg = []
		self.rocketImg.append(pygame.image.load('rocket1.png'))
		self.rocketImg.append(pygame.image.load('rocket2.png'))
		self.rocketImg.append(pygame.image.load('rocket3.png'))
		self.rocketImg.append(pygame.image.load('rocket4.png'))
		self.rocketIndex=0
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
		
	def changeRocket(self):
		self.rocketIndex = self.rocketIndex + 1
		if self.rocketIndex > 3:
			self.rocketIndex=0
		
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
			
		if self.current_x_pos > 800 + self.rocketImg[self.rocketIndex].get_width()/2:
			self.current_x_pos = -1 * self.rocketImg[self.rocketIndex].get_width()
			
		if self.current_x_pos < -1 * self.rocketImg[self.rocketIndex].get_width():
			self.current_x_pos = 800
		
		self.flameCount = self.flameCount+1
		if self.flameCount==3:
			self.flameCount=0
			
		self.thrustCount = self.thrustCount+1
		if self.thrustCount==2:
			self.thrustCount=0
		
		
		
	def draw (self,surface):
		x_draw_pos = self.current_x_pos-self.rocketImg[self.rocketIndex].get_width()/2
		y_draw_pos = self.current_y_pos-self.rocketImg[self.rocketIndex].get_height()

		surface.blit(self.rocketImg[self.rocketIndex],(x_draw_pos,y_draw_pos))
		
		if self.fire:
			surface.blit(self.fireImg[self.flameCount],(x_draw_pos+self.rocketImg[self.rocketIndex].get_width()/2-self.fireImg[self.flameCount].get_width()/2,y_draw_pos+self.rocketImg[self.rocketIndex].get_height()))
			
		if self.rightThrust:
			surface.blit(self.leftThrustImg[self.thrustCount],(x_draw_pos-self.leftThrustImg[self.thrustCount].get_width()+11,y_draw_pos+30))
			
		if self.leftThrust:
			surface.blit(self.rightThrustImg[self.thrustCount],(x_draw_pos+self.rocketImg[self.rocketIndex].get_width()-11,y_draw_pos+30))

			
			

class LandingPad:
	def __init__(self,x=0,y=0):
		self.x_pos=x
		self.y_pos=y
		self.padImg=pygame.image.load('landingPad.png')
		
	def set_pos(self,x,y):
		self.x_pos=x
		self.y_pos=y
		
	def draw (self, surface):
		x_draw_pos = self.x_pos-self.padImg.get_width()/2
		y_draw_pos = self.y_pos
		surface.blit(self.padImg,(x_draw_pos,y_draw_pos))
			

game=Game(800,800,60)
game.gameInit()
game.gameLoop()
quit()


		