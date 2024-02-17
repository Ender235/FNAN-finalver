#Five Nights At Noobs
#Created and produced by Sam Sivorn and Ricardo Rubert

import pygame
import random

#global variables
global gameState
global currentCam
global turningNumber
global camPanelCheck
global staticOpacity
global difficulties
global difficulty
global tickyWickies
global tickyWickies2
global power
global night
global nightTicks
global savedNight
global transitionTicks
global transitionFrame
global activeJumpscare
global winTicks
global starAchieved
global deathTicks
global deathFrame
global confettiFrame
global resolution

#functions for calculating size and position of objects for differing resolutions
def calculate_position(x, y):
    global resolution
    new_x = (x/1920) * resolution[0]
    new_y = (y/1080) * resolution[1]
    return (new_x, new_y)

def calculate_size(size):
    global resolution
    x_length = (size[0]/1920) * resolution[0]
    y_length = (size[1]/1080) * resolution[1]
    return (x_length, y_length)

#variables
activeJumpscare = "None"
night = 0
tickyWickies = [60*4, 60*6]
tickyWickies2 = [60*4, 60*6]
difficulties = [[5, 5, 0, 0], [7, 6, 0, 6], [8, 7, 10, 14], [13, 13, 12, 18], [17, 17, 16, 20], [20, 20, 20, 22]]
difficulty = difficulties[night]
camPanelCheck = 0
staticFrame = 0
turningNumber = -1
currentCam = 0
cameraMoveSpeed = 20
movingPixels = 300
running = True
staticOpacity = 50
power = 2*100999
nightLength = 60*30*6
nightLength = 60*30*7
nightTicks = 0
dataFile = "data (DO NOT MODIFY)/data.txt"
savedNight = 0
transitionTicks = 2*60
transitionFrame = 0
winTicks = 0
deathLength = 200

with open("data (DO NOT MODIFY)/of.txt", "r") as f:
    starAchieved = int(f.readlines()[0][0])


# pygame initalisation
base_resolution = (1920,1080)
gameState = "title"
pygame.init()
gameName = "Five Nights At Noobs"
resolution = pygame.display.Info()
resolution = (resolution.current_w, resolution.current_h)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption(gameName)
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("images/icon.png").convert_alpha())

#check current night in the data file
with open(dataFile, "r") as f:
    savedNight = int(f.readlines()[0][11])

#load the images for each night's ending
winScreenImages = []
for i in range(0,6):
    winScreenImages.append(pygame.transform.scale(pygame.image.load(f"images/win/{i}.png").convert(), calculate_size([1920, 1080])))

#initalise array for confetti frames then append each frame
confettiImages = []
for i in range(0, 81):
    confettiImages.append(pygame.transform.scale(pygame.image.load(f"images/win/confetti/frame_{i}_delay-0.1s.png").convert_alpha(), calculate_size([1920, 1080])))
confettiRect = confettiImages[0].get_rect(center = calculate_position(1920/2, 1080/2))

winScreenRect = winScreenImages[0].get_rect(center = calculate_position(1920/2, 1080/2))
winSound = pygame.mixer.Sound("audio/win.mp3")

sf = 0.4
starImage = pygame.transform.scale(pygame.image.load("images/menu/star.png").convert_alpha(), calculate_size([220*sf, 209*sf]))
starRect = starImage.get_rect(center = calculate_position(1208, 320))

#load call audios
callAudios = []
for i in range(0, 5):
    callAudios.append(pygame.mixer.Sound(f"audio/phone/{i}.wav"))

powerOutSound = pygame.mixer.Sound("audio/soundeffects/powerdown.wav")


#camera static
staticFrames = []

for i in range(0, 8):
    staticFrames.append(pygame.transform.scale(pygame.image.load(f"images/static/{i+1}.png").convert(), calculate_size([1920, 1080])))

staticFrameRect = staticFrames[0].get_rect(center = (calculate_position(1920/2, 1080/2)))

#sets images of static to low opacity
for frame in staticFrames:
    frame.set_alpha(staticOpacity)

deathSound = pygame.mixer.Sound("audio/death.mp3")

#load transition frames
transitionFrames = []
for i in range(0, 10):
    transitionFrames.append(pygame.transform.scale(pygame.image.load(f"images/transition/{i}.png").convert_alpha(), calculate_size([1920, 1080])))
transitionRect = transitionFrames[0].get_rect()

nightTransitionImages = []
for i in range(0, 6):
    nightTransitionImages.append(pygame.transform.scale(pygame.image.load(f"images/transition/night {i}.png").convert(), calculate_size([1920, 1080])))
nightTransitionRect = nightTransitionImages[0].get_rect()

#cameras
sf = 1.4   # scale factor
camOverlayImage = pygame.transform.scale(pygame.image.load("images/cam overlay.png").convert_alpha(), calculate_size([439*sf, 376*sf]))
camOverlayRect = camOverlayImage.get_rect(bottomright = calculate_position(1920, 1080))

camUpSound = pygame.mixer.Sound("audio/soundeffects/camera_down.wav")
camUpSound.set_volume(0.1)


#button images

cam1ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM1/CAM1B.png").convert_alpha(), calculate_size([92, 54]))
cam1ButtonRect = cam1ButtonImage.get_rect(center = calculate_position(1543, 580))
cam2ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM2/CAM2B.png").convert_alpha(), calculate_size([92, 54]))
cam2ButtonRect = cam2ButtonImage.get_rect(center = calculate_position(1512, 664))
cam3ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM3/CAM3B.png").convert(), calculate_size([92, 54]))
cam3ButtonRect = cam3ButtonImage.get_rect(center = calculate_position(1463, 786))
cam4ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM4/CAM4B.png").convert(), calculate_size([92,54]))
cam4ButtonRect = cam4ButtonImage.get_rect(center = calculate_position(1350, 708))
cam5ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM5/CAM5B.png").convert(), calculate_size([92, 54]))
cam5ButtonRect = cam5ButtonImage.get_rect(center = calculate_position(1870, 708))
cam6ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM6/CAM6B.png").convert(), calculate_size([92, 54]))
cam6ButtonRect = cam6ButtonImage.get_rect(center = calculate_position(1542, 963))
cam7ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM7/CAM7B.png").convert(), calculate_size([92, 54]))
cam7ButtonRect = cam6ButtonImage.get_rect(center = calculate_position(1410, 936))
cam8ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM8/CAM8B.png").convert(), calculate_size([92, 54]))
cam8ButtonRect = cam8ButtonImage.get_rect(center = calculate_position(1542, 1024))
cam9ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM9/CAM9B.png").convert(), calculate_size([92, 54]))
cam9ButtonRect = cam9ButtonImage.get_rect(center = calculate_position(1707, 964))
cam10ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM10/CAM10B.png").convert(), calculate_size([92, 54]))
cam10ButtonRect = cam10ButtonImage.get_rect(center = calculate_position(1707, 1028))
cam11ButtonImage = pygame.transform.scale(pygame.image.load("images/camera/CAM11/CAM11B.png").convert(), calculate_size([92, 54]))
cam11ButtonRect = cam11ButtonImage.get_rect(center = calculate_position(1856, 912))

#death screen
deathScreenImages = []
for i in range(0, 33):
    deathScreenImages.append(pygame.transform.scale(pygame.image.load(f"images/death/{i}.png"), calculate_size([1920, 1080])))
deathScreenRect = deathScreenImages[0].get_rect(center = calculate_position(1920/2, 1080/2))

#camera arrays
cam1Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM1/0.png").convert(), calculate_size([2560, 1080])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM1/1.png").convert(), calculate_size([2560, 1080])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM1/2.png").convert(), calculate_size([2560, 1080])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM1/3.png").convert(), calculate_size([2560, 1080]))

]
cam1Image = cam1Images[3]
cam1Rect = cam1Image.get_rect(center = calculate_position(2560/2, 1080/2))

cam2Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM2/0.png").convert(), calculate_size([2560, 1080])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM2/1.png").convert_alpha(), calculate_size([2560, 1080])),
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM2/3.png").convert(), calculate_size([2560, 1080]))
]
cam2Image = cam2Images[3]
cam2Rect = cam2Image.get_rect(center = calculate_position(2560/2, 1080/2))

cam3Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM3/0.png").convert(), calculate_size([2560, 1920])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM3/1.png").convert(), calculate_size([2560, 1920])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM3/1.png").convert(), calculate_size([2560, 1920])),
    pygame.transform.scale(pygame.image.load("images/camera/CAM3/3.png").convert(), calculate_size([2560, 1920])),
]
cam3Image = pygame.transform.scale(pygame.image.load("images/camera/CAM3/0.png").convert(), calculate_size([2560, 1080]))
cam3Rect = cam3Image.get_rect(center = calculate_position(2560/2, 1080/2))

cam4Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM4/0.png").convert(), calculate_size([2560, 1080])),
    None,
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM4/3.png").convert(), calculate_size([2560, 1080]))
]
cam4Image = cam4Images[3]
cam4Rect = cam4Image.get_rect(center = calculate_position(2560/2, 1080/2))

cam5Images = [
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM5/1.png").convert(), calculate_size([2560, 1080])),
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM5/3.png").convert(), calculate_size([2560, 1080]))
]
cam5Image = cam5Images[3]
cam5Rect = cam5Image.get_rect(center = calculate_position(2560/2, 1080/2))


cam6Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM6/0.png").convert(), calculate_size([2560, 1080])),
    None,
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM6/3.png").convert(), calculate_size([2560, 1080]))
]
cam6Image = cam6Images[3]
cam6Rect = cam6Image.get_rect(center = calculate_position(2560/2, 1080/2))


cam7Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM7/0.png").convert(), calculate_size([2560, 1080])),
    None,
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM7/3.png").convert(), calculate_size([2560, 1080]))
]
cam7Image = cam7Images[3]
cam7Rect = cam6Image.get_rect(center = calculate_position(2560/2, 1080/2))


cam8Images = [
    pygame.transform.scale(pygame.image.load("images/camera/CAM8/0.png").convert(), calculate_size([2560, 1080])),
    None,
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM8/3.png").convert(), calculate_size([2560, 1080]))
]
cam8Image = cam8Images[3]
cam8Rect = cam8Image.get_rect(center = calculate_position(2560/2, 1080/2))


cam9Images = [
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM9/1.png").convert(), calculate_size([2560, 1080])),
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM9/3.png").convert(), calculate_size([2560, 1080]))
]
cam9Image = cam9Images[3]
cam9Rect = cam9Image.get_rect(center = calculate_position(2560/2, 1080/2))


cam10Images = [
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM10/1.png").convert(), calculate_size([2560, 1080])),
    None,
    pygame.transform.scale(pygame.image.load("images/camera/CAM10/3.png").convert(), calculate_size([2560, 1080]))
]
cam10Image = cam10Images[3]
cam10Rect = cam10Image.get_rect(center = calculate_position(2560/2, 1080/2))

cam11Image = pygame.transform.scale(pygame.image.load("images/camera/CAM11/0.png").convert(), calculate_size([2560, 1080]))
cam11Rect = cam11Image.get_rect(center = calculate_position(1920/2, 1080/2))

#camera panel
camPanelImage = pygame.transform.scale(pygame.image.load("images/camera pannel.png").convert_alpha(), calculate_size([550, 150]))
camPanelRect = camPanelImage.get_rect(center = calculate_position(1920/2, 1000))
camPanelImage.set_alpha(100)
camChangeSound = pygame.mixer.Sound("audio/soundeffects/camera_change.wav")
camChangeSound.set_volume(0.5)

#title screen
titleImage = pygame.transform.scale(pygame.image.load("images/title.png").convert(), calculate_size([1920, 1080]))
nightmareTitleImage = pygame.transform.scale(pygame.image.load("images/title_nightmare.png").convert(), calculate_size([1920, 1080]))
titleImageRect = titleImage.get_rect(center = calculate_position(1920/2, 1080/2))

newGameImage = pygame.transform.scale(pygame.image.load("images/menu/newgame.png").convert(), calculate_size([488, 133]))
newGameRect = newGameImage.get_rect(center = calculate_position(970, 461))

continueImage = pygame.transform.scale(pygame.image.load("images/menu/continue.png").convert(), calculate_size([492, 106]))
continueRect = continueImage.get_rect(center = calculate_position(973, 566))

nightmareImage = pygame.transform.scale(pygame.image.load("images/menu/custom.png").convert(), calculate_size([376, 109]))
nightmareRect = nightmareImage.get_rect(center =  calculate_position(920, 666))
menuMusic = pygame.mixer.Sound("audio/music/main_menu.wav")

#office
office_image = pygame.transform.scale(pygame.image.load("images/office/office.png").convert(), calculate_size([2560,1080]))
office_rect = office_image.get_rect(center = calculate_position(2560/2,1080/2))

litUpLeftDoorImage = pygame.transform.scale(pygame.image.load("images/office/litupleftdoor.png").convert_alpha(), calculate_size([2560, 1080]))
litUpRightDoorImage = pygame.transform.scale(pygame.image.load("images/office/lituprightdoor.png").convert_alpha(), calculate_size([2560, 1080]))
officeAmbiance = pygame.mixer.Sound("audio/soundeffects/fan.wav")
officeAmbiance.set_volume(0.05)

#office buttons

lLightButtonImage = pygame.transform.scale(pygame.image.load("images/office/leftlightbutton.png").convert_alpha(), calculate_size([106, 136]))
lLightButtonRect = lLightButtonImage.get_rect(center = calculate_position(83, 677))
lDoorButtonImage = pygame.transform.scale(pygame.image.load("images/office/leftdoorbutton.png").convert_alpha(), calculate_size([105, 139]))
lDoorButtonRect = lDoorButtonImage.get_rect(center = calculate_position(83, 494))

rLightButtonImage = pygame.transform.scale(pygame.image.load("images/office/rightlightbutton.png").convert_alpha(), calculate_size([103, 134]))
rLightButtonRect = rLightButtonImage.get_rect(center = calculate_position(2495, 677))
rDoorButtonImage = pygame.transform.scale(pygame.image.load("images/office/rightdoorbutton.png").convert_alpha(), calculate_size([105, 137]))
rDoorButtonRect = rDoorButtonImage.get_rect(center = calculate_position(2495, 493))

atDoorLeftImage = pygame.transform.scale(pygame.image.load("images/office/atleftdoor.png").convert_alpha(), calculate_size([2560, 1080]))
atDoorRightImage = pygame.transform.scale(pygame.image.load("images/office/atrightdoor.png").convert_alpha(), calculate_size([2560, 1080]))

leftDoorImages = [litUpLeftDoorImage, atDoorLeftImage]
rightDoorImages = [litUpRightDoorImage, atDoorRightImage]

doorHitSound = pygame.mixer.Sound("audio/doorhit.mp3")

#office rect list

sf = 2.3
blackoutImage = pygame.transform.scale(pygame.image.load("images/office/blackout.png").convert(), calculate_size([2560, 1080]))
officeRects = [office_rect, lLightButtonRect, lDoorButtonRect, rLightButtonRect, rDoorButtonRect]
powerLeftImage = pygame.transform.scale(pygame.image.load("images/power/powerleft.png").convert_alpha(), calculate_size([137*sf, 14*sf]))   #137 14
powerLeftRect = powerLeftImage.get_rect(center = calculate_position(233, 905))

powerImages = []
for num in range(0,10):
    powerImages.append(pygame.transform.scale(pygame.image.load(f"images/power/{num}.png").convert_alpha(), calculate_size([19*2, 23*2])))

sf = 3
timeImages = []
for i in range(0, 7):
    timeImages.append(pygame.transform.scale(powerImages[i], calculate_size([19*sf, 23*sf])))


sf = 1.5
nightImage = pygame.transform.scale(pygame.image.load("images/time/night.png").convert_alpha(), calculate_size([130*sf ,34*sf]))

nightRect = nightImage.get_rect(center = calculate_position(1689, 147))

sf = 2.3
nightNumImages = []
for i in range(1, 7):
    nightNumImages.append(pygame.transform.scale(powerImages[i], calculate_size([19*sf, 23*sf])))

nightNumRect = nightNumImages[0].get_rect(center = calculate_position(1839, 152))

powerRects = [
    powerImages[0].get_rect(center = calculate_position(429, 907)),
    powerImages[0].get_rect(center = calculate_position(472, 907)),
    powerImages[0].get_rect(center = calculate_position(514, 907))
]

timeRect = timeImages[0].get_rect(center = calculate_position(1749, 60))

sf = 2
amImage = pygame.transform.scale(pygame.image.load("images/time/am.png").convert_alpha(), calculate_size([42*sf, 26*sf]))
amRect = amImage.get_rect(center = calculate_position(1831, 61))

#door anim
leftDoorAnimationFrames = []
for i in range(0, 26):
    leftDoorAnimationFrames.append(pygame.transform.scale(pygame.image.load(f"images/office/leftdoor/{i}.png").convert_alpha(), calculate_size([2560, 1080])))

rightDoorAnimationFrames = []
for i in range(0, 26):
    rightDoorAnimationFrames.append(pygame.transform.scale(pygame.image.load(f"images/office/rightdoor/{i}.png").convert_alpha(), calculate_size([2560, 1080])))

endingImages = [
    pygame.transform.scale(pygame.image.load("images/endings/0.png").convert(), calculate_size([1920, 1080])),
    pygame.transform.scale(pygame.image.load("images/endings/1.png").convert(), calculate_size([1920, 1080]))
]
endingRect = endingImages[0].get_rect(center = calculate_position(1920/2, 1080/2))
endingMusic = [pygame.mixer.Sound("audio/ending.mp3"), pygame.mixer.Sound("audio/ending1.mp3")]

#jumpscare class
class Jumpscare():
    def __init__(self, num, images, rect):
        self.num = num
        self.images = images
        self.rect = rect
        self.animationFrame = 0
        self.ticks = 0
        self.waitTicks = 10
        self.sound = pygame.mixer.Sound(f"audio/jumpscares/{num}.mp3")
        self.soundPlaying = False
    
    #ran each frame that the jumpscare animation is playing
    def display(self):
        if not self.soundPlaying:
            self.sound.play()
            self.soundPlaying = True
        self.waitTicks -= 1
        screen.blit(self.images[self.animationFrame], self.rect)
        self.ticks += 1
        if self.animationFrame != 4 and self.waitTicks <= 0:
            self.animationFrame += 1
        if self.ticks >= 50:
            self.sound.stop()
            return True
        return False

# door class 

class Door():
    def __init__(self, num, litUpDoorImage, closedDoorImages, doorLightButtonImage, doorLightButtonRect, doorButtonImage, doorButtonRect, lightOn, doorOn):
        self.num = num
        self.litUpDoorImage = litUpDoorImage
        self.closedDoorImages = closedDoorImages
        self.doorLightButtonImage = doorLightButtonImage
        self.doorLightButtonRect = doorLightButtonRect
        self.doorButtonImage = doorButtonImage
        self.doorButtonRect = doorButtonRect
        self.lightOn = lightOn
        self.doorOn = doorOn
        self.tickAmount = 20
        self.animationFrame = 25
        self.lightTicks = self.tickAmount
        self.doorTicks = self.tickAmount

        self.lightSound = pygame.mixer.Sound("audio/soundeffects/light_on.wav")
        self.lightSound.set_volume(0.2)
        self.lightSoundOn = False

        self.doorSound = pygame.mixer.Sound("audio/soundeffects/door_open.wav")
        self.doorSound.set_volume(0.2)
        self.doorSoundOn = False

        self.doorSound2 = pygame.mixer.Sound("audio/soundeffects/door_open.wav")
        self.doorSound2.set_volume(0.2)
        self.doorSound2On = True
    
    def update(self):
        #run each frame
        global power
        mPos = pygame.mouse.get_pos()
        self.power = power
        self.lightTicks -= 1
        self.doorTicks -= 1

        self.lightSound.set_volume(0.2)
        self.doorSound.set_volume(0.2)
        self.doorSound2.set_volume(0.2)

        #checks if door button is pressed
        if mPos[0] >= self.doorButtonRect.left and mPos[0] <= self.doorButtonRect.right:
            if mPos[1] <= self.doorButtonRect.bottom and mPos[1] >= self.doorButtonRect.top:
                if pygame.mouse.get_pressed()[0] and self.doorTicks <= 0:
                    self.doorOn = not self.doorOn
                    self.doorTicks = self.tickAmount

        #checks if light button is pressed
        if mPos[0] >= self.doorLightButtonRect.left and mPos[0] <= self.doorLightButtonRect.right:
            if mPos[1] <= self.doorLightButtonRect.bottom and mPos[1] >= self.doorLightButtonRect.top:
                if pygame.mouse.get_pressed()[0] and self.lightTicks <= 0:
                    self.lightOn = not self.lightOn
                    self.lightTicks = self.tickAmount

        if self.lightOn:
            power -= 10 * (0.85)
            screen.blit(self.doorLightButtonImage, self.doorLightButtonRect)
            screen.blit(self.litUpDoorImage[basicChars[self.num].atDoor], office_rect)

        
        if self.doorOn:
            power -= 10 * (0.85)
            screen.blit(self.doorButtonImage, self.doorButtonRect)
            
        if self.animationFrame != 25:
            screen.blit(self.closedDoorImages[self.animationFrame], office_rect)

    def updateOnCams(self):
        #ran each frame that the player is in the cameras
        self.lightSound.set_volume(0)
        self.doorSound.set_volume(0)
        self.doorSound2.set_volume(0)
        global power
        if self.lightOn:
            power -= 10 * 0.85
        if self.doorOn:
            power -= 10 * 0.85

    def updateOffCams(self):
        #ran each frame that the player is in the office (not in cams)
        if self.lightOn:
            if not self.lightSoundOn:
                self.lightSoundOn = True
                self.lightSound.play(-1)
        else:
            self.lightSoundOn = False
            self.lightSound.stop()

        if self.doorOn:
            if not self.doorSoundOn:
                self.doorSoundOn = True
                self.doorSound.play()
            self.doorSound2.stop()
            self.doorSound2On = False
        else:
            if not self.doorSound2On:
                self.doorSound2On = True
                self.doorSound2.play()
            self.doorSoundOn = False
            self.doorSound.stop()
        
    def updateAnimation(self):
        #ran each frame to update the current animation state of the door
        if self.doorOn:
            if self.animationFrame != 0:
                self.animationFrame -= 1
        else:
            if self.animationFrame != 25:
                self.animationFrame += 1

#door instances
doors = [
    Door(0, leftDoorImages, leftDoorAnimationFrames, lLightButtonImage, lLightButtonRect, lDoorButtonImage, lDoorButtonRect, False, False),
    Door(1, rightDoorImages, rightDoorAnimationFrames, rLightButtonImage, rLightButtonRect, rDoorButtonImage, rDoorButtonRect, False, False)
]

# class for basic stage character
class BasicChar():
    def __init__(self, location, movementArray, number, atDoor):
        self.location = location
        self.movementArray = movementArray
        self.number = number
        self.atDoor = atDoor
    
        

    def printLocation(self):
        print(self.location)

    def canMove(self):
        rand = random.randint(0, 20)
        if rand < difficulty[self.number]:
            return True
        return False

class Droos():
    def __init__(self):
        self.sound = pygame.mixer.Sound("audio/eating.mp3")
        self.sound.play(-1)
        self.sound.set_volume(0)
        self.noFood = False
        self.ticks = 0
        self.difficulty = 20
        self.buttonImage = pygame.transform.scale(pygame.image.load("images/foodButton.png").convert(), calculate_size([276, 162]))
        self.buttonRect = self.buttonImage.get_rect()
        self.buttonActive = False
        self.buttonLocation = 0

    def update(self):
        global activeJumpscare
        self.ticks += (self.difficulty) / 20
        if self.ticks >= 500 and self.ticks < 2000:
            self.noFood = True
        elif self.ticks >= 2000:
            activeJumpscare = 3
            changeState("jumpscare")
            self.sound.set_volume(0)


        #eating sounds
        if currentCam == 10 and gameState == "cams" and not self.noFood:
            self.sound.set_volume(0.5)
        else:
            self.sound.set_volume(0)

    def button(self):
        mPos = pygame.mouse.get_pos()

        if self.noFood:

            #if the button hasnt already been generated, generate it and place it in a random camera in a random positon on the screen
            if not self.buttonActive:
                self.buttonRect.center = calculate_position(random.randint(0, 1920), random.randint(0, 1080))
                self.buttonLocation = random.randint(0, 10)
                self.buttonActive = True
            
            #show the order food button if the player is on the correct camera
            if currentCam == self.buttonLocation:
                screen.blit(self.buttonImage, self.buttonRect)
                if mPos[0] >= self.buttonRect.left and mPos[0] <= self.buttonRect.right:
                    if mPos[1] <= self.buttonRect.bottom and mPos[1] >= self.buttonRect.top:
                        if pygame.mouse.get_pressed()[0]:
                            self.buttonActive = False
                            self.noFood = False
                            self.ticks = 0
                            self.sound.set_volume(0.5)


droos = Droos()

class Ender():
    def __init__(self, images, rect):
        self.images = images
        self.rect = rect
        self.state = 0
        self.baseTicks = 2000
        self.ticks = 0
        self.difficulty = 0

    #display ender on the camera according to his current state
    def display(self):
        if currentCam == 2:
            cams[2].image = self.images[self.state]

    #ran every frame
    def update(self):
        #change ender's state according to his current ticks
        global activeJumpscare
        self.ticks += (self.difficulty) / 20
        if self.ticks <= 500:
            self.state = 0
        elif self.ticks <= 1000:
            self.state = 1
        elif self.ticks <= 1500:
            self.state = 2
        elif self.ticks <= 2000:
            self.state = 3

        #if ticks reach threshold, attack the player
        if self.ticks >= self.baseTicks:
            if doors[0].doorOn:
                self.ticks = 0
                doorHitSound.play()
            else:
                activeJumpscare = 2
                changeState("jumpscare")
    
    #ran every frame the player is on the cameras (increases rate of aggression if past a certain state)
    def updateOffice(self):
        global activeJumpscare
        if self.state == 3:
            self.ticks += (self.difficulty) / 20
        else:
            self.ticks += ((self.difficulty / 20) / 3)
        if self.ticks >= self.baseTicks:
            if doors[0].doorOn:
                self.ticks = 0
            else:
                activeJumpscare = 2
                changeState("jumpscare")


#load images of ender's states
enderImages = []
for i in range(0, 4):
    enderImages.append(pygame.transform.scale(pygame.image.load(f"images/camera/CAM3/{i}.png").convert(), calculate_size([2560, 1080])))
enderRect = enderImages[0].get_rect()

ender = Ender(enderImages, enderRect)

# Camera class
class Camera():
    def __init__(self, image, rect, buttonImage, buttonRect, number, num):
        self.image = image
        self.buttonImage = buttonImage
        self.rect = rect
        self.buttonRect = buttonRect
        self.number = number
        self.num = num

    #ran every frame that player is on cameras
    def checkClicked(self):
        global currentCam
        mPos = pygame.mouse.get_pos()
        if mPos[0] >= self.buttonRect.left and mPos[0] <= self.buttonRect.right:
            if mPos[1] >= self.buttonRect.top and mPos[1] <= self.buttonRect.bottom:
                if pygame.mouse.get_pressed()[0]:
                    if self.num != currentCam:
                        camChangeSound.play()
                        return True
        return False
    

    def print(self):

        screen.blit(self.image, self.rect)

    def displayButton(self):
        screen.blit(self.buttonImage, self.buttonRect)

    def move(self, x, y):
        self.rect.topleft = (x,y)

    def getPos(self):
        return self.rect.topleft


#load jumpscare images
jumpscareImages = [[], [], [], []]
for i in range(0, 5):
    jumpscareImages[0].append(pygame.transform.scale(pygame.image.load(f"images/jumpscares/0/{i}.png").convert_alpha(), calculate_size([1920, 1080])))
    jumpscareImages[1].append(pygame.transform.scale(pygame.image.load(f"images/jumpscares/1/{i}.png").convert_alpha(), calculate_size([1920, 1080])))
    jumpscareImages[2].append(pygame.transform.scale(pygame.image.load(f"images/jumpscares/2/{i}.png").convert_alpha(), calculate_size([2560, 1080])))
    jumpscareImages[3].append(pygame.transform.scale(pygame.image.load(f"images/jumpscares/3/{i}.png").convert_alpha(), calculate_size([1920, 1080])))


jumpscareRect = jumpscareImages[0][0].get_rect()

#create array of jumpscares
jumpscares = [Jumpscare(0, jumpscareImages[0], jumpscareRect),
              Jumpscare(1, jumpscareImages[1], jumpscareRect),
              Jumpscare(2, jumpscareImages[2], office_rect),
              Jumpscare(3, jumpscareImages[3], jumpscareRect)]


# changes the state of the game
def changeState(x):
    global gameState
    gameState = x



#check if camera panel was clicked
def checkClickCamera():
    global camPanelCheck
    pos = pygame.mouse.get_pos()
    if pos[0] >= camPanelRect.left and pos[0] <= camPanelRect.right:
        if pos[1] >= camPanelRect.top and pos[1] <= camPanelRect.bottom:
            if camPanelCheck == 0:
                camPanelCheck = 1
                camUpSound.play()
                return True
            else:
                return False
    camPanelCheck = 0
    return False


#ran every frame to check if basic stage characters can move
def characterMovement(num, char):
    global activeJumpscare
    returnVal = None
    global tickyWickies
    tickyWickies[num] -= 1
    if activeJumpscare == "None":
        if tickyWickies[num] <= 0:
            if char.canMove():
                returnVal = [char.location, None]
                if not char.atDoor:
                    if char.location == 7 or char.location == 9:
                        char.atDoor = True
                        char.location = -1
                        returnVal[1] = -1
                    else:
                        char.location = random.choice(char.movementArray[char.location])
                        returnVal[1] = char.location
                else:
                    if doors[num].doorOn:
                        char.atDoor = False
                        char.location = 1
                        returnVal[1] = char.location
                    else:
                        char.location = -1
                        returnVal[1] = char.location
                        if activeJumpscare == "None":
                            activeJumpscare = num
                        char.atDoor = False
                        if gameState == "blackout":
                            changeState("jumpscare")
            tickyWickies[num] = tickyWickies2[num]
    
    else:
        if gameState == "blackout":
            changeState("jumpscare")

    return returnVal


#updates the power text on UI
def updatePower():
    global power
    if int(power/(2*1000)) <= 0:
        return True

    displayPower = str(int(power / (2*1000)))

    for i in range(len(displayPower)):
        num = int(displayPower[i])
        screen.blit(powerImages[num], powerRects[i])

    screen.blit(powerLeftImage, powerLeftRect)
    

# ran at the start of a new night to set character difficulties and reset any character states
def loadNight(num):
    global night
    global difficulty
    global nightTicks
    global power
    global activeJumpscare
    global staticFrames
    global tickyWickies
    global activeJumpscare
    global winTicks
    global deathTicks
    global deathFrame
    global confettiFrame 
    
    winTicks = 500
    deathFrame = 0
    deathTicks = deathLength
    confettiFrame = 0

    for frame in staticFrames:
        frame.set_alpha(50)
    activeJumpscare = "None"
    power = 2*100999
    nightTicks = 0
    night = num
    difficulty = difficulties[num]

    #sets ender to his base state
    ender.difficulty = difficulties[night][2]
    ender.state = 0
    ender.ticks = 0

    for i,v in enumerate(tickyWickies2):
        tickyWickies[i] = v


    #sets droos to his base state
    droos.difficulty = difficulties[night][3]
    droos.ticks = 0
    droos.noFood = False
    droos.buttonActive = False

    #resets doors to original state
    for door in doors:
        door.doorOn = False
        door.doorSoundOn = False
        door.doorSound2On = True
        door.lightOn = False
        door.lightSoundOn = False
        door.animationFrame = 25

    #moves characters to the stage if they are not already there
    for char in basicChars:
        char.atDoor = False
        char.location = 0

    #resets frame and ticks for each jumpscare
    for j in jumpscares:
        j.animationFrame = 0
        j.ticks = 0
        j.soundPlaying = False
    activeJumpscare = "None"
    
#displays the time overlay
def showTime():
    mPos = pygame.mouse.get_pos()
    global nightTicks
    n = (nightLength/6)
    displayTime = int(nightTicks / (n))
    screen.blit(timeImages[displayTime], timeRect)

    screen.blit(amImage, amRect)
    screen.blit(nightImage, nightRect)
    screen.blit(nightNumImages[night], nightNumRect)

menuRects = [newGameRect, continueRect, nightmareRect]

#ran each frame in the menu to check wether a button is pressed and loads correct night accordingly
def menuButtonsFunc():
    global transitionTicks
    global transitionFrame
    global starAchieved
    global savedNight

    mPos = pygame.mouse.get_pos()
    if savedNight > 4:
        screen.blit(nightmareTitleImage, titleImageRect)
    else:
        screen.blit(titleImage, titleImageRect)
    
    if starAchieved:
        screen.blit(starImage, starRect)
    for i,rect in enumerate(menuRects):
        if mPos[0] >= rect.left and mPos[0] <= rect.right:
            if mPos[1] <= rect.bottom and mPos[1] >= rect.top:
                if pygame.mouse.get_pressed()[0]:
                    if i == 0:
                        loadNight(0)
                        savedNight = 0
                        starAchieved = 0
                        with open("data (DO NOT MODIFY)/of.txt", "w") as f:
                            f.write("0")
                        with open(dataFile, "w") as f:
                            f.write(f"73561463237{0}")
                        menuMusic.stop()
                        camChangeSound.play()
                        changeState("transition")
                        transitionTicks = 2*60
                        transitionFrame = 0 
                    elif i == 1:
                        if savedNight > 4:
                            loadNight(4)
                        else:
                            loadNight(savedNight)
                        menuMusic.stop()
                        camChangeSound.play()
                        changeState("transition")
                        transitionTicks = 2*60
                        transitionFrame = 0 
                    elif i == 2 and savedNight > 4:
                        loadNight(5)
                        menuMusic.stop()
                        camChangeSound.play()
                        changeState("transition")
                        transitionTicks = 2*60
                        transitionFrame = 0 
                    
                    



# updates game according to current state
def stateUpdate():
    global currentCam
    global turningNumber
    global staticFrame
    global staticOpacity
    global power
    global nightTicks
    global savedNight
    global transitionTicks
    global transitionFrame
    global winTicks
    global starAchieved
    global deathTicks
    global deathFrame
    global confettiFrame
    global activeJumpscare

    #if the state is office
    if gameState == "office":
        droos.update()
        ender.updateOffice()
        nightTicks += 1
        power -= 5 * 0.85

        screen.blit(office_image, office_rect)
        screen.blit(camPanelImage, camPanelRect)
        characterMovement(1, basicChars[1])
        characterMovement(0, basicChars[0])

        for door in doors:
            door.updateAnimation()
            door.update()
            door.updateOffCams()

        #office panning calculations (use this for cam panning too)
        scaled_office_r_bound = calculate_position(0, 1920)[1]

        if pygame.mouse.get_pos()[0] <= movingPixels and office_rect.left < 0:
            for rect in officeRects:
                rect.x += cameraMoveSpeed

        if pygame.mouse.get_pos()[0] >= scaled_office_r_bound - movingPixels and office_rect.right > scaled_office_r_bound:
            for rect in officeRects:
                rect.x -= cameraMoveSpeed
        
        if nightTicks == nightLength:
            changeState("win")
            winSound.play()

        #camera click detection
        if checkClickCamera():
            changeState("cams")
        
        if updatePower():
            powerOutSound.play()
            changeState("blackout")

        showTime()

    #if the state is title
    elif gameState == "title":        
        if staticFrame == 7:
            staticFrame = -1
        staticFrame += 1

        for frame in staticFrames:
            frame.set_alpha(20)
        
        menuButtonsFunc()
        screen.blit(staticFrames[staticFrame], staticFrameRect)

    #if the state is cams
    elif gameState == "cams":
        droos.update()
        ender.update()
        nightTicks += 1
        power -= 5 * 0.85

        if nightTicks == nightLength:
            changeState("win")
            winSound.play()
        
        for door in doors:
            door.updateAnimation()
            door.updateOnCams()

        power -= 5 * 0.85

        
        for i in range(len(basicChars)):
            locations = characterMovement(i, basicChars[i])
            if locations:
                for loc in locations:
                    if loc == currentCam:
                        staticOpacity = 250

        #render the camera and all the camera buttons
        currentPos = cams[currentCam].getPos()
        cams[currentCam].print()
        ender.display()
        

        for i,char in enumerate(basicChars):
            if char.location == currentCam:
                screen.blit(camImages[currentCam][i], cams[currentCam].rect)
            
        if currentCam == 0 and basicChars[0].location == 0 and basicChars[1].location == 0:
            screen.blit(cam1Images[2], cam1Rect)

        #camera static handling
        if staticFrame == 7:
            staticFrame = -1
        staticFrame += 1

        if staticOpacity > 50:
            staticOpacity -= 10
            for frame in staticFrames:
                frame.set_alpha(staticOpacity)

        
        screen.blit(staticFrames[staticFrame], staticFrameRect)
        droos.button()
        screen.blit(camOverlayImage, camOverlayRect)
        screen.blit(camPanelImage, camPanelRect)



        #camera pan code
        scaled_camera_r_bound = calculate_position(0, 1920)[1]

        if currentCam != 11:
            if turningNumber == -1:
                cams[currentCam].move(currentPos[0] - 2, currentPos[1])
                if cams[currentCam].rect.right <= scaled_camera_r_bound:
                    turningNumber = 1

            if turningNumber == 1:
                cams[currentCam].move(currentPos[0] + 2, currentPos[1])
                if cams[currentCam].rect.left >= 0:
                    turningNumber = -1
        


        for i,cam in enumerate(cams):
            cam.displayButton()
            if cam.checkClicked():
                staticOpacity = 200
                currentCam = i

        showTime()

        #camera click detection
        if checkClickCamera():
            changeState("office")
            if activeJumpscare != "None":
                changeState("jumpscare")
        
        if updatePower():
            changeState("blackout")
    
    #if the game state is blackout
    elif gameState == "blackout":
        nightTicks += 1
        if night != 5:
            callAudios[night].stop()
        officeAmbiance.stop()
        for door in doors:
            door.doorOn = False
            door.doorSound.stop()
            door.doorSound2.stop()
            door.doorSoundOn = False
            door.doorSound2On = False
            door.lightSound.stop()
            door.lightSoundOn = False
        for i,char in enumerate(basicChars):
            characterMovement(i, char)
        droos.update()
        ender.update()

        sag = calculate_position(0, 1920)

        if pygame.mouse.get_pos()[0] <= movingPixels and office_rect.left < 0:
            for rect in officeRects:
                rect.x += cameraMoveSpeed

        if pygame.mouse.get_pos()[0] >= sag[1] - movingPixels and office_rect.right > sag[1]:
            for rect in officeRects:
                rect.x -= cameraMoveSpeed
        screen.blit(blackoutImage, office_rect)

        if nightTicks == nightLength:
            changeState("win")
            winSound.play()

    #if game state is transition
    elif gameState == "transition":
        screen.blit(nightTransitionImages[night], nightTransitionRect)
        transitionTicks -= 1
        if transitionFrame < len(transitionFrames):
            screen.blit(transitionFrames[transitionFrame], transitionRect)
        if transitionTicks <= 0:
            officeAmbiance.play(-1)
            if night != 5:
                callAudios[night].play()
            changeState("office")
        transitionFrame += 1


    #if gamestate is jumpscare
    elif gameState == "jumpscare":
        if night != 5:
            callAudios[night].stop()
        powerOutSound.stop()
        for door in doors:
            
            door.lightSoundOn = False
            door.lightSound.stop()
            door.doorSoundOn = False
            door.doorSound.stop()
            door.doorSound2On = False
            door.doorSound2.stop()
        if night != 5:
            callAudios[night].stop()
        officeAmbiance.stop()
        if power:
            screen.blit(office_image, office_rect)
        else:
            screen.blit(blackoutImage, office_image)
        if jumpscares[activeJumpscare].display():
            changeState("death")
            deathSound.play()
        showTime()

    #if the state is death
    elif gameState == "death":
        deathTicks -= 1
        deathFrame += 1

        if deathFrame >= 33:
            deathFrame = 0
        
        if deathTicks <= 0 :
            deathSound.stop()
            menuMusic.play(-1)
            changeState("title")
        screen.blit(deathScreenImages[deathFrame], deathScreenRect)
    

    #if the state is win
    elif gameState == "win":
        if night != 5:
            callAudios[night].stop()

        for door in doors:
            door.doorSound.stop()
            door.doorSound2.stop()
            door.doorSoundOn = False
            door.doorSound2On = False
            door.lightSound.stop()
            door.lightSoundOn = False

        droos.sound.set_volume(0)
        confettiFrame += 1
        powerOutSound.stop()
        officeAmbiance.stop()
        winTicks -= 1
        if confettiFrame == 80:
            confettiFrame = 0
        screen.blit(winScreenImages[night], winScreenRect)
        screen.blit(confettiImages[confettiFrame], confettiRect)
        if winTicks <= 0:
            if night == 5:
                starAchieved = 1
                with open("data (DO NOT MODIFY)/of.txt", "w") as f:
                    f.write("1")
            winSound.stop()
            if night <= 4:
                savedNight = night + 1
                with open(dataFile, "w") as f:
                    f.write(f"73561463237{savedNight}")
            
            if night < 4:
                loadNight(savedNight)
                camChangeSound.play()
                changeState("transition")
                transitionFrame = 0
                transitionTicks = 2*60
            else:
                winTicks = 600
                changeState("ending")
                endingMusic[night - 5].play()
    
    #if the state is ending
    elif gameState == "ending":
        for frame in staticFrames:
            frame.set_alpha(20)

        if staticFrame == 7:
            staticFrame = -1
        staticFrame += 1

        winTicks -= 1
        screen.blit(endingImages[night - 4], endingRect)

        if night == 4:
            screen.blit(staticFrames[staticFrame], staticFrameRect)

        if winTicks <= 0:
            camChangeSound.play()
            endingMusic[night - 5].stop()
            menuMusic.play(-1)
            changeState("title")

    

#base camera images
camImages = [cam1Images, cam2Images, cam3Images, cam4Images, cam5Images, cam6Images, cam7Images, cam8Images, cam9Images, cam10Images]

#create cam instances
cams = [
    Camera(cam1Image, cam1Rect, cam1ButtonImage, cam1ButtonRect, 2, 0),
    Camera(cam2Image, cam2Rect, cam2ButtonImage, cam2ButtonRect, 3, 1),
    Camera(cam3Image, cam3Rect, cam3ButtonImage, cam3ButtonRect, 3, 2),
    Camera(cam4Image, cam4Rect, cam4ButtonImage, cam4ButtonRect, 3, 3),
    Camera(cam5Image, cam5Rect, cam5ButtonImage, cam5ButtonRect, 3, 4),
    Camera(cam6Image, cam6Rect, cam6ButtonImage, cam6ButtonRect, 3, 5),
    Camera(cam7Image, cam7Rect, cam7ButtonImage, cam7ButtonRect, 3, 6),
    Camera(cam8Image, cam8Rect, cam8ButtonImage, cam8ButtonRect, 3, 7),
    Camera(cam9Image, cam9Rect, cam9ButtonImage, cam9ButtonRect, 3, 8),
    Camera(cam10Image, cam10Rect, cam10ButtonImage, cam10ButtonRect, 3, 9),
    Camera(cam11Image, cam11Rect, cam11ButtonImage, cam11ButtonRect, 0, 10)
]


#movement arrays for the stage characters telling them where they can move
movementArrays = [
    [[1], [3,5] , None, [1], None, [6, 7], [5], [5], None, None],
    [[1], [4, 8], None, None, [1], None, None, None, [9], [8]]
]

# creates array containing the 2 stage characters
basicChars = [
    BasicChar(0, movementArrays[0], 0, False),
    BasicChar(0, movementArrays[1], 1, False)
]

#plays the main menu music when the game is initally loaded
menuMusic.play(-1)

#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    stateUpdate()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()