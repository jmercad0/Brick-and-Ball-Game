# ----------------------------------------------------------------------
# Name:         CS 122: HW #8 (GUI Application)
# Author:       Jordan Mercado
# Purpose:      To implement a GUI Application with Tkinter & argparse
#               Play by moving player with left and right arrow.  Earn
#               50 points for each brick destroyed by ball collision.
#               Game is over once ball exits screen. (victory if all
#               points acquired, game over otherwise)
#
# Date:         3/29/2019
# ----------------------------------------------------------------------

from tkinter import *
import argparse


class Game:

    """
    Class to support a general purpose GUI Game Application

    Argument:
    parent: (tkinter.tk): root tkinter object
    name    (str): name of player
    rows    (int): # of rows of bricks

    Attributes:
    rparent (tkinter): root tkinter object
    rows    (int): number of rows of bricks
    name    (str): name of player
    canvas  (tkinter.Canvas): the widget containing play area
    start_button (tkinter.Button): button to initiate game
    status  (tkinter.Label): label defining status of game
    score   (int):  score earned in game
    score_display (tkinter.Label): label displaying score earned
    velx    (int): horizontal velocity of ball
    vely    (int): vertical velocity of ball
    ball_id (int): id to reference ball within canvas
    """
    def __init__(self,parent,name,rows):
        # Initialize parent and command line variables
        self.rparent = parent
        self.rows = rows
        self.name = name
        parent.title("HW8: Game")

        # Create Canvas to hold game
        self.canvas = Canvas(width = 400)
        self.canvas.grid(row = 0)

        # Create Start button and associate with start method
        self.start_button = Button(parent, text='START', width=20,
                                      command=self.start)
        self.start_button.grid(row = 1,sticky = 'W')

        # Create a status label to show the current status
        self.status = Label(parent,text='Ready to start')

        self.status.grid(row = 3, sticky = 'W')
        # Initialize score parameters
        self.score = 0
        self.score_display = Label(parent, text=f"{self.name}'s Score: "
                                f"{self.score}")
        self.score_display.grid(row = 4, sticky = 'W')

        # Initialize velocity of ball
        self.velx = -5
        self.vely = -7

        # Initilialize ball_id
        self.ball_id = 0

        # Bind keystrokes to move player
        self.rparent.bind("<Key>", self.move_player)


    def reset(self):
        """
        Resets parameters and objects of game and restarts game
        :return: None
        """
        # Delete all objects from canvas
        for obj in self.canvas.find_all():
            self.canvas.delete(obj)

        # Re initialize velocity variables
        self.velx = -5
        self.vely = -7

        # Restart score parameters
        self.score = 0
        self.score_display.configure(text=f"{self.name}'s "
        f"Score: {self.score}")

        # Start game again
        self.start()


    def start(self):
        """
        Initializes paramters & objects for game and initiates animation
        :return: None
        """
        # Configure status label and remove start button
        self.status.configure(text='In progress',foreground='green')
        self.start_button.grid_forget()

        # Create bricks in canvas
        for i in range(8):
            for j in range(self.rows):
                # Alternate SJSU colors for rows of bricks
                if j % 2 == 0:
                    self.canvas.create_rectangle(0+(50*i), 0+(25*j), 50+(i*50),
                                     25+(j*25), fill='blue', outline='yellow')
                else:
                    self.canvas.create_rectangle(0+(50*i), 0+(25*j), 50+(i*50),
                                     25+(j*25), fill='yellow', outline='blue')

        # Create ball & initialize coordinates
        self.ball_id = self.canvas.create_oval(170, 225, 185, 240,
                                               fill='white', outline='cyan')
        self.ball_coordinates = (170, 225, 185, 240)

        # Create controllable player
        self.player = self.canvas.create_oval(165, 250, 235, 260,
                      fill = 'yellow', outline = 'cyan', tag = 'player')

        # Create reset button
        self.reset_button = self.start_button = Button(self.rparent,
                                    text='RESET', width=20, command=self.reset)
        self.reset_button.grid(sticky = 'W')

        # Create SJSU insignia for game
        self.sjsu_image =  PhotoImage(file="sjsuspartan.gif", width=150,
                                     height=125)
        self.sjsu_image2 = PhotoImage(file="sjsu.gif", width=150,
                                     height=125)
        self.sjsu1 = Label(self.rparent, image=self.sjsu_image)
        self.sjsu2 = Label(self.rparent, image=self.sjsu_image2)
        self.sjsu1.grid(row=0, column=1, sticky = 'NE')
        self.sjsu2.grid(row=0, column=1, sticky='SE')
        self.sjsu_text = Label(self.rparent, text="SJSU CS122: #HW8 GUI APP")
        self.sjsu_text.grid(row = 0, column = 1, sticky = 'E')

        # Begin animation of game
        Game.animate(self)



    def animate(self):
        """
        Simulates movement, physics and hit collision of ball and bricks
        :return: None
        """
        # Move ball by velocity values
        self.canvas.move(self.ball_id, self.velx, self.vely)
        # Update ball coordinates to follow move
        self.ball_coordinates = (self.ball_coordinates[0] + self.velx,
                                 self.ball_coordinates[1] + self.vely,
                                 self.ball_coordinates[2] + self.velx,
                                 self.ball_coordinates[3] + self.vely)
        # Find object collisions with balls coordinates
        overlap = self.canvas.find_overlapping(self.ball_coordinates[0],
                                               self.ball_coordinates[1],
                                               self.ball_coordinates[2],
                                               self.ball_coordinates[3])

        # Check for collision if overlap includes object besides ball
        if len(overlap)>1:
            for obj in overlap:
                object_coords = self.canvas.coords(obj)
                # If obj is brick, delete obj and add 50 points to score
                if obj != self.ball_id and obj != self.player:
                    self.canvas.delete(obj)
                    self.score += 50
                    self.score_display.configure(text = f"{self.name}'s "
                                                 f"Score: {self.score}")
                # Collision detection for ball hits side of brick
                if ((self.ball_coordinates[0] < object_coords[0] or
                     self.ball_coordinates[2] > object_coords[2]) and
                    (self.ball_coordinates[3] < object_coords[3] or
                     self.ball_coordinates[1] > object_coords[1])):
                   self.velx = self.velx * -1
                   self.vely = self.vely * -1

            # Update velocity to simulate bounce off object
            self.vely = self.vely * -1

        # Find canvas height and width measures
        self.canv_height = self.canvas.winfo_height()
        self.canv_width = self.canvas.winfo_width()

        # Check for collision of canvas walls
        if self.ball_coordinates[0] < 0 or \
                self.ball_coordinates[2] > self.canv_width:
            self.velx = self.velx * -1

        # Update canvas for movement or end game if ball is off screen
        if self.ball_coordinates[1] > self.canv_height or \
                self.ball_coordinates[3] < 0:
            self.stop()
        else:
            self.canvas.after(80, self.animate)






    def move_player(self, event):
        """
        Moves player object left and right

        :param event: captures keystrokes to apply to player object
        :return: None
        """
        key = event.keysym
        # Move player left if within canvas
        if key == "Left" and self.canvas.coords(self.player)[0] > 0:
            self.canvas.move(self.player, -15, 0)
        # Move player right if within canvas
        elif key == "Right" and self.canvas.coords(self.player)[2] < \
                self.canv_width:
            self.canvas.move(self.player, 15, 0)


    def stop(self):
        """
        Signals victory or game over when ball leaves canvas
        :return: None
        """
        # Signal victory if scored all possible points
        if self.score == (50*8)*self.rows:
            self.status.configure(text='Victory!', foreground = 'yellow')
        # Else signal game over
        else:
            self.status.configure(text='Game Over!', foreground='red')



def main():
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Gets args for Brick '
                                                 'Breaker Game')
    parser.add_argument('name', help='name of player',
                        nargs='?', default='Sammy the Spartan')
    parser.add_argument('size', help='# of rows in grid',
                        type=int, nargs='?', default=4)
    # Extract command line arguments
    args = parser.parse_args()
    name = args.name
    rows = min(args.size,7)

    # Create gui application main window and initialize game class
    root = Tk()
    game = Game(root,name,rows)

    # Enter main event loop
    root.mainloop()



if __name__=="__main__":
    main()
