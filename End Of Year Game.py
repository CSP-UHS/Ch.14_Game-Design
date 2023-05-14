import arcade
import random

SW = 1000
SH = 750

SIZE = 5
LEFT = arcade.key.LEFT
RIGHT = arcade.key.RIGHT
UP = arcade.key.UP
DOWN = arcade.key.DOWN
ImposterShadowSize = 0.3
ImposterShadowSpeed = 8
MonsterAttackSpeed = 1/20
CrewmateAttackSpeed = 1/80
EXPLOSION_TEXTURE_COUNT = 50

# from Player import *
SSPEED = 8
SPEED = 5

from On_Press import *
from amongus_attack import *

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/amongus normal.png",.75)
        self.angle = 0
        self.center_x = random.randint(0,SW)
        self.center_y = random.randint(0,SH)
        self.change_x = 0
        self.change_y = 0
        self.pressed_keys = set()
        self.flipped_horizontally = bool(False)

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x


        if self.left < 0:
            self.left = 0
        elif self.right > 2*SW:
            self.right = 2*SW

        elif self.bottom < 0:
            self.bottom = 0

        elif self.top > SH*2:
            self.top = SH*2

        # elif self.center_x >= SW*2 - self.width and self.center_y >= SH*2 - self.height:
        #     self.center_x = SW*2 - self.width
        #     self.center_y = SH*2 - self.height

            # Imposter Motion
            # if UP in self.pressed_keys:
            #     self.change_y = ISPEED
            # elif DOWN in self.pressed_keys:
            #     self.change_y = -ISPEED
            # elif LEFT in self.pressed_keys:
            #     self.change_x = -ISPEED
            # elif RIGHT in self.pressed_keys:
            #     self.change_x = ISPEED

class Monster(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/mongus.png",2)
        self.angle = 0
        self.center_x = random.randint(0,SW)
        self.center_y = random.randint(0,SH)
        self.change_x = 0
        self.change_y = 0
        self.pressed_keys = set()
        self.flipped_horizontally = bool(False)
        # self.monster_health = 10

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x


        if self.left < 0:
            self.left = 0
        elif self.right > 2*SW:
            self.right = 2*SW

        elif self.bottom < 0:
            self.bottom = 0

        elif self.top > SH*2:
            self.top = SH*2

class Crewmates(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/amongus normal.png")
        self.angle = 0
        self.scale = 0.5
        self.center_x = random.randint(0,SW)
        self.center_y = random.randint(0,SH)
        self.change_y = 0
        self.change_x = 0


    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x

        if self.left < 0:
            self.left = 0
        elif self.right > 2 * SW:
            self.right = 2 * SW

        elif self.bottom < 0:
            self.bottom = 0

        elif self.top > SH * 2:
            self.top = SH * 2

class RangeAttack(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/ImposterShadow.png", ImposterShadowSize/2)

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x
        self.angle += 1
        if self.bottom > SH*2:
            self.kill()
        if self.top < -SH:
            self.kill()
        if self.left < -SW :
            self.kill()
        if self.right > SW*2:
            self.kill()


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.current_texture = 0
        self.textures = texture_list
        # self.explosion = arcade.load_sound("sounds/explosion.wav")
    #
    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class MyGame(arcade.Window):
    def __init__(self,screen_width,screen_height,title):
        super().__init__(screen_width,screen_height,title,True)
        self.set_background = arcade.load_texture("Images/Amongus Wallpaper 2.jpeg")
        self.imposter_sound = arcade.load_sound("Among-Us-Role-Sound-Effect.wav")
        self.ambient = arcade.load_sound("Ambient Weapons Sound Effect Wav.wav")
        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

        self.explosions = arcade.SpriteList()
        self.c_count = 1
        self.pressed_keys = set()
        self.SPEED = 3
        self.mouseaim = False
        self.GameOver = False
        arcade.play_sound(self.ambient)

    # def reset(self):
        self.player_list = arcade.SpriteList()
        # Creating Imposter
        self.imposter = Player()
        self.imposter.center_x = SW
        self.imposter.center_y = SH
        self.player_list.append(self.imposter)

        # Creating Crewmate
        self.crewmate_list = arcade.SpriteList()
        for i in range(self.c_count):
            crewmate = Crewmates()
            crewmate.center_x = random.randrange(50,SH-50)
            crewmate.center_y = random.randrange(50,SW-50)
            self.crewmate_list.append(crewmate)

        for i in range(self.c_count):
            crewmate = Crewmates()
            crewmate.center_x = random.randrange(SH+50,(SH*2)-50)
            crewmate.center_y = random.randrange(SW-50, (SW*2) - 50)
            self.crewmate_list.append(crewmate)


        # Creating Range Attack
        self.rangeattack_list = arcade.SpriteList()



    # def level_up(self):

        self.Gameover = False
        self.Winner = False
        self.level = False
        self.monster_list = arcade.SpriteList()
        self.monster_health = 9

        # Final Boss
        # self.monster_list = arcade.SpriteList()
        # self.monster = Monster()
        # self.monster.center_x = 100
        # self.monster.center_y = 100
    # def level(self):
    #     if self.level == True:
            # self.monster_list = arcade.SpriteList()
        self.monster = Monster()
        self.monster.center_x = 300
        self.monster.center_y = 300
        self.monster_list.append(self.monster)


    def crewmate_attack(self):
        # if arcade.key.C in self.pressed_keys:
        for crewmate in self.crewmate_list:
            if crewmate.center_y > self.imposter.center_y:
                crewmate.change_y -= CrewmateAttackSpeed
                if crewmate.center_x > self.imposter.center_x:
                    crewmate.change_x -= CrewmateAttackSpeed
                elif crewmate.center_x < self.imposter.center_x:
                    crewmate.change_x += CrewmateAttackSpeed
            elif crewmate.center_y < self.imposter.center_y:
                crewmate.change_y += CrewmateAttackSpeed
                if crewmate.center_x > self.imposter.center_x:
                    crewmate.change_x -= CrewmateAttackSpeed
                elif crewmate.center_x < self.imposter.center_x:
                    crewmate.change_x += CrewmateAttackSpeed

    def monster_attack(self):
        # if arcade.key.C in self.pressed_keys:
        for monster in self.monster_list:
            if monster.center_y > self.imposter.center_y:
                monster.change_y -= MonsterAttackSpeed
                if monster.center_x > self.imposter.center_x:
                    monster.change_x -= MonsterAttackSpeed
                elif monster.center_x < self.imposter.center_x:
                    monster.change_x += MonsterAttackSpeed
            elif monster.center_y < self.imposter.center_y:
                monster.change_y += MonsterAttackSpeed
                if monster.center_x > self.imposter.center_x:
                    monster.change_x -= MonsterAttackSpeed
                elif monster.center_x < self.imposter.center_x:
                    monster.change_x += MonsterAttackSpeed


    def on_update(self,dt):
        self.crewmate_attack()
        self.crewmate_list.update()
        self.player_list.update()
        self.rangeattack_list.update()
        self.screen_motion()
        self.explosions.update()


        if self.level == True:
            self.monster_attack()
            self.monster_list.update()

        # self.level()aa
        # self.mouse_aim_control()
        imposter_kill = arcade.check_for_collision_with_list(self.imposter,self.crewmate_list)
        if len(imposter_kill) > 0 and self.Gameover == False:
            self.imposter.kill()
            arcade.play_sound(self.imposter_sound)
            self.Gameover = True


        for impostershadow in self.rangeattack_list:
            hit_list = arcade.check_for_collision_with_list(impostershadow, self.crewmate_list)
            if len(hit_list) > 0:
                impostershadow.kill()
            elif len(self.crewmate_list) == 0:
                self.level = True

            for crewmate in hit_list:
                # self.crewmate_list.shuffle()
                if crewmate.scale >= 0.25:
                    crewmate.scale /= 2
                else:
                    crewmate.kill()
                    arcade.play_sound(self.imposter_sound)



        for impostershadow in self.rangeattack_list:
            hit_list = arcade.check_for_collision_with_list(impostershadow, self.monster_list)
            if len(hit_list) > 0:
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.scale = 10
                self.explosions.append(explosion)
                impostershadow.kill()
            # elif len(self.monster_list) == 0:
                # self.Winner = True


            for monster in hit_list:
                # self.crewmate_list.shuffle()

                if self.monster_health >= 1:
                    self.monster_health -= 1
                elif self.monster_health <= 0.1:
                    monster.kill()
                    self.Winner = True
                    # arcade.play_sound(self.imposter_sound)

        # for crewmate in self.crewmate_list:
        #     if crewmate.center_y > self.imposter.center_y:
        #         crewmate.change_y -= 1/30
        #     elif crewmate.center_y < self.imposter.center_y:
        #         crewmate.change_y += 1/30
        #     elif crewmate.center_x > self.imposter.center_x:
        #         crewmate.change_x -= 1/30
        #     elif crewmate.center_x < self.imposter.center_x:
        #         crewmate.change_x += 1/30

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SW, SH, SW * 2, SH * 2, self.set_background)
        self.player_list.draw()
        self.crewmate_list.draw()
        self.explosions.draw()
        self.rangeattack_list.draw()
        arcade.draw_rectangle_filled(SW, SH * 2, SW * 2, 5, arcade.color.WHITE, )
        arcade.draw_rectangle_filled(SW, 0, SW * 2, 5, arcade.color.WHITE, )
        arcade.draw_rectangle_filled(0, SH, 5, SH * 2, arcade.color.WHITE, )
        arcade.draw_rectangle_filled(SW * 2, SH, 5, SH * 2, arcade.color.WHITE, )

        if self.Gameover == True:
            arcade.draw_rectangle_filled(SW, SH, SW*2, SH*2, arcade.color.BLACK,)
            arcade.draw_text("Game over!", self.imposter.center_x, self.imposter.center_y, arcade.color.NEON_GREEN, 100,
                             anchor_x="center", anchor_y="center")

        if self.Winner == True:
            self.imposter.center_x = SW
            self.imposter.center_y = SH
            arcade.draw_rectangle_filled(SW, SH, SW*2, SH*2, arcade.color.BLACK,)
            arcade.draw_text("You Won!", self.imposter.center_x, self.imposter.center_y, arcade.color.NEON_GREEN, 100,
                             anchor_x="center", anchor_y="center")

        if self.level == True and self.Winner == False:
            self.monster_list.draw()
            output = f"Monster Health: {self.monster_health+1}"
            arcade.draw_text(output, self.imposter.center_x -110, self.imposter.center_y - 110, arcade.color.GREEN, 14)

    def screen_motion(self):
        move_left = self.imposter.center_x- (SW/2)
        move_right = self.imposter.center_x+ (SW/2)
        move_up = self.imposter.center_y + (SH/2)
        move_down = self.imposter.center_y- (SH/2)
        self.set_viewport(move_left,move_right,move_down,move_up)




    def on_mouse_press(self, mouse_x: int, mouse_y: int, button: int, modifiers: int,):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Left Mouse Button Pressed at", mouse_x,mouse_y)


        elif button == arcade.MOUSE_BUTTON_RIGHT:
            print("Right Mouse Button Pressed at", mouse_x,mouse_y)


    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)
        if arcade.key.ESCAPE in self.pressed_keys:
            arcade.exit()
            # Imposter Motion
        if arcade.key.LSHIFT in self.pressed_keys:
            self.SPEED = SSPEED
        if UP in self.pressed_keys:
            self.imposter.change_y = self.SPEED
        if DOWN in self.pressed_keys:
            self.imposter.change_y = -self.SPEED
        if LEFT in self.pressed_keys:
            self.imposter.change_x = -self.SPEED
        if RIGHT in self.pressed_keys:
            self.imposter.change_x = self.SPEED
            # Crewmate Motion
        # if key == arcade.key.W:
        #     self.crewmate.change_y = SPEED
        # if key == arcade.key.S:
        #     self.crewmate.change_y = -SPEED
        # if key == arcade.key.A:
        #     self.crewmate.change_x = -SPEED
        # if key == arcade.key.D:
        #     self.crewmate.change_x = SPEED

        # Range Attack UP
        if arcade.key.W in self.pressed_keys:
            self.impostershadow = RangeAttack()
            self.impostershadow.center_x = self.imposter.center_x
            self.impostershadow.change_y = ImposterShadowSpeed
            self.impostershadow.bottom = self.imposter.top
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        # Range Attack Down
        if arcade.key.S in self.pressed_keys:
            self.impostershadow = RangeAttack()
            self.impostershadow.center_x = self.imposter.center_x
            self.impostershadow.change_y = -ImposterShadowSpeed
            self.impostershadow.top = self.imposter.bottom
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        # Range Attack Right
        if arcade.key.D in self.pressed_keys:
            self.impostershadow = RangeAttack()
            self.impostershadow.change_x = ImposterShadowSpeed
            self.impostershadow.center_y = self.imposter.center_y
            self.impostershadow.left = self.imposter.right
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        # Range Attack Left
        if arcade.key.A in self.pressed_keys:
            self.impostershadow = RangeAttack()
            self.impostershadow.change_x = -ImposterShadowSpeed
            self.impostershadow.center_y = self.imposter.center_y
            self.impostershadow.right = self.imposter.left
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        if key == arcade.key.M:
            self.mouseaim = True
        # Range Attack Up with Mouse
        if arcade.key.SPACE in self.pressed_keys and self._mouse_y > self.imposter.center_y and self.mouseaim == True:
            self.impostershadow = RangeAttack()
            self.impostershadow.center_x = self.imposter.center_x
            self.impostershadow.change_y = ImposterShadowSpeed
            self.impostershadow.bottom = self.imposter.top
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)
            arcade.play_sound(self.imposter_sound)

        # Range Attack Down with Mouse
        if arcade.key.SPACE in self.pressed_keys and self._mouse_y < self.imposter.center_y and self.mouseaim == True:
            self.impostershadow = RangeAttack()
            self.impostershadow.center_x = self.imposter.center_x
            self.impostershadow.change_y = -ImposterShadowSpeed
            self.impostershadow.top = self.imposter.bottom
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        # Range Attack Right with Mouse
        if arcade.key.SPACE in self.pressed_keys and self._mouse_x > self.imposter.center_x and self.mouseaim == True:
            self.impostershadow = RangeAttack()
            self.impostershadow.change_x = ImposterShadowSpeed
            self.impostershadow.center_y = self.imposter.center_y
            self.impostershadow.left = self.imposter.right
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)

        # Range Attack Left with Mouse
        if arcade.key.SPACE in self.pressed_keys and self._mouse_x < self.imposter.center_x and self.mouseaim == True:
            self.impostershadow = RangeAttack()
            self.impostershadow.change_x = -ImposterShadowSpeed
            self.impostershadow.center_y = self.imposter.center_y
            self.impostershadow.right = self.imposter.left
            self.impostershadow.angle = 0
            self.rangeattack_list.append(self.impostershadow)


    def on_key_release(self, key, modifiers):
        self.pressed_keys.remove(key)
        # Imposter Stop Motion
        if key == arcade.key.LSHIFT:
            self.SPEED = SPEED

        if key == arcade.key.UP:
            self.imposter.change_y = 0
        elif key == arcade.key.DOWN:
            self.imposter.change_y = 0
        if key == arcade.key.LEFT:
            self.imposter.change_x = 0
        if key == arcade.key.RIGHT:
            self.imposter.change_x = 0
        # Crewmate Stop Motion
        # if key == arcade.key.W:
        #     self.crewmate.change_y = 0
        # elif key == arcade.key.S:
        #     self.crewmate.change_y = 0
        # if key == arcade.key.A:
        #     self.crewmate.change_x = 0
        # if key == arcade.key.D:
        #     self.crewmate.change_x = 0

    # def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
    #     self.imposter.center_x = x
    #     self.imposter.center_y = y

#-----Main Function--------
def main():
    window = MyGame(SW,SH,"Amongus")
    arcade.run()
    # window.reset()
#------Run Main Function-----
if __name__ == "__main__":
    main()



