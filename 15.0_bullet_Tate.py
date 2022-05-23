#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
bullet_scale = 1
SW = 800
SH = 600
SP = 4
t_speed = 2
t_score = 2
b_score = 1
b_speed = 10
EXPLOSION_TEXTURE_COUNT = 50
explosion_scale = 5
levels  = 3

class Explosion(arcade.Sprite):
    def __init__(self,texture_list):
        super().__init__("Images/explosions/explosion0000.png", explosion_scale)
        self.current_texture = 0
        self.textures = texture_list

        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.current_texture +=1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.center_x+=self.change_x
        if self.left <= 0:
            self.left = 0
        if self.right >= SW:
            self.right = SW


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w=int(self.width)
        self.h = int(self.height)
    def update(self):
        self.center_y  -= t_speed
        if self.top < 0:
            self.center_x =random.randrange(self.w, SW-self.w)
            self.center_y = random.randrange(SH+self.h, SH*2)


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")

    def update(self):
        self.center_y +=b_speed
        self.angle=90
        if self.top<0:
            self.kill()

class Enemy_bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")

    def update(self):
        self.center_y -=b_speed
        self.angle=-90
        if self.bottom>SH:
            self.kill()






#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.current_state = 0
        self.Gameover = True
        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))


    def reset(self):
        if self.current_state in range(1,levels+1):
            self.background = arcade.load_texture(f"Images/sky{self.current_state}.png")

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        # self.Gameover = False
        # self.score = 0

        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.bottom = 20
        self.player_list.append(self.BB8)

        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w,SW-trooper.w)
            trooper.center_y = random.randrange(SH/2,SH*2)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW//2,SH//2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and SPACE to fire. Choose level 1, 2, or 3.", SW//2, SH//2, arcade.color.PISTACHIO, align = "center", anchor_x = "center")
        elif not self.Gameover:
            arcade.draw_texture_rectangle(SW//2, SH//2, SW, SH, self.background)
            self.trooper_list.draw()
            self.player_list.draw()
            self.bullets.draw()
            self.ebullets.draw()
            self.explosions.draw()

            output = f"score: {self.score}"
            level = f"Level:{self.current_state}"
            arcade.draw_rectangle_filled(SW-40,SH-20,80,40,arcade.color.CARIBBEAN_GREEN)
            arcade.draw_text(level, SW - 80, SH - 20, arcade.color.CITRINE,14)
            arcade.draw_text(output, SW - 80, SW - 20, arcade.color.YELLOW, 14)
        else:
            arcade.draw_rectangle_filled(SW/2,SH/2,SW,SH,arcade.color.BLACK)
            arcade.draw_text("THE FORCE IS NOT STRONG WITH THIS ONE. PRESS I FOR INSTRUCTIONS OR A LEVEL NUMBER.",SW/2,SH/2,arcade.color.CITRINE,10,align="center",anchor_x="center")

    def on_update(self, dt):
        if self.current_state in range(1,levels+1):
            self.Gameover = False
        else:
            self.Gameover = True

        if not self.Gameover:

            self.player_list.update()
            self.trooper_list.update()
            self.bullets.update()
            self.ebullets.update()
            self.explosions.update()



            if len(self.trooper_list) == 0:
                self.current_state+=1
                self.reset()



            BB8_hit = arcade.check_for_collision_with_list(self.BB8,self.trooper_list)

            if len(BB8_hit) > 0 and not self.Gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_state = levels + 1

            for trooper in self.trooper_list:
                if random.randrange(100)==0:
                    ebullet = Enemy_bullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.top = trooper.bottom
                    self.ebullets.append(ebullet)

            BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
            if len(BB8_bombed) > 0 and not self.Gameover:
                self.BB8.kill()
                self.Gameover = True






            for bullet in self.bullets:
                hit_list = arcade.check_for_collision_with_list(bullet,self.trooper_list)
                if len(hit_list) > 0:
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosions.append(explosion)

                for trooper in hit_list:
                    trooper.kill()
                    self.score += t_score







    def on_key_press(self, key, modifiers):


        if key == arcade.key.RIGHT:
            self.BB8.change_x=SP
        elif key == arcade.key.LEFT:
            self.BB8.change_x = -SP
        elif key == arcade.key.R:
            self.reset()
        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullets.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)
            self.bullet.angle = 90

        if key == arcade.key.I and self.Gameover:
            self.current_state = 0
        elif key == arcade.key.KEY_1 and self.Gameover:
            self.current_state = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_2 and self.Gameover:
            self.current_state = 2
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_3 and self.Gameover:
            self.current_state = 3
            self.score = 0
            self.reset()


    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.BB8.change_x=0



#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    window.reset()
    arcade.run()


#------Run Main Function-----
if __name__ == "__main__":
    main()

