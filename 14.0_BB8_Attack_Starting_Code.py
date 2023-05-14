#Sign your name:_Oded Harazi
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade
imposter = arcade.load_sound("sounds/Among-Us-Role-Sound-Effect.wav")
# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 10
bullet_scale = 1
bullet_speed = 10
SW = 800
SH = 600
SP = 10
t_speed = 2
#points for bullets and troopers
t_score = 5
b_score = 1
EXPLOSION_TEXTURE_COUNT = 50

#Explosion Class
class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.current_texture = 0
        self.textures = texture_list
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()

# Player Class
class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")
    def update(self):
        self.center_x+=self.change_x
        if self.right < 0:
            self.left = SW
        elif self.left > SW:
            self.right = 0

class Trooper(arcade.Sprite):

    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y-=t_speed
        if self.top < 0:
            self.center_x = random.randrange(self.w,SW-self.w)
            self.center_y = random.randrange(SH+self.h,SH*2)

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png",bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y+=bullet_speed
        if self.bottom > SH:
            self.kill()

#Enemy Bullet Class
class Enemy_Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png",bullet_scale)
    def update(self):
        self.center_y-=bullet_speed
        self.angle = 270
        if self.top < 0:
            self.kill()



#------MyGame C lass--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)
        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))
    def reset(self):
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        self.score = 0
        self.Gameover = False


        #Create the Player
        self.BB8 = Player()
        self.BB8.center_x = SH/2
        self.BB8.center_y = SH/8
        self.player_list.append(self.BB8)
        self.Winner = False

        #Create the troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randint(trooper.w, SW-trooper.w)
            trooper.center_y = random.randrange(SH//2,SH-trooper.h)
            self.trooper_list.append(trooper)

        #
        # self.explosions = Explosion()
        # self.explosion.center_x = self.trooper.center_x
        # self.explosions.center_y = self.trooper.center_y

    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()
        self.bullets.draw()
        self.ebullets.draw()
        self.explosions.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output,SW-80,SH-20,arcade.color.BLACK,14)

    #Draw the "game over" screen
        if self.Gameover == True:
            arcade.draw_rectangle_filled(SW//2,SH//2,SW,SH,arcade.color.BLACK)
            arcade.draw_text(f"High Score: {self.score}", SW/2,SH/4, anchor_x = "center", anchor_y = "center")

            arcade.draw_text("Game over: Press P to Play Again!", SW/2, SH/2, arcade.color.NEON_GREEN,14,anchor_x = "center", anchor_y = "center")

        if self.Winner == True:
            arcade.draw_rectangle_filled(SW//2,SH//2,SW,SH,arcade.color.BLACK)
            arcade.draw_text(f"High Score: {self.score}", SW/2,SH/4, anchor_x = "center", anchor_y = "center")

            arcade.draw_text("You Won! - Press P to Play Again!", SW/2, SH/2, arcade.color.NEON_GREEN,14,anchor_x = "center", anchor_y = "center")
    def on_update(self, dt):
        self.trooper_list.update()
        self.player_list.update()
        self.bullets.update()
        self.ebullets.update()
        self.explosions.update()


        #BB8 dies to trooper
        bb8_hit = arcade.check_for_collision_with_list(self.BB8,self.trooper_list)
        if len(bb8_hit) > 0 and not self.Gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.Gameover = True

        #Troopers Randomly Drop Bombs
        for trooper in self.trooper_list:
            if random.randrange(1000) == 1:
                ebullet = Enemy_Bullet()
                ebullet.angle = 0
                ebullet.center_x = trooper.center_x
                ebullet.top = trooper.bottom
                self.ebullets.append(ebullet)
        #Detect if bb8 gets hit
        BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
        if len(BB8_bombed) > 0 and not self.Gameover and not self.Winner:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.Gameover = True

        #Bullets hitting troopers
        for bullet in self.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
            if len(hit_list) > 0:
                arcade.play_sound(self.BB8.explosion)
                bullet.kill()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.scale = 1
                self.explosions.append(explosion)
                # self.explosions.append_texture(self.explosion_texture_list)

            for trooper in hit_list:
                trooper.kill()
                self.score += t_score

        if len(self.trooper_list) == 0:
            self.Winner = True


    # def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
    #     self.BB8.center_x = x
    #     self.BB8.center_y = y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.BB8.change_y = SP
        elif key == arcade.key.DOWN:
            self.BB8.change_y = -SP
        elif key == arcade.key.LEFT:
            self.BB8.change_x = -SP
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = SP
        elif key == arcade.key.P:
            self.reset()

        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 90
            self.bullets.append(self.bullet)
            if self.score >= 0:
                self.score -= b_score
            else:
                self.score = 0
            arcade.play_sound(self.BB8.laser_sound)

        elif key == arcade.key.R and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 0
            self.bullets.append(self.bullet)
            if self.score >= 0:
                self.score -= b_score
            else:
                self.score = 0
            arcade.play_sound(self.BB8.laser_sound)

        elif key == arcade.key.Q:
            arcade.play_sound(imposter)
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.BB8.change_y = 0
        elif key == arcade.key.DOWN:
            self.BB8.change_y = 0
        if key == arcade.key.LEFT:
            self.BB8.change_x = 0
        if key == arcade.key.RIGHT:
            self.BB8.change_x = 0
        elif key == arcade.key.R and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 0
            self.bullets.append(self.bullet)
            if self.score >= 0:
                self.score -= b_score
            else:
                self.score = 0
            arcade.play_sound(self.BB8.laser_sound)


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    window.reset()
    arcade.run()

#------Run Main Function-----
if __name__ == "__main__":
    main()
