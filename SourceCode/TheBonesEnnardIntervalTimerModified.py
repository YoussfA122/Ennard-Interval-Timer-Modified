import os
import sys
import tkinter as tk
from datetime import timedelta
from threading import Thread
import keyboard
import pygame


class DualStopwatchApp:
    def __init__(self, master):

        self.master = master
        self.master.title("TheBones5 Ennard Interval Timer")
        self.master.attributes('-topmost', True)  # Make the window always on top

        self.resource_path = self.get_resource_path()

        self.intro_label = tk.Label(master, text="Welcome to TheBones5 Ennard Interval Timer! Subscribe to TheBones5 YouTube channel on YouTube.", font=('Helvetica', 24))
        self.intro_label.pack(pady=20)

        self.intro_label = tk.Label(master, text="Press Q to Start the timer you can start the timer even if the program isn't focused", font=('Helvetica', 24))
        self.intro_label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_timers)
        self.start_button.pack(pady=10)

        self.sound1_button = tk.Button(master, text="If you want to hear the sound that plays when the 30 seconds that Ennard don't move ends", command=self.test_beeb_sound1)
        self.sound1_button.pack(pady=10)

        self.sound2_button = tk.Button(master, text="If you want to hear the sound that plays when Ennard has a movement opportunity", command=self.test_beeb_sound2)
        self.sound2_button.pack(pady=10)

        self.global_timer_value = tk.StringVar()
        self.interval_timer_value = tk.StringVar()

        self.global_timer_label = tk.Label(master, text="Global Timer:", font=('Helvetica', 24))
        self.global_timer_label.pack(pady=10)
        self.global_timer_display = tk.Label(master, textvariable=self.global_timer_value, font=('Helvetica', 36, 'bold'))
        self.global_timer_display.pack(pady=10)

        self.interval_timer_label = tk.Label(master, text="Interval Timer:", font=('Helvetica', 24))
        self.interval_timer_label.pack(pady=10)
        self.interval_timer_display = tk.Label(master, textvariable=self.interval_timer_value, font=('Helvetica', 36, 'bold'))
        self.interval_timer_display.pack(pady=10)

        self.message_label = tk.Label(master, text="", font=('Helvetica', 14), fg='red')
        self.message_label.pack(pady=10)

        # ASCII art of a smiling dog
        self.dog_art_label = tk.Label(master, text="""
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⢁⠂⠀⠀⠀
⠀⠀⠀⠀⠈⢢⠈⠑⢥⡀⠀⠠⠤⠒⠒⠒⠒⠲⠤⠤⢀⣴⠟⠁⣠⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀
⡆⠀⠀⠀⠀⠀⡸⠀⢀⡠⠤⡀⠀⠀⠀⠀⠀⠀⠀⡠⠤⡀⠀⠸⠀⠀⠀⠀⠀⢠
⣿⢂⠀⠀⢀⠔⠁⠀⢫⠀⠀⠐⡀⠀⠀⠀⠀⠀⡎⠀⠀⢨⠂⠀⠑⠄⠀⠀⠀⡻
⢻⣮⣰⠴⠃⠀⠀⣀⣀⡁⠒⠊⠀⠀⠀⠀⠀⠀⠙⠒⢂⣁⣀⠀⠀⠈⠀⢀⣠⠃
⢠⡿⠁⠀⠀⢀⣾⠟⠛⠿⣷⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠛⠻⣷⡄⠀⠀⠀⢻⡄
⣾⠇⠀⠀⠀⣾⠁⠀⠀⠀⠙⠇⠀⢀⡀⢄⣀⠀⠰⠏⠀⠀⠀⠈⢿⠀⠀⠀⠘⡷
⡿⠀⢀⠠⠤⠖⠒⠒⠒⠒⠒⠒⠊⣁⣤⣤⣄⠉⠒⠶⠒⠒⠒⠒⠒⢡⣄⣀⠀⢧
⡗⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠙⠿⡿⠋⠀⡀⠀⠀⠑⠄⠀⣰⠟⠉⠉⣧⠈
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠦⢤⠴⠧⢤⠴⠃⠀⠂⠀⠀⢀⡏⠀⠀⠀⠸⣎
⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⡿
⠀⠈⠛⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⣼⢹
⠀⠀⠀⠀⠈⠉⣻⡶⠢⠤⠤⠤⠄⠀⠀⠀⠀⠀⠀⠀⠠⠤⣴⠃⠀⠀⠀⠀⢰⢃⠛
⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⣠⢿⠋⠀
        """, font=('Courier', 16))
        self.dog_art_label.pack(pady=10)

        self.global_timer = timedelta()
        self.interval_timer = timedelta(seconds=30)
        self.is_running = False

        # Hook 'Q' key press event globally
        keyboard.on_press_key('q', self.key_pressed)

    def get_resource_path(self):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def key_pressed(self, event):
        self.start_timers()

    def start_timers(self):
        if not self.is_running:
            self.is_running = True
            self.intro_label.pack_forget()
            self.start_button.pack_forget()
            self.sound1_button.pack_forget()
            self.sound2_button.pack_forget()
            self.update_timers()

    def show_move_message(self):
        if 0 <= self.global_timer.seconds < 35:
            self.message_label.config(text="Ennard will begin moving in the next 10 seconds")
        if 37 <= self.global_timer.seconds < 600:
            self.message_label.config(text="Ennard has a movement opportunity")

        self.master.after(1000, self.clear_message)

    def beeb_sound(self):
        if 0 <= self.global_timer.seconds < 35:
            pygame.init()
            pygame.mixer.music.load(os.path.join(self.resource_path, "beep-warning-6387.mp3"))
            pygame.mixer.music.play()
        elif 37 <= self.global_timer.seconds < 540:
            pygame.init()
            pygame.mixer.music.load(os.path.join(self.resource_path, "beep-104060.wav"))
            pygame.mixer.music.play()
        elif 540 <= self.global_timer.seconds:
            pygame.init()
            pygame.mixer.music.load(os.path.join(self.resource_path, "winsquare-6993.mp3"))
            pygame.mixer.music.play()

    def test_beeb_sound1(self):
        pygame.init()
        pygame.mixer.music.load(os.path.join(self.resource_path, "beep-warning-6387.mp3"))
        pygame.mixer.music.play()

    def test_beeb_sound2(self):
        pygame.init()
        pygame.mixer.music.load(os.path.join(self.resource_path, "beep-104060.wav"))
        pygame.mixer.music.play()

    def update_timers(self):
        if self.is_running:
            self.global_timer += timedelta(seconds=1)
            self.global_timer_value.set(str(self.global_timer).split(".")[0])

            self.interval_timer -= timedelta(seconds=1)
            self.interval_timer_value.set(str(self.interval_timer).split(".")[0])

            if self.interval_timer == timedelta():
                self.reset_interval_timer()
                Thread(target=self.beeb_sound).start()
                Thread(target=self.show_move_message).start()

            self.master.after(1000, self.update_timers)

    def reset_interval_timer(self):
        if 30 <= self.global_timer.seconds < 90:
            self.interval_timer = timedelta(seconds=10)
        elif 90 <= self.global_timer.seconds < 360:
            self.interval_timer = timedelta(seconds=6)
        elif 360 <= self.global_timer.seconds < 450:
            self.interval_timer = timedelta(seconds=3)
        elif 450 <= self.global_timer.seconds < 540:
            self.interval_timer = timedelta(seconds=2)
        else:
            self.is_running = False

    def clear_message(self):
        self.message_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = DualStopwatchApp(root)
    root.mainloop()
