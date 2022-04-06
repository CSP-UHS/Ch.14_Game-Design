#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800
SH = 600
SP = 4


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
    def update(self):
        pass

class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png")
        self.w=int(self.w)
        self.h = int(self.h)








#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)


    def reset(self):
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        self.score = 0

        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH/2
        self.player_list.append(self.BB8)

        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w,SW-trooper.w)
            trooper.center_y = random.randrange(trooper.h,SH-trooper.h)

    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()

        output = f"score: {self.score}"
        arcade.draw_text(output,10,20,arcade.color.BLACK,14,)
    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()

        trooper_hit_list = arcade.check_for_collision_with_list(self.BB8,self.trooper_list)
        for trooper in trooper_hit_list:
            trooper.kill()
            arcade.play_sound(self.BB8)
            self.score+=1

        if self.score == self.trooper_count:
            self.reset()


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.BB8.center_x = x
        self.BB8.center_y = y


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    arcade.run()


#------Run Main Function-----
if __name__ == "__main__":
    main()
