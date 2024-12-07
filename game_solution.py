# Sprite sheet and maze image sourced from:
# https://www.spriters-resource.com/arcade/pacman/sheet/52631/
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import time
import random
import json


class PacManGame:
    def __init__(self, master):
        # All initialization variables
        self.master = master
        self.master.title("PacMan")
        self.master.geometry("600x600")
        self.current_session_scores = []
        self.leaderboard_file = "leaderboard.txt"
        self.player_name = "No name"
        self.start_time = 0
        self.level = 1

        # Create the game canvas
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()
        self.canvas.tag_raise("pause_menu")

        # Load background
        self.background_image = Image.open("Coursework2/PacManBaseMaze.png").resize((600, 600))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw",
                                 tags="background")  # align with top left corner

        # Load pellets
        self.pellet_image = ImageTk.PhotoImage(Image.open("Coursework2/PacManPellet.png").resize((5, 5)))
        self.power_pellet_image = ImageTk.PhotoImage(
            Image.open("Coursework2/PacManPowerPellet.png").resize((20, 20))
        )

        # Load bonus fruits
        self.cherry_image = ImageTk.PhotoImage(Image.open("Coursework2/Cherry.png").resize((30, 30)))
        self.strawberry_image = ImageTk.PhotoImage(
            Image.open("Coursework2/Strawberry.png").resize((30, 30))
        )
        self.apple_image = ImageTk.PhotoImage(Image.open("Coursework2/Apple.png").resize((30, 30)))

        # Load Pacman directional frames
        self.pacman_frames = {
            "Left": [
                ImageTk.PhotoImage(Image.open("Coursework2/PacManRightFrame1.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManRightFrame2.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame3.png").resize((30, 30))),
            ],
            "Right": [
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame1.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame2.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame3.png").resize((30, 30))),
            ],
            "Up": [
                ImageTk.PhotoImage(Image.open("Coursework2/PacManUpFrame1.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManUpFrame2.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame3.png").resize((30, 30))),
            ],
            "Down": [
                ImageTk.PhotoImage(Image.open("Coursework2/PacManDownFrame1.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManDownFrame2.png").resize((30, 30))),
                ImageTk.PhotoImage(Image.open("Coursework2/PacManFrame3.png").resize((30, 30))),
            ],
        }

        # Player's default stats
        self.pacman_x = 330
        self.pacman_y = 335
        self.direction = "Right"
        self.player_speed = 5
        self.score = 0
        self.lives = 3
        self.time_survived = 0
        self.pacman_current_frame_index = 0
        self.paused = False
        self.boss_key_active = False
        self.ghost_speed = 1
        self.power_pellet_active = False
        self.power_pellet_timer = 0
        self.total_pellets = 184
        self.invulnerable = False
        self.teleport_count = 0  # Sets up 2nd cheat code

        # Base control settings
        self.controls = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right",
            "Pause": "p",
        }
        self.resetcontrols = self.controls.copy()

        # Define ghosts as a dictionary, each key holds 8 values: starting x and y, starting frames, chase, release time and state.
        self.ghosts = {
            "red": {
                "x": 300, "y": 225,
                "frame1": ImageTk.PhotoImage(Image.open("Coursework2/RedGhostFrame1.png").resize((30, 30))),
                "frame2": ImageTk.PhotoImage(Image.open("Coursework2/RedGhostFrame2.png").resize((30, 30))),
                "current_frame": 1, "chase": False, "release_time": time.time(), "state": "normal",
                "original_frames": [ImageTk.PhotoImage(Image.open("Coursework2/RedGhostFrame1.png").resize((30, 30))),
                                    ImageTk.PhotoImage(Image.open("Coursework2/RedGhostFrame2.png").resize((30, 30)))]
            },
            "blue": {
                "x": 260, "y": 290,
                "frame1": ImageTk.PhotoImage(Image.open("Coursework2/BlueGhostFrame1.png").resize((30, 30))),
                "frame2": ImageTk.PhotoImage(Image.open("Coursework2/BlueGhostFrame2.png").resize((30, 30))),
                "current_frame": 1, "chase": False, "release_time": time.time(), "state": "normal",
                "original_frames": [ImageTk.PhotoImage(Image.open("Coursework2/BlueGhostFrame1.png").resize((30, 30))),
                                    ImageTk.PhotoImage(Image.open("Coursework2/BlueGhostFrame2.png").resize((30, 30)))]
            },
            "orange": {
                "x": 300, "y": 290,
                "frame1": ImageTk.PhotoImage(Image.open("Coursework2/OrangeGhostFrame1.png").resize((30, 30))),
                "frame2": ImageTk.PhotoImage(Image.open("Coursework2/OrangeGhostFrame2.png").resize((30, 30))),
                "current_frame": 1, "chase": False, "release_time": time.time(), "state": "normal",
                "original_frames": [
                    ImageTk.PhotoImage(Image.open("Coursework2/OrangeGhostFrame1.png").resize((30, 30))),
                    ImageTk.PhotoImage(Image.open("Coursework2/OrangeGhostFrame2.png").resize((30, 30)))]
            },
            "pink": {
                "x": 340, "y": 290,
                "frame1": ImageTk.PhotoImage(Image.open("Coursework2/PinkGhostFrame1.png").resize((30, 30))),
                "frame2": ImageTk.PhotoImage(Image.open("Coursework2/PinkGhostFrame2.png").resize((30, 30))),
                "current_frame": 1, "chase": False, "release_time": time.time(), "state": "normal",
                "original_frames": [ImageTk.PhotoImage(Image.open("Coursework2/PinkGhostFrame1.png").resize((30, 30))),
                                    ImageTk.PhotoImage(Image.open("Coursework2/PinkGhostFrame2.png").resize((30, 30)))]
            }
        }

        # Initialise boss key
        self.Boss_Key_Image = ImageTk.PhotoImage(Image.open("Coursework2/BossKey.png").resize((600, 600)))

        # Initialise maze grid.
        # I set the canvas geometry to 600x600 and grid position size to 30x30, so there are 20 usable rows and columns
        self.maze_grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 5, 5, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 1, 5, 5, 5, 5, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 2, 0, 1, 1, 1, 1, 0, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # Restore-able maze grid for restarts
        self.original_maze_grid = [row[:] for row in self.maze_grid]
        # Take action based on the key that was pressed
        self.master.bind("<KeyPress>", self.key_press)
        # Flag to indicate if the game is over
        self.game_over = False
        # Initilaise menu at the top of the screen.
        self.create_menu_bar()

        self.game_loop()
        self.pause_menu = None
        self.pause_text = None

    def create_menu_bar(self):
        """
        Function to create the menu bar shown atop the screen.
        It can display the leaderboard or allow the user to customise their control keys (up,down,left,right,pause).
        """
        menu_bar = tk.Menu(self.master)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Controls List", command=self.show_controls)
        settings_menu.add_command(label="Customise Controls", command=self.customise_controls)
        settings_menu.add_command(label="Reset Controls", command=self.reset_controls)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        leaderboard_menu = tk.Menu(menu_bar, tearoff=0)
        leaderboard_menu.add_command(label="Show Leaderboard", command=self.show_leaderboard)
        # leaderboard_menu.add_command(label= "Highscores", command=self.show_highscores)
        menu_bar.add_cascade(label="Leaderboard", menu=leaderboard_menu)

        save_load_menu = tk.Menu(menu_bar, tearoff=0)
        save_load_menu.add_command(label="Save Game", command=self.save_game)
        save_load_menu.add_command(label="Load Game", command=self.load_game)
        menu_bar.add_cascade(label="Save/Load", menu=save_load_menu)

        self.master.config(menu=menu_bar)

    def show_controls(self):
        """
        Opens a Tkinter window that shows the user what they've currently bound their controls to.
        Shows some basic instructions on how to reset the controls.
        """
        self.toggle_pause()
        controls_window = tk.Toplevel(self.master)
        controls_window.title("Controls")

        canvas = tk.Canvas(controls_window, width=350, height=250, bg="black")
        canvas.pack()

        controls_text = f"""
        Move Up: {self.controls['Up']}
        Move Down: {self.controls['Down']}
        Move Left: {self.controls['Left']}
        Move Right: {self.controls['Right']}
        Pause: {self.controls['Pause']}
        Boss Key : b
        
        Default movement controls are the arrow keys!
        Reset to them using the 'Reset Controls' button
        or by typing "Up" "Down" "Left" "Right".
        """
        canvas.create_text(150, 100, text=controls_text, font=("Montserrat", 12), fill="white", justify="left")

    def customise_controls(self):
        """
        Automatically pauses the game and sends 5 Tkinter windows that allow the user to customise the
        pause, up, down, left and right keys.
        """
        self.toggle_pause()
        for action in self.controls.keys():
            new_key = simpledialog.askstring("Customise Controls", f"Enter a new key for {action}:")
            if new_key:
                self.controls[action] = new_key
        self.toggle_pause()

    def reset_controls(self):
        """
        Resets the movement and pause controls if the user responds "yes" to the Tkinter message box.
        """
        self.toggle_pause()
        if messagebox.askyesno("Reset Controls", "Do you want to reset controls to default?"):
            self.controls = self.resetcontrols.copy()
        self.toggle_pause()

    def show_leaderboard(self):
        """
        Creates a Tkinter window that displays the contents of leaderboard.txt in order of score
        """
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("Leaderboard")

        canvas = tk.Canvas(leaderboard_window, width=400, height=300, bg="black")
        canvas.pack()

        canvas.create_text(200, 20, text="Leaderboard", font=("Montserrat", 16), fill="white")

        y_position = 60
        for rank, (name, score, time_survived, level) in enumerate(self.current_session_scores, 1):
            canvas.create_text(200, y_position, text=f"{rank}. {name}: {score} (Time: {time_survived}, Level: {level})",
                               font=("Montserrat", 12), fill="white")
            y_position += 20  # move the next line of strings below the current one.

    def start_game(self):
        """
        Begins the game by pausing it until the user enters their name.
        Then begins incrementing the time survived.
        """
        if not self.player_name or self.player_name == "No name":
            self.toggle_pause()
            self.player_name = self.get_player_name()
            self.toggle_pause()

        self.start_time = time.time()
        self.time_survived = 0
        self.game_over = False
        self.paused = False

    def end_game(self):
        """
        Ends the game by saving the current session's scores to leaderboard.txt and then displaying the leaderboard.
        """
        final_score = self.score  # stop incrementing the score
        self.game_over = True

        time_survived = round(self.time_survived, 2)  # round to 2 d.p. for display

        if self.player_name:  # Only if the player entered a username
            with open(self.leaderboard_file, "a") as leaderboards:
                leaderboards.write(f"{self.player_name}:{final_score}:{time_survived}s:Level {self.level}\n")
                # Write scores to leaderboard.txt
            self.current_session_scores.append((self.player_name, final_score, f"{time_survived}s", self.level))
            # Append scores to current_session_scores array
            messagebox.showinfo("Game Over",
                                f"Game over, {self.player_name}!\nScore: {final_score}\nTime Survived: "
                                f"{time_survived}s\nLevel Reached: {self.level}")
            # Show the user their name, final score, time and level on screen.
            self.show_leaderboard()

    @staticmethod
    def get_player_name():
        """
        Utility function that prompts the user to input their name and returns it.
        Displays a warning message if nothing is entered.
        """
        name = simpledialog.askstring("Player Name", "Enter your name:")
        if not name:
            messagebox.showwarning("No Name", "You must enter a name to play!")
            # Prevent the user from playing without entering a name
            # (needed for leaderboard formatting)
            return PacManGame.get_player_name()
        return name

    def key_press(self, event):
        """
        Defines actions to take based on user key input, stored in event parameter
        """
        if event.keysym == 'b':
            self.show_boss_key()  # hide the screen with the boss key function
        elif event.keysym == self.controls["Pause"]:
            self.toggle_pause()  # pause the game if the dictionary value for pause is detected
        elif not self.paused and event.keysym in self.controls.values():
            # if the key pressed is in self.controls dictionary's values
            for action, key in self.controls.items():  # find they key related to the value
                if event.keysym == key:
                    self.direction = action  # assign self.direction from move_pacman function to action

    def pause_timer(self):
        """
        Prevents the time survived from being incremented when the game is paused.
        """
        self.paused = not self.paused  # switch between paused and unpaused states
        if self.paused:
            self.time_survived += time.time() - self.start_time  # dont increase time survived if paused
            self.show_pause_menu()
        else:
            self.start_time = time.time()  # set the start time to current time for resumed gameplay
            self.hide_pause_menu()

    def draw_pellets(self):
        """
        Checks each row and then each column of the maze grid, setting x and y to the center of each 30x30 tile.
        If the hardcoded int value is 2, draw a regular pellet, if 3 draw a power pellet and so on for the fruits.
        """
        self.canvas.delete("pellets")
        # delete all pellets (for restart_game, eat_pellets and update_status functions)
        for row in range(len(self.maze_grid)):
            for col in range(len(self.maze_grid[row])):
                x, y = col * 30 + 15, row * 30 + 15  # Center of each tile
                if self.maze_grid[row][col] == 2:
                    # self.canvas.create_image(x, y, image=self.pellet_image, tags="pellets")
                    self.canvas.create_oval(x, y, x + 5, y + 5, fill="pink", tags="pellets")
                    # draw a shape for the pellets
                elif self.maze_grid[row][col] == 3:
                    self.canvas.create_image(x, y, image=self.power_pellet_image, tags="pellets")
                    self.canvas.tag_raise("pellets", "background")  # implementing image hierarchy
                elif self.maze_grid[row][col] == 6:
                    self.canvas.create_image(x, y, image=self.cherry_image, tags="pellets")
                elif self.maze_grid[row][col] == 7:
                    self.canvas.create_image(x, y, image=self.strawberry_image, tags="pellets")
                elif self.maze_grid[row][col] == 8:
                    self.canvas.create_image(x, y, image=self.apple_image, tags="pellets")
                # w, z = col * 30, row * 30
                # if 19 > row > 1 == self.maze_grid[row][col] and 1 < col < 19:
                #     self.canvas.create_rectangle(w, z, w + 30, z + 30, fill="dark blue", tags="wall")
                # Implementing these shapes significantly slows performance.

    def toggle_pause(self):
        """
        Removes boss key, pauses, and resumes the game.
        """
        if self.boss_key_active:
            self.remove_boss_key()
            return

        self.paused = not self.paused
        if self.paused:
            self.show_pause_menu()
        else:
            self.hide_pause_menu()

    def show_pause_menu(self):
        """
        Creates the pause overlay and text.
        """
        self.pause_menu = self.canvas.create_rectangle(0, 0, 600, 600, fill="black", stipple="gray50",
                                                       tags="pause_menu")
        self.canvas.create_text(300, 300, text="PAUSED", font=("Montserrat", 40, "bold"), fill="white",
                                tags="pause_menu_text")
        self.canvas.tag_raise("pause_menu")
        self.canvas.tag_raise("pause_menu_text")

    def hide_pause_menu(self):
        """
        Deletes the pause overlay and text.
        """
        self.canvas.delete("pause_menu")
        self.canvas.delete("pause_menu_text")

    def show_boss_key(self):
        """
        Adds the boss key overlay above the pause overlay, while pausing the game.
        """
        if not self.boss_key_active:
            self.boss_key_active = True
            if not self.paused:
                self.paused = True
                self.show_pause_menu()
            self.canvas.create_image(0, 0, image=self.Boss_Key_Image, anchor="nw", tags="boss_key")
        else:
            self.remove_boss_key()

    def remove_boss_key(self):
        """
        Removes the boss key overlay above the pause overlay, keeping the game paused.
        """
        self.canvas.delete("boss_key")
        self.boss_key_active = False
        self.paused = True
        self.show_pause_menu()

    def update_status(self):
        """
        Updates the player's score and lives on-screen when called in restart_game, eat_pellets and check_collision.
        """
        self.canvas.delete("status")
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", fill="white", anchor="nw", font=("Helvetica", 14),
                                tags="status")
        self.canvas.create_text(520, 10, text=f"Lives: {self.lives}", fill="white", anchor="nw", font=("Helvetica", 14),
                                tags="status")

    def move_pacman(self):
        """
        Prevents Pacman from moving if the game is paused or ended.
        Contains a cheat codes to double player_speed.
        Handles Pacman's movement in all 4 directions.
        Checks if Pacman is not colliding with a wall, or goes out of bounds.
        """
        if self.paused or self.game_over:  # stop moving Pacman if the game is over or paused
            return

        if self.player_name == "Pac":  # check for the 1st cheat code
            speed_multiplier = 2  # double the speed
        else:
            speed_multiplier = 1

        new_x, new_y = self.pacman_x, self.pacman_y
        if self.direction == 'Up':
            new_y -= 5 * speed_multiplier
        elif self.direction == 'Down':
            new_y += 5 * speed_multiplier
        elif self.direction == 'Left':
            new_x -= 5 * speed_multiplier
        elif self.direction == 'Right':
            new_x += 5 * speed_multiplier

        if not self.is_wall(new_x, new_y) and self.pacman_x >= 0:
            # If pacman is currently in the maze and has not collided with a wall
            self.pacman_x, self.pacman_y = new_x, new_y  # keep moving in the same direction
            self.pacman_current_frame_index = (self.pacman_current_frame_index + 1) % len(
                self.pacman_frames[self.direction])  # continue looping through animation frames
        else:
            self.pacman_current_frame_index = 1  # stop looping through animation frames

            if self.pacman_x < 0:  # teleport from left to right
                self.pacman_x = 600
                self.teleport_count += 1
            elif self.pacman_x >= 590:  # teleport from right to left
                self.pacman_x = 10
                self.teleport_count += 1
            if self.teleport_count >= 20:
                self.invulnerable = True

    def is_wall(self, x, y):
        """Checks if the grid's x and y are on a wall in the maze."""
        grid_x, grid_y = self.get_grid_position(x, y)
        # Converts pixel coords to grid coords
        if 0 <= grid_x < len(self.maze_grid[0]) and 0 <= grid_y < len(self.maze_grid):
            # If grid coors are within maze boundaries.
            return self.maze_grid[grid_y][grid_x] == 1
            # if pixel coords represent a wall in the grid
        return False  # if coords aren't within game boundaries, return false

    def get_grid_position(self, x, y):
        """Converts pixel coords to grid coords"""
        return x // 30, y // 30  # get the largest integer <= x/30 and y/30

    def eat_pellets(self):
        """
        Updates player stats when eating pellets or fruits.
        Checks cells adjacent to Pacman’s grid position for consumables
        Increments score when Pacman collides with pellets/fruits
        Handles power pellet mode.
        """
        # reuse get_grid_position for pacman position
        pacman_grid_x = self.pacman_x // 30
        pacman_grid_y = self.pacman_y // 30

        # spawn bonus fruits
        if self.total_pellets == 135:
            self.maze_grid[7][10] = 6  # cherry
            self.maze_grid[11][22] = 6  # restart safety
        elif self.total_pellets == 90:
            self.maze_grid[3][8] = 7  # apple
        elif self.total_pellets == 45:
            self.maze_grid[18][9] = 8  # strawberry

        # Check adjacent grid cells for pellets/fruits, based on pacman direction
        adjacent_cells = [
            (pacman_grid_x, pacman_grid_y),
            (pacman_grid_x + 1, pacman_grid_y),
            (pacman_grid_x - 1, pacman_grid_y),
            (pacman_grid_x, pacman_grid_y + 1),
            (pacman_grid_x, pacman_grid_y - 1)
        ]

        pellet_eaten = False

        for grid_x, grid_y in adjacent_cells:
            # Check if the position is within grid bounds
            if (0 <= grid_y < len(self.maze_grid) and
                    0 <= grid_x < len(self.maze_grid[0])):

                # Check for regular pellet
                if self.maze_grid[grid_y][grid_x] == 2:
                    # Calculate the centre position of the pellet
                    pellet_centre_x = grid_x * 30 + 15
                    pellet_centre_y = grid_y * 30 + 15

                    # Check if Pacman is close enough to eat the pellet
                    distance = ((self.pacman_x - pellet_centre_x) ** 2 +
                                (self.pacman_y - pellet_centre_y) ** 2) ** 0.5

                    if distance < 15:
                        self.maze_grid[grid_y][grid_x] = 0  # Remove pellet from grid
                        self.score += 50
                        self.total_pellets -= 1
                        pellet_eaten = True

                # Check for power pellet
                elif self.maze_grid[grid_y][grid_x] == 3:
                    # Calculate the centre position of the power pellet
                    pellet_centre_x = grid_x * 30 + 15
                    pellet_centre_y = grid_y * 30 + 15

                    # Check if Pacman is close enough to eat the power pellet
                    distance = ((self.pacman_x - pellet_centre_x) ** 2 + (self.pacman_y - pellet_centre_y) ** 2) ** 0.5

                    if distance < 15:  # If Pacman is close enough to the pellet
                        self.maze_grid[grid_y][grid_x] = 0  # Remove power pellet from grid
                        self.score += 100
                        self.total_pellets -= 1
                        pellet_eaten = True
                        for ghost_name, ghost in self.ghosts.items():
                            ghost["eaten"] = False
                        self.power_pellet_active = True  # raise the power_pellet_active flag for 10s
                        self.power_pellet_timer = time.time()

                # Same rules as above for bonus fruits
                elif self.maze_grid[grid_y][grid_x] == 6:  # Cherry
                    fruit_centre_x = grid_x * 30 + 15
                    fruit_centre_y = grid_y * 30 + 15

                    distance = ((self.pacman_x - fruit_centre_x) ** 2 + (self.pacman_y - fruit_centre_y) ** 2) ** 0.5
                    if distance < 15:
                        self.maze_grid[grid_y][grid_x] = 0
                        self.score += 500
                        pellet_eaten = True

                elif self.maze_grid[grid_y][grid_x] == 7:  # Apple
                    fruit_centre_x = grid_x * 30 + 15
                    fruit_centre_y = grid_y * 30 + 15

                    distance = ((self.pacman_x - fruit_centre_x) ** 2 + (self.pacman_y - fruit_centre_y) ** 2) ** 0.5
                    if distance < 15:
                        self.maze_grid[grid_y][grid_x] = 0
                        self.score += 1000
                        pellet_eaten = True

                elif self.maze_grid[grid_y][grid_x] == 8:  # Strawberry
                    fruit_centre_x = grid_x * 30 + 15
                    fruit_centre_y = grid_y * 30 + 15

                    distance = ((self.pacman_x - fruit_centre_x) ** 2 + (self.pacman_y - fruit_centre_y) ** 2) ** 0.5
                    if distance < 15:
                        self.maze_grid[grid_y][grid_x] = 0
                        self.score += 1000
                        pellet_eaten = True

        if pellet_eaten:
            self.update_status()  # update the score display
            self.draw_pellets()  # redraw the pellets to show the eaten one is gone

    def get_remaining_pellets(self):
        """
        Check each row of the maze grid for consumables, incrementing the counter if there is a consumable.
        """
        pellet_count = 0
        for row in self.maze_grid:
            pellet_count += row.count(2) + row.count(3)  # Count both regular and power pellets
        return pellet_count

    def check_win_condition(self):
        """
        Check if the player has consumed all pellets in the game area.
        If so, restart the game with a slightly increased difficulty
        """
        if self.get_remaining_pellets() == 0:
            self.game_over = True
            self.canvas.create_text(300, 250, text="Level Complete! +1 Life!", font=("Montserrat", 24),
                                    fill="yellow",
                                    tags="winlevelmsg")  # Displaying on-screen winner's message
            self.canvas.tag_raise("winlevelmsg", "pacman")
            self.canvas.tag_raise("winlevelmsg", "ghosts")
            self.canvas.tag_raise("winlevelmsg", "background")  # image hierarchy
            self.master.after(4000, lambda: self.restart_game(increase_difficulty=True))

    def save_game(self):
        """
        Pauses the current session.
        Saves the current state of the game into a .json file, which can then be reloaded
        To resume the user's progress.
        """
        self.toggle_pause()
        # The .json file is dynamically updated with all the following instance variables (as strings)
        game_state = {
            "player_name": self.player_name,
            "score": self.score,
            "lives": self.lives,
            "level": self.level,
            "maze_grid": self.maze_grid,
            "controls": self.controls,
            "teleport_count": self.teleport_count,
            "time_survived": self.time_survived,
            "pacman_position": {"x": self.pacman_x, "y": self.pacman_y},
            "pacman_direction": self.direction,
            "power_pellet_timer": self.power_pellet_timer,
            "ghosts": {
                name: {"x": ghost["x"], "y": ghost["y"], "chase": ghost["chase"], "state": ghost["state"]}
                for name, ghost in self.ghosts.items()
            },
        }

        try:  # Handles potential errors in saving
            with open("save_game.json", "w") as save_file:
                json.dump(game_state, save_file)  # Stores all the game data into the .json file.
            messagebox.showinfo("Game Saved", "Your game has been saved!")
        except Exception as e:  # Handle error - undefined variable
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
        self.toggle_pause()

    def load_game(self):
        """
        Pauses the current game, loads the user's game from the json file, allowing them to continue their progress.
        """
        try:  # Handles potential errors in loading
            with open("save_game.json", "r") as save_file:
                game_state = json.load(save_file)  # Loads all game_state data from the .json file.

            # Restore from the .json file all the following instance variables
            self.toggle_pause()
            self.player_name = game_state["player_name"]
            self.score = game_state["score"]
            self.lives = game_state["lives"]
            self.level = game_state["level"]
            self.controls = game_state["controls"]
            self.maze_grid = game_state["maze_grid"]
            self.pacman_x = game_state["pacman_position"]["x"]
            self.pacman_y = game_state["pacman_position"]["y"]
            self.direction = game_state["pacman_direction"]
            self.teleport_count = game_state["teleport_count"]
            self.time_survived = game_state["time_survived"]
            self.power_pellet_timer = game_state["power_pellet_timer"]

            for name, ghost_state in game_state["ghosts"].items():
                self.ghosts[name]["x"] = ghost_state["x"]
                self.ghosts[name]["y"] = ghost_state["y"]
                self.ghosts[name]["chase"] = ghost_state["chase"]
                self.ghosts[name]["state"] = ghost_state["state"]

            # Redraw canvas to reflect the previous game state
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw", tags="background")
            self.update_status()
            self.draw_pellets()
            self.draw_pacman()
            self.draw_ghosts()
            self.move_pacman()
            self.move_ghosts()

            messagebox.showinfo("Game Loaded", "Your game has been loaded!")  # If non-empty json found
        except FileNotFoundError:  # Handle errors - empty json
            messagebox.showwarning("No Save Found", "No saved game found. Save a game first.")
        except Exception as e:  # Handle errors - undefined variables
            messagebox.showerror("Error", f"An error occurred while loading: {e}")
        self.toggle_pause()

    def restart_game(self, increase_difficulty=False):
        """
        Restart the game with increased difficulty parameter initialised to false.
        If the player won the level i.e. game_over = False
        Increase the difficulty and do not reset their stats
        Else, reset the player's stats (name, level, score, time and controls)
        In both cases, reset the maze grid, pellets, pacman position and ghost position.
        """
        self.teleport_count = 0
        if not increase_difficulty and self.game_over:
            self.lives = 3
            self.game_over = False
            self.paused = False
            self.player_name = "No name"  # reset the username for the next player
            self.time_survived = 0
            self.start_time = 0
            self.level = 1
            self.controls = {
                "Up": "Up",
                "Down": "Down",
                "Left": "Left",
                "Right": "Right",
                "Pause": "p",
            }
        else:  # if increased_difficulty remains true
            self.start_time = time.time()
            self.time_survived += time.time() - self.start_time
            self.player_name = self.player_name
            self.player_speed = self.player_speed
            self.score = self.score
            self.lives += 1
            self.controls = self.controls
            self.level += 1
            for ghost in self.ghosts.values():
                ghost["release_time"] -= 5  # Ghosts are released earlier
                self.ghost_speed += 0.5  # Increase ghost speed

        self.pacman_x, self.pacman_y = 330, 335
        self.direction = "Right"
        self.total_pellets = self.total_pellets + (184 - self.get_remaining_pellets())  # return to 184 pellets
        self.maze_grid = [row[:] for row in self.original_maze_grid]
        power_pellet_locations = {(2, 2), (2, 19), (19, 2), (19, 19)}  # define grid locations of power pellets

        for row in range(len(self.maze_grid)):
            for col in range(len(self.maze_grid[row])):
                if self.maze_grid[row][col] == 0:
                    if (row, col) in power_pellet_locations:
                        self.maze_grid[row][col] = 3  # redraw power pellet
                    else:
                        self.maze_grid[row][col] = 2  # redraw regular pellet

        # Reset ghost positions, states and release time.
        for ghost_name, ghost in self.ghosts.items():
            if ghost_name == "red":
                ghost["x"], ghost["y"] = 300, 225
            elif ghost_name == "blue":
                ghost["x"], ghost["y"] = 260, 290
            elif ghost_name == "orange":
                ghost["x"], ghost["y"] = 300, 290
            elif ghost_name == "pink":
                ghost["x"], ghost["y"] = 340, 290
            ghost["chase"] = False
            ghost["eaten"] = False
            ghost["release_time"] = time.time()

        # Redraw UI and restart the game loop
        self.canvas.delete("pellets")
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw", tags="background")
        self.update_status()
        self.draw_pellets()
        self.draw_pacman()
        self.draw_ghosts()
        self.start_game()

    def calculate_ghost_speed(self):
        """
        Calculate the speed of the ghost based on the remaining pellets and power pellet status.
        The ghost's speed increases as remaining pellets decrease.
        Their speed halves when a power pellet is active.
        """
        total_pellets = 184  # initial number of pellets in the maze
        remaining = self.get_remaining_pellets()
        if self.power_pellet_active:
            # Ghost's speed increased by up to 1 per level as pellets decrease
            return self.ghost_speed + (1 * (1 - (remaining / total_pellets)))
        else:
            return self.ghost_speed + (1 * (1 - (remaining / total_pellets))) / 2  # Halve ghost speed if vulnerable

    def draw_pacman(self):
        """
        Refresh Pacman sprite on-screen, and begin cycling through its frames.
        Change frames based on direction.
        """
        self.canvas.delete("pacman")
        frames = self.pacman_frames[self.direction]
        pacman_photo = frames[self.pacman_current_frame_index]
        self.canvas.create_image(self.pacman_x, self.pacman_y, image=pacman_photo, tags="pacman")
        self.pacman_current_frame_index = (self.pacman_current_frame_index + 1) % len(frames)
        self.canvas.tag_raise("pacman", "pellets")  # implementing image hierarchy

        # Begin A* search algorithm, using the Manhattan distance manhattan, for Red.
        # A* prerequisites

    def manhattan(self, a, b):
        """
            Returns the distance from the start point (a[0],b[0]) travelling along the
            adjacent and opposite edges to the end point (a[1],b[1]).
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, grid, node):
        """
        Return a list of valid neighbour nodes for each node based on maze boundaries
        """
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # check right, left, up, down directions
        for dx, dy in directions:
            new_x, new_y = node[0] + dx, node[1] + dy
            if (0 <= new_y < len(grid) and
                    0 <= new_x < len(grid[0]) and
                    grid[new_y][new_x] != 1):  # if tile is not a wall
                neighbors.append((new_x, new_y))  # append it to neighbours array
        return neighbors

    def reconstruct_path(self, came_from, current):
        """
            Returns the list of nodes containing the path from start to end point.
            came_from dictionary maps the node from the current node to the previous node
        """
        path = [current]
        while current in came_from:
            current = came_from[current]  # travelling backwards from current path
            path.append(current)
        path.reverse()
        return path  # return path from start to end point

    def a_star(self, grid, start, goal):
        """
            Returns the shortest path from start point (ghost grid position) to end point
            (target_x, target_y) as a list of grid positions using A* algorithm.
            Every node begins in the closed set of visited nodes
            Selects nodes with the lowest g score and add them to the open set.
            Calculate the path with the lowest g score and constructs it.
        """
        # Convert pixel coordinates to grid coordinates
        start = (int(start[0] // 30), int(start[1] // 30))
        goal = (int(goal[0] // 30), int(goal[1] // 30))

        # Initialize the open set with the start node
        open_set = {start}
        came_from = {}  # Will contain the reconstructed path, once backtracking is complete

        # Initialize f and g scores
        g_score = {start: 0}
        f_score = {start: self.manhattan(start, goal)}
        # Return the manhattan distance from each point

        while open_set:  # While unvisited nodes remain
            # Get node with lowest f_score
            current = min(open_set, key=lambda node: f_score.get(node, float('inf')))

            if current == goal:  # If the shortest path was found
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            # Move the current node to the closed set
            for neighbor in self.get_neighbors(grid, current):
                # Calculate tentative g_score for each neighbour
                tentative_g_score = g_score[current] + 1
                # As each neighbour has the same cost of 1.

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    # Optimal path found, update came_from and scores.
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.manhattan(neighbor, goal)

                    if neighbor not in open_set:
                        # Add neighbour to open set if not already in it.
                        open_set.add(neighbor)

        return []  # No path found

    # Begin dikstra's pathfinding algorithm
    def dijkstra(self, start, goal):
        """
            Returns the shortest path from start point (ghost grid position) to end point
            (target_x, target_y) as a list of grid positions using Dijkstra's algorithm.
            Every node begins in the set of unvisited nodes.
            The algorithm continues as long as there are unvisited nodes.
            Once the shortest path is found it is reconstructed.
        """
        # Convert pixel coords to grid tiles
        start = (int(start[0] // 30), int(start[1] // 30))
        goal = (int(goal[0] // 30), int(goal[1] // 30))

        distances = {start: 0}  # The current shortest path from start to end node
        previous = {start: None}  # Reconstruct the path
        nodes = {(x, y) for y in range(len(self.maze_grid))
                 for x in range(len(self.maze_grid[0]))
                 if self.maze_grid[y][x] != 1}
        # If grid tile is not a wall, add it to the set.

        while nodes:
            current = min(nodes, key=lambda node: distances.get(node, float('inf')))
            # Select the unvisited node with the smallest distance from start
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = previous[current]
                return path[::-1]

            nodes.remove(current)
            # Mark current node as visited by removing it from dictionary

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                # Check the four neighbours of the current node
                neighbor = (current[0] + dx, current[1] + dy)
                # Calculate maze coords of the neighbour
                if (neighbor in nodes and
                        0 <= neighbor[1] < len(self.maze_grid) and
                        0 <= neighbor[0] < len(self.maze_grid[0]) and
                        self.maze_grid[neighbor[1]][neighbor[0]] != 1):
                    # If the neighbour is a path in game boundaries and is unexplored
                    alt = distances[current] + 1
                    # Calculate distance to the neighbour from current node
                    if alt < distances.get(neighbor, float('inf')):
                        # If this path is better than the previous one
                        distances[neighbor] = alt
                        previous[neighbor] = current
                        # Update the dictionaries with this new node.
        return []

    def move_ghosts(self):
        """
            Moves the ghosts based on their current state, target, and pathfinding algorithm.
            Handles the movement of the four ghosts based on their state and power pellet status.
            Defines the target position for each ghost and moves the ghost along the calculated path.
        """
        if self.paused or self.game_over or self.boss_key_active:
            return  # Ghosts stop moving if game is paused (by boss key too) or game over.

        current_time = time.time()
        release_delays = {
            "red": 5,
            "blue": 10,
            "orange": 15,
            "pink": 20
        }

        speed = self.calculate_ghost_speed()
        current_time = time.time()

        for ghost_name, ghost in self.ghosts.items():
            if current_time - ghost["release_time"] > release_delays[
                ghost_name.lower()]:  # freeing ghosts at respective times
                ghost["chase"] = True
            if not ghost["chase"]:  # i.e. chase mode is False
                pen_moves = [(0, speed), (0, -speed), (speed, 0), (-speed, 0)]  # 4 directions considered
                valid_moves = []  # Store valid moves in the list

                for move_x, move_y in pen_moves:  # Check each move
                    new_x = ghost["x"] + move_x
                    new_y = ghost["y"] + move_y
                    # If new coords are within pen boundaries
                    if 260 <= new_x <= 340 and 270 <= new_y <= 310:
                        valid_moves.append((move_x, move_y))  # Add this as a valid move

                if valid_moves:  # Move the ghosts around randomly in the pen
                    move_x, move_y = random.choice(valid_moves)
                    ghost["x"] += move_x
                    ghost["y"] += move_y
                continue

            target_x = self.pacman_x
            target_y = self.pacman_y

            if ghost_name == "blue":
                if self.direction == "Right":
                    target_x, target_y = self.pacman_x + 30, self.pacman_y
                elif self.direction == "Left":
                    target_x, target_y = self.pacman_x - 30, self.pacman_y
                elif self.direction == "Up":
                    target_x, target_y = self.pacman_x, self.pacman_y - 30
                else:
                    target_x, target_y = self.pacman_x, self.pacman_y + 30

            elif ghost_name == "pink":
                if self.direction == "Right":
                    target_x, target_y = self.pacman_x - 30, self.pacman_y
                elif self.direction == "Left":
                    target_x, target_y = self.pacman_x + 30, self.pacman_y
                elif self.direction == "Up":
                    target_x, target_y = self.pacman_x, self.pacman_y + 30
                else:
                    target_x, target_y = self.pacman_x, self.pacman_y - 30

            elif ghost_name == "orange":
                distance = ((self.pacman_x - ghost["x"]) ** 2 +
                            (self.pacman_y - ghost["y"]) ** 2) ** 0.5
                if distance > 200:  # Stops moving if Pacman goes too far
                    target_x, target_y = 300, 300
                # else use default pacman position

            # set ghost path's based on colour, not like the original game.
            path = []
            if ghost_name == "red" or "blue" and ghost["chase"] == True:  # Red and blue pathfind using A*
                path = self.a_star(self.maze_grid, (ghost["x"], ghost["y"]), (target_x, target_y))
            elif ghost_name == "orange" or "pink":  # Orange and pink pathfind using Dijkstra's
                path = self.dijkstra((ghost["x"], ghost["y"]), (target_x, target_y))

            # Move ghost along path
            if path and len(path) > 1:
                next_cell = path[1]
                next_x = next_cell[0] * 30 + 15
                next_y = next_cell[1] * 30 + 15

                # Move towards next cell
                if next_x > ghost["x"]:
                    ghost["x"] += speed
                elif next_x < ghost["x"]:
                    ghost["x"] -= speed
                if next_y > ghost["y"]:
                    ghost["y"] += speed
                elif next_y < ghost["y"]:
                    ghost["y"] -= speed

            if self.power_pellet_active and (current_time - self.power_pellet_timer < 10):
                ghost["state"] = "scared"
                ghost["chase"] = False  # disable chase mode
                ghost["frame1"] = ImageTk.PhotoImage(Image.open("Coursework2/ScaredGhostFrame1.png").resize((30, 30)))
                ghost["frame2"] = ImageTk.PhotoImage(Image.open("Coursework2/ScaredGhostFrame2.png").resize((30, 30)))
            else:
                ghost["chase"] = True  # return to chasing pacman
                ghost["state"] = "normal"
                ghost["frame1"] = ghost["original_frames"][0]
                ghost["frame2"] = ghost["original_frames"][1]

    def draw_ghosts(self):
        """
        Refreshes and draws ghosts' sprites on-screen.
        Cycle through regular ghost frames for each ghost.
        """
        self.canvas.delete("ghosts")
        for name, ghost in self.ghosts.items():
            ghost_photo = ghost["frame1"] if ghost["current_frame"] == 1 else ghost["frame2"]
            self.canvas.create_image(ghost["x"], ghost["y"], image=ghost_photo, tags="ghosts")
            ghost["current_frame"] = 3 - ghost["current_frame"]
            self.canvas.tag_raise("ghosts", "pacman")  # implementing image hierarchy

    def check_collision(self):
        """
        Checks for collisions between Pacman and ghosts in the game.
        If collision is true, check whether ghost is normal/scared and whether power pellet is active.
        Updates the game state, score, lives, and handles game over scenarios accordingly.
        """
        if not self.invulnerable or self.power_pellet_active:
            for ghost in self.ghosts.values():
                if abs(self.pacman_x - ghost["x"]) < 15 and abs(self.pacman_y - ghost["y"]) < 15:
                    if self.power_pellet_active and ghost["state"] == "scared":
                        self.score += 200
                        self.update_status()
                        self.respawn_ghost(ghost)
                        ghost["eaten"] = True
                    elif not self.invulnerable and ghost["state"] == "normal":
                        # Normal collision with a normal ghost
                        self.lives -= 1
                        self.update_status()

                        if self.lives > 0:
                            self.canvas.create_text(300, 250, text=f"You hit a ghost! Lives left: {self.lives}",
                                                    font=("Montserrat", 24), fill="red", tags="message")
                            self.master.after(2000, self.clear_message)
                            self.pacman_x, self.pacman_y = 330, 335
                        else:
                            self.game_over = True
                            self.canvas.create_text(300, 250, text="Game Over", font=("Montserrat", 24), fill="red",
                                                    tags="message")
                            self.end_game()
                            self.master.after(3000, self.restart_game)

    def clear_message(self):
        """
        Delete the game over message.
        """
        self.canvas.delete("message")

    def respawn_ghost(self, ghost):
        """
        Re-initialise all ghost attributes.
        """
        ghost["x"] = 300
        ghost["y"] = 290
        ghost["respawn_time"] = time.time() + 5
        # reset chase mode
        ghost["eaten"] = False
        ghost["state"] = "normal"
        ghost["frame1"] = ghost["original_frames"][0]
        ghost["frame2"] = ghost["original_frames"][1]
        ghost["chase"] = False

    def game_loop(self):
        """
        Continuously updates the game state by handling movement, collisions, scoring, lives, time etc.
        Also handles the game's drawing logic and pauses the game if required.
        """
        if not (self.game_over or self.paused or self.boss_key_active):
            self.time_survived = time.time() - self.start_time  # Update survival time
            self.move_pacman()
            self.move_ghosts()
            self.check_collision()
            self.eat_pellets()
            self.check_win_condition()

        self.draw_pellets()
        self.draw_pacman()
        self.draw_ghosts()

        if self.paused and not self.canvas.find_withtag("pause_menu"):
            self.show_pause_menu()

        self.master.after(100, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    game = PacManGame(root)
    game.start_game()
    root.mainloop()
