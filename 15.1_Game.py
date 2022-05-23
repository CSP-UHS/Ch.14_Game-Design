'''
SPRITE GAME
-----------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''

import random
import arcade

# --- Constants ---
SW = 800
SH = 600
player_scale = 0.2
blue_scale = 0.25
player_speed = 2
scary_scale = 0.5
eye_scale = 0.5
sword_scale = 0.2
s_speed = 4
block_count = 1
block_scale = 0.75
LEVELS = 4
fire_speed = 3
fire_scale = 0.5
#------MyGame Class--------------

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/probably_main_character.png", player_scale)
        self.bounce_sound = arcade.load_sound('sounds/bounce.mp3')
    def update(self):
        self.center_x+=self.change_x
        self.center_y += self.change_y
        if self.left <= 0:
            self.left = 0
        if self.right >= SW:
            self.right = SW
        if self.top >= SH:
            self.top = SH
        if self.bottom <= 0:
            self.bottom = 0

class Barrier(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/wall.again.jpg",eye_scale)
        self.bounce_sound = arcade.load_sound('sounds/bounce.mp3')
    def update(self):
        pass
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/Enemy2.png", block_scale)
        self.bounce_sound = arcade.load_sound('sounds/bounce.mp3')
        self.death_sound = arcade.load_sound("sounds/explosion.mp3")
        self.dy = 2
        self.dx = 2
    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx
        if self.top > SH or self.bottom < 0:
            self.dy *= -1
        if self.left < 0 or self.right > SW:
            self.dx *= -1
class Fire_breath(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/explosions/explosion0019.png", block_scale)
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)
        self.flame_sound = arcade.load_sound("sounds/fire.mp3")
    def update(self):
        if self.bottom > SH or self.top < 0:
            self.kill()
        elif self.right > SW or self.left < 0:
            self.kill()
        if self.angle == 0:
            self.center_x = fire_speed
        elif self.angle == 90:
            self.center_y += fire_speed
        elif self.angle == 180:
            self.center_x -= fire_speed
        elif self.angle == 270:
            self.center_y -= fire_speed
class Enemy_2(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/Enemy1.png", block_scale)
        self.bounce_sound = arcade.load_sound('sounds/bounce.mp3')
        self.death_sound = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.center_x+=self.change_x
        self.center_y+=self.change_y
        if self.left <= 0:
            self.left = 0
        if self.right >= SW:
            self.right = SW
        if self.top >= SH:
            self.top = SH
        if self.bottom <= 0:
            self.bottom = 0
class Enemy_3(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/Enemy3.png")
        self.dx = 4
        self.death_sound = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.center_x+=self.dx
        if self.left <=0:
            self.dx *= -1
        if self.right >= SW:
            self.dx *=-1
class Laser(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png")
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.angle = 270
    def update(self):
        if self.top <= 0:
            self.kill()
        self.center_y -= fire_speed

class Boss(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/Enemy4.png", block_scale)
        self.bounce_sound = arcade.load_sound('sounds/bounce.mp3')
        self.death_sound = arcade.load_sound("sounds/explosion.mp3")
        self.dx = 2
        self.dy = 2
    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx
        if self.top > SH or self.bottom < 0:
            self.dy *= -1
        if self.left < 0 or self.right > SW:
            self.dx *= -1
class Blue_flame(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/Boss_boom.png",blue_scale)
        self.angle_choice = [0,45,90,135,180,225,270,315]
        self.fire_sound = arcade.load_sound("sounds/fire.mp3")
    def update(self):
        if self.bottom >= SH:
            self.kill()
        if self.top <= 0:
            self.kill()
        if self.right <= 0:
            self.kill()
        if self.left >= SW:
            self.kill()
        if self.angle == 0:
            self.center_x += fire_speed
        elif self.angle == 45:
            self.center_x +=fire_speed
            self.center_y +=fire_speed
        elif self.angle == 90:
            self.center_y +=fire_speed
        elif self.angle == 135:
            self.center_y +=fire_speed
            self.center_x-=fire_speed
        elif self.angle == 180:
            self.center_x -=fire_speed
        elif self.angle == 225:
            self.center_x -=fire_speed
            self.center_y -=fire_speed
        elif self.angle == 270:
            self.center_y -=fire_speed
        elif self.angle == 315:
            self.center_x +=fire_speed
            self.center_y -=fire_speed


class Sword(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/weapon_real.png", sword_scale)
        self.sword_sound = arcade.load_sound("sounds/sword.mp3")

    def update(self):
        self.center_x +=s_speed
        self.angle=-135
        if (self.center_x-self.change_x) > 20:
            self.kill()



class MyGame(arcade.Window):
    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.current_state = 0
    def reset(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.swords = arcade.SpriteList()
        self.enemy_second = arcade.SpriteList()
        self.fire_list = arcade.SpriteList()
        self.enemy_third = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.boss = arcade.SpriteList()
        self.boss_blue = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.bad_knight = Enemy_2()
        self.wing_dude = Enemy()
        self.why_eye = Enemy_3()
        self.evil_aladdin = Boss()

        self.Gameover = False
        if self.current_state == 1:
            self.background = arcade.load_texture("Images/backgroung.jpeg")
            self.bad_knight.center_x=SW/2
            self.bad_knight.center_y = SH-SH/10
            self.enemy_list.append(self.bad_knight)
            self.all_sprites.append(self.bad_knight)
        elif self.current_state == 2:
            self.wing_dude.center_x = SW / 4
            self.wing_dude.center_y = SH/2
            self.enemy_second.append(self.wing_dude)
            self.all_sprites.append(self.wing_dude)
        elif self.current_state == 3:
            self.why_eye.center_x = SW/2
            self.why_eye.center_y = SH-SH/10
            self.enemy_third.append(self.why_eye)
            self.all_sprites.append(self.why_eye)
        elif self.current_state == 4:
            self.evil_aladdin.center_x = SW/2
            self.evil_aladdin.center_y = SH-SH/10
            self.boss.append(self.evil_aladdin)
            self.all_sprites.append(self.evil_aladdin)

        character = Enemy()



        self.hero = Player()
        self.hero.center_x = SW/2
        self.hero.center_y = SH/10
        self.player_list.append(self.hero)
        self.all_sprites.append(self.hero)
        self.block = Barrier()
        coordinate_list = [[65,400],[65,150],[735,400],[735,150],[350,350],[200,150],[650,400],[650,150]]



        if self.current_state > 0 and self.current_state <= 4:
            for coordinate in coordinate_list :
                wall = Barrier()
                wall.center_x = coordinate[0]
                wall.center_y = coordinate[1]
                self.walls.append(wall)



    def on_draw(self):
        arcade.start_render()
        if self.current_state == 0:
            arcade.draw_text("Welcome to what I like to call Attitude City", SW/10, SH-SH/4, arcade.color.GO_GREEN, 18, 600, "center", "arial")
            arcade.draw_text("Press Z to begin because I said so. See, attitude.", SW/8 ,SH-SH/3, arcade.color.GO_GREEN, 14, 600, "center", "arial")
        elif self.current_state == 1:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.enemy_list.draw()
            self.walls.draw()
        elif self.current_state == 2:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.enemy_second.draw()
            self.fire_list.draw()
            self.walls.draw()
        elif self.current_state == 3:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.enemy_third.draw()
            self.lasers.draw()
            self.walls.draw()
        elif self.current_state == 4:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.evil_aladdin.draw()
            self.boss_blue.draw()
            self.walls.draw()
        elif self.current_state == 5:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("Wow you really do suck at this.", SW/10, SH-SH/5, arcade.color.GO_GREEN, 18, 600, "center", "arial")
            arcade.draw_text("I mean this game is pretty much for kids Mr Hermon.", SW/10, SH-SH/4, arcade.color.GO_GREEN,14, 600, "center", "arial")
            arcade.draw_text("Whatever. Press L to restart because you lost. How's that for some rude attitude.", SW/12, SH-SH/3, arcade.color.GO_GREEN, 14,  800, "center", "arial")
        elif self.current_state == 6:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("Goooooooooood jooooooob. Congratulations.", SW/8, SH-SH/5, arcade.color.GO_GREEN, 18, 600, "center", "arial")
            arcade.draw_text("I mean it wasn't that hard anyways. Don't go around thinking your good or anything", SW/14, SH-SH/4, arcade.color.GO_GREEN, 14, 800, "left", "arial")
            arcade.draw_text("If you want to replay, press o. I didn't say it had to make sense", SW/14, SH-SH/3, arcade.color.GO_GREEN, 14, 850, "left", "arial")
            arcade.draw_text("So welcome to Attitude City", 100, SH-SH/2, arcade.color.GO_GREEN, 14, 1000, "left", "arial")
            arcade.draw_text("And yes, we do have dinosaurs on our dinosaur tour", 50, SH/3, arcade.color.GO_GREEN, 14, 1000, "center", "arial")
        self.player_list.draw()
        self.swords.draw()

    def on_update(self, dt):
        self.player_list.update()
        self.enemy_list.update()
        self.enemy_second.update()
        self.fire_list.update()
        self.swords.update()
        self.enemy_third.update()
        self.lasers.update()
        self.boss.update()
        self.boss_blue.update()

        enemy_hit = arcade.check_for_collision_with_list(self.hero, self.enemy_list)
        if len(enemy_hit) > 0:
            self.hero.kill()
            self.current_state = 5
            self.hero_weapon.kill()
        hero_hit = arcade.check_for_collision_with_list(self.bad_knight, self.swords)
        if len(hero_hit) > 0:
            self.bad_knight.kill()
            self.current_state = 2
            arcade.play_sound(self.bad_knight.death_sound)
            self.reset()
        fire_hit = arcade.check_for_collision_with_list(self.hero, self.fire_list)
        if len(fire_hit) > 0:
            self.hero.kill()
            self.current_state = 5
            self.hero_weapon.kill()
        scary_hit = arcade.check_for_collision_with_list(self.hero, self.enemy_second)
        if len(scary_hit) > 0:
            self.hero.kill()
            self.hero_weapon.kill()
            self.current_state = 5
        scary_kill = arcade.check_for_collision_with_list(self.wing_dude, self.swords)
        if len(scary_kill) > 0:
            self.wing_dude.kill()
            self.current_state = 3
            arcade.play_sound(self.wing_dude.death_sound)
            self.reset()
        laser_kill = arcade.check_for_collision_with_list(self.hero, self.lasers)
        if len(laser_kill) > 0:
            self.hero.kill()
            self.current_state = 5
        eye_kill = arcade.check_for_collision_with_list(self.why_eye, self.swords)
        if len(eye_kill) > 0:
            self.why_eye.kill()
            self.current_state = 4
            arcade.play_sound(self.why_eye.death_sound)
            self.reset()
        eye_hit = arcade.check_for_collision_with_list(self.hero, self.enemy_third)
        if len(eye_hit) > 0:
            self.hero.kill()
            self.current_state = 5
            self.hero_weapon.kill()
        boss_hit = arcade.check_for_collision_with_list(self.hero, self.boss)
        if len(boss_hit) > 0:
            self.hero.kill()
            self.current_state = 5
            self.hero_weapon.kill()
        blue_fire_hit = arcade.check_for_collision_with_list(self.hero,self.boss_blue)
        if len(blue_fire_hit) > 0:
            self.hero.kill()
            self.current_state = 5
            self.hero_weapon.kill()
        boss_kill = arcade.check_for_collision_with_list(self.evil_aladdin, self.swords)
        hero_wall = arcade.check_for_collision_with_list(self.hero, self.walls)
        if len(hero_wall) > 0:
            self.hero.change_y*=-1
            self.hero.change_x*=-1
            arcade.play_sound(self.hero.bounce_sound)
        knight_wall = arcade.check_for_collision_with_list(self.bad_knight, self.walls)
        if len(knight_wall) > 0:
            self.bad_knight.change_x*=-1
            self.bad_knight.change_y*=-1
            arcade.play_sound(self.bad_knight.bounce_sound)
        scary_wall = arcade.check_for_collision_with_list(self.wing_dude, self.walls)
        if len(scary_wall) > 0:
            if self.wing_dude.center_x < scary_wall[0].left or self.wing_dude.center_x > scary_wall[0].right:
                self.wing_dude.dx*=-1
                arcade.play_sound(self.wing_dude.bounce_sound)
            elif self.wing_dude.center_y < scary_wall[0].bottom or self.wing_dude.center_y > scary_wall[0].top:
                self.wing_dude.dy*=-1
                arcade.play_sound(self.wing_dude.bounce_sound)

        if len(boss_kill) > 0:
            self.evil_aladdin.kill()
            self.current_state = 6
            arcade.play_sound(self.evil_aladdin.death_sound)
            self.reset()
        for character in self.enemy_second:
            if random.randrange(50) == 0:
                self.ebullet = Fire_breath()
                self.ebullet.center_x = character.center_x
                self.ebullet.center_y = character.center_y
                self.fire_list.append(self.ebullet)
                self.all_sprites.append(self.ebullet)
                arcade.play_sound(self.ebullet.flame_sound)
        for ebullet in self.fire_list:
            fire_wall = arcade.check_for_collision_with_list(ebullet, self.walls)
            if len(fire_wall) > 0:
                ebullet.kill()
        boss_wall = arcade.check_for_collision_with_list(self.evil_aladdin, self.walls)
        if len(boss_wall) > 0:
            if self.evil_aladdin.center_x < boss_wall[0].left or self.evil_aladdin.center_x > boss_wall[0].right:
                self.evil_aladdin.dx *= -1
                arcade.play_sound(self.evil_aladdin.bounce_sound)
            elif self.evil_aladdin.center_y < boss_wall[0].bottom or self.evil_aladdin.center_y > boss_wall[0].top:
                self.evil_aladdin.dy *= - 1
                arcade.play_sound(self.evil_aladdin.bounce_sound)
        for pig in self.boss_blue:
            blue_wall = arcade.check_for_collision_with_list(pig, self.walls)
            if len(blue_wall) > 0:
                pig.kill()


        for thing in self.enemy_third:
            if random.randrange(15) == 0:
                eye_laser = Laser()
                eye_laser.center_x = thing.center_x
                eye_laser.center_y = thing.bottom
                self.lasers.append(eye_laser)
                arcade.play_sound(eye_laser.laser_sound)
        for monster in self.boss:
            x = 0
            if random.randrange(50) == 0:
                for i in range(8):
                    boss_fire = Blue_flame()
                    boss_fire.center_x = monster.center_x
                    boss_fire.center_y = monster.center_y
                    boss_fire.angle = boss_fire.angle_choice[x]
                    self.boss_blue.append(boss_fire)
                    self.all_sprites.append(boss_fire)
                    x+=1





    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.hero.change_y=player_speed
            self.bad_knight.change_y=-player_speed
        elif key == arcade.key.DOWN:
            self.hero.change_y=-player_speed
            self.bad_knight.change_y=player_speed
        elif key == arcade.key.RIGHT:
            self.hero.change_x=player_speed
            self.bad_knight.change_x=-player_speed
        elif key == arcade.key.LEFT:
            self.hero.change_x=-player_speed
            self.bad_knight.change_x=player_speed
        elif key == arcade.key.D:
            self.hero_weapon = Sword()
            self.hero_weapon.change_x = self.hero.center_x+4
            self.hero_weapon.center_x = self.hero.center_x+4
            self.hero_weapon.center_y = self.hero.center_y-5
            self.swords.append(self.hero_weapon)
            arcade.play_sound(self.hero_weapon.sword_sound)
        elif key == arcade.key.Z:
            while self.current_state == 0:
                self.current_state = 1
                self.reset()
        elif key == arcade.key.L:
            while self.current_state == 5:
                self.current_state = 1
                self.reset()
        elif key == arcade.key.O:
            while self.current_state == 6:
                self.current_state = 1
                self.reset()
        elif key == arcade.key.K:
            while self.current_state ==1:
                self.current_state = 4
                self.reset()
        elif key == arcade.key.U:
            while self.current_state ==  1:
                self.current_state = 3
                self.reset()



    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.hero.change_y = 0
            self.bad_knight.change_y = 0
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.hero.change_x = 0
            self.bad_knight.change_x = 0


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"2015 Attitude City")
    window.reset()
    arcade.run()

#------Run Main Function-----
if __name__ == "__main__":
    main()
