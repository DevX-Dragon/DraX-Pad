# this code handles the logic for the games that can be played with the macro keys.
# this is a simple dodge game where you die when the pixel touches you.
# thanks to awesome-macropad repo for game ideas.
import random

class MacropadGame:
    def __init__(self, display):
        self.display = display
        self.reset()

    def reset(self):
        self.player_x = 64
        self.enemy_x = random.randint(0, 120)
        self.enemy_y = 0
        self.score = 0
        self.game_over = False
        self.speed = 2

    def handle_input(self, key_num):
        if self.game_over:
            if key_num == 1: self.reset() # Press middle top key to restart
            return

        if key_num == 0: self.player_x -= 8  # Move Left
        if key_num == 2: self.player_x += 8  # Move Right
        self.player_x = max(0, min(118, self.player_x))

    def update(self):
        if self.game_over: return

        # Enemy falls down
        self.enemy_y += self.speed
        
        # Check if enemy hit the bottom
        if self.enemy_y > 64:
            self.enemy_y = 0
            self.enemy_x = random.randint(0, 120)
            self.score += 1
            # Speed up slightly every 5 points
            if self.score % 5 == 0:
                self.speed += 1

        # COLLISION DETECTION (Dodge Logic)
        # If enemy Y is near player Y and X positions overlap
        if self.enemy_y > 45 and abs(self.player_x - self.enemy_x) < 8:
            self.game_over = True

    def draw(self):
        self.display.fill(0)
        if self.game_over:
            self.display.text("GAME OVER!", 35, 20, 1)
            self.display.text(f"Score: {self.score}", 40, 35, 1)
            self.display.text("Press Key 1", 30, 50, 1)
        else:
            # Draw Score
            self.display.text(f"Score: {self.score}", 0, 0, 1)
            # Draw Player (Paddle)
            self.display.fill_rect(self.player_x, 55, 12, 4, 1)
            # Draw Falling Enemy (Square)
            self.display.fill_rect(self.enemy_x, self.enemy_y, 4, 4, 1)
        
        self.display.show()