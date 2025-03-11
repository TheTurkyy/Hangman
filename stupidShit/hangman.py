import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # i used this for the image 
def load_words():
    """Loads words from words.txt file"""
    try:
        with open("words.txt", "r") as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        messagebox.showerror("Error", "words.txt file not found!")
        return []

class HangmanGame:
    """Main Hangman game class with GUI"""
    # Dark mode colors
    DARK_BG = "#2C2F33"  
    DARK_FG = "#FFFFFF"  
    BTN_BG = "#23272A"   
    BTN_FG = "#FFFFFF"  
    BTN_ACTIVE = "#99AAB5"  
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.configure(bg=self.DARK_BG)

        self.words = load_words()
        self.word = random.choice(self.words).lower() if self.words else "error"
        self.guessed_letters = set()
        self.attempts = 5

        self.word_display = tk.StringVar()
        self.update_display()
        self.create_widgets()

        self.hangman_image_label = tk.Label(self.root, bg=self.DARK_BG)
        self.hangman_image_label.pack(pady=20)

        self.update_hangman_image()

    def create_widgets(self):
        tk.Label(self.root, text="Hangman (By Turkyy)", font=("Arial", 24), bg=self.DARK_BG, fg=self.DARK_FG).pack()

        self.word_label = tk.Label(self.root, textvariable=self.word_display, font=("Arial", 20), bg=self.DARK_BG, fg=self.DARK_FG)
        self.word_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, bg=self.DARK_BG)
        self.buttons_frame.pack()

        self.letter_buttons = {}
        for letter in "abcdefghijklmnopqrstuvwxyz":
            btn = tk.Button(self.buttons_frame, text=letter, font=("Arial", 14), bg=self.BTN_BG, fg=self.BTN_FG,
                            activebackground=self.BTN_ACTIVE, activeforeground=self.DARK_BG,
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=(ord(letter) - ord('a')) // 9, column=(ord(letter) - ord('a')) % 9, padx=2, pady=2)
            self.letter_buttons[letter] = btn

        self.status_label = tk.Label(self.root, text=f"Attempts left: {self.attempts}", font=("Arial", 14), bg=self.DARK_BG, fg=self.DARK_FG)
        self.status_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Restart Game", font=("Arial", 14), bg=self.BTN_BG, fg=self.BTN_FG,
                                      activebackground=self.BTN_ACTIVE, activeforeground=self.DARK_BG, command=self.restart_game)
        self.reset_button.pack(pady=10)

    def update_hangman_image(self):
        if self.attempts == 6:
            image_path = "Assets/images/hangman5.png"
        elif self.attempts == 5:
            image_path = "Assets/images/hangman5.png"
        elif self.attempts == 4:
            image_path = "Assets/images/hangman4.png"
        elif self.attempts == 3:
            image_path = "Assets/images/hangman3.png"
        elif self.attempts == 2:
            image_path = "Assets/images/hangman2.png"
        else:
            image_path = "Assets/images/hangman1.png"  
        
        try:
            hangman_image = Image.open(image_path)
            resized_image = hangman_image.resize((300, 300))  # my image was a bit small lmao (had to resize it, can be left out if youre happy with your own images)
            hangman_image_tk = ImageTk.PhotoImage(resized_image)
            
            self.hangman_image_label.config(image=hangman_image_tk)
            self.hangman_image_label.image = hangman_image_tk  
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state=tk.DISABLED)

        if letter in self.word:
            self.update_display()
            if all(l in self.guessed_letters for l in self.word):
                messagebox.showinfo("Hangman", f"🎉 You won! The word was: {self.word}")
                self.disable_buttons()
        else:
            self.attempts -= 1
            self.status_label.config(text=f"Attempts left: {self.attempts}")
            self.update_hangman_image()  # Update image after each wrong guess

            if self.attempts == 0:
                messagebox.showerror("Game Over", f"❌ You lost! The word was: {self.word}")
                self.disable_buttons()

    def disable_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state=tk.DISABLED)

    def update_display(self):
        self.word_display.set(" ".join(letter if letter in self.guessed_letters else "_" for letter in self.word))

    def restart_game(self):
        self.word = random.choice(self.words).lower() if self.words else "error"
        self.guessed_letters.clear()
        self.attempts = 5
        self.update_display()
        self.status_label.config(text=f"Attempts left: {self.attempts}")
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)
        self.update_hangman_image()  


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
