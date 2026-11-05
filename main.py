
import tkinter as tk
import random
import threading

try:
    import winsound
except ImportError:
    winsound = None


WORDS = {
    "FRUITS": [
        ("APPLE", "A fruit that keeps the doctor away"),
        ("MANGO", "King of fruits"),
        ("BANANA", "A long yellow fruit"),
        ("ORANGE", "A citrus fruit"),
        ("GRAPES", "Small fruits in bunches"),
        ("PAPAYA", "A tropical orange fruit"),
        ("PINEAPPLE", "A fruit with a crown"),
        ("CHERRY", "A small red fruit"),
        ("STRAWBERRY", "A red fruit with tiny seeds"),
        ("WATERMELON", "A large green fruit")
    ],
    "ANIMALS": [
        ("TIGER", "A wild animal with black stripes"),
        ("LION", "King of the jungle"),
        ("ELEPHANT", "The largest land animal"),
        ("GIRAFFE", "An animal with a long neck"),
        ("MONKEY", "An animal that climbs trees"),
        ("DOLPHIN", "An intelligent sea animal"),
        ("RABBIT", "An animal with long ears"),
        ("PENGUIN", "A bird that cannot fly"),
        ("KANGAROO", "An animal with a baby pouch"),
        ("LEOPARD", "A wild cat with spots")
    ],
    "TECHNOLOGY": [
        ("PYTHON", "A popular programming language"),
        ("COMPUTER", "An electronic processing machine"),
        ("KEYBOARD", "Used for typing"),
        ("INTERNET", "A worldwide computer network"),
        ("ROBOT", "A machine that performs tasks"),
        ("MOBILE", "A device used for calls"),
        ("SOFTWARE", "Programs used by computers"),
        ("DATABASE", "An organized collection of data"),
        ("ALGORITHM", "Steps to solve a problem"),
        ("WEBSITE", "A collection of web pages")
    ],
    "FOOD": [
        ("PIZZA", "An Italian dish with cheese"),
        ("BURGER", "A sandwich with a patty"),
        ("NOODLES", "Long thin strips of food"),
        ("SAMOSA", "A triangular Indian snack"),
        ("PANEER", "A popular Indian milk product"),
        ("CHOCOLATE", "A sweet treat made from cocoa"),
        ("SANDWICH", "Bread with a filling"),
        ("BIRYANI", "A popular spiced rice dish"),
        ("POPCORN", "A movie-time snack"),
        ("PANCAKE", "A flat breakfast dish")
    ],
    "NATURE": [
        ("FLOWER", "A colorful part of a plant"),
        ("MOUNTAIN", "A very high natural landform"),
        ("RAINBOW", "A colorful arc after rain"),
        ("FOREST", "A large area covered with trees"),
        ("OCEAN", "A very large body of salt water"),
        ("SUNSHINE", "Light from the sun"),
        ("RIVER", "A natural flowing water body"),
        ("THUNDER", "A loud sound during a storm"),
        ("BUTTERFLY", "An insect with colorful wings"),
        ("RAIN", "Water falling from clouds")
    ],
    "EDUCATION": [
        ("SCHOOL", "A place where students study"),
        ("TEACHER", "A person who helps students learn"),
        ("SCIENCE", "Study of the natural world"),
        ("HISTORY", "Study of past events"),
        ("LIBRARY", "A place filled with books"),
        ("NOTEBOOK", "Used to write class notes"),
        ("COLLEGE", "An institution for higher studies"),
        ("EXAMINATION", "A test of knowledge"),
        ("MATHEMATICS", "Study of numbers and shapes"),
        ("KNOWLEDGE", "Understanding gained through learning")
    ]
}


BG = "#090014"
CARD = "#180B2B"
PINK = "#FF2E93"
PURPLE = "#A855F7"
CYAN = "#00F5FF"
WHITE = "#FFFFFF"
GREEN = "#39FF88"
RED = "#FF3366"

MAX_ATTEMPTS = 6


class NeonHangman:

    def __init__(self, root):
        self.root = root
        self.root.title("NEON HANGMAN")
        self.root.geometry("950x790")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.score = 0
        self.rounds = 0
        self.previous_word = None

        self.category = tk.StringVar(value="ALL")
        self.difficulty = tk.StringVar(value="ALL")

        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)

        self.show_welcome()

    # NON-BLOCKING SOUND EFFECTS
    def sound(self, effect):
        if winsound is None:
            return

        sounds = {
            "correct": [(1000, 150)],
            "wrong": [(300, 200)],
            "win": [(700, 120), (1000, 120), (1300, 200)],
            "lose": [(500, 150), (250, 250)],
            "exit": [(800, 120), (500, 180)]
        }

        def play():
            try:
                for frequency, duration in sounds[effect]:
                    winsound.Beep(frequency, duration)
            except Exception as error:
                print("Sound error:", error)

        threading.Thread(target=play, daemon=True).start()

    # EXIT GAME
    def exit_game(self):
        self.sound("exit")
        self.root.after(600, self.root.destroy)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, parent):
        tk.Label(
            parent,
            text="⚡ NEON HANGMAN ⚡",
            font=("Arial", 30, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(25, 5))

        tk.Label(
            parent,
            text="THE ULTIMATE WORD GUESSING CHALLENGE",
            font=("Arial", 10, "bold"),
            bg=BG,
            fg=PINK
        ).pack()

    # WELCOME SCREEN
    def show_welcome(self):
        self.clear_screen()
        self.heading(self.root)

        card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=PURPLE,
            highlightthickness=2
        )
        card.pack(padx=70, pady=35, fill="both", expand=True)

        tk.Label(
            card,
            text="WELCOME PLAYER!",
            font=("Arial", 25, "bold"),
            bg=CARD,
            fg=PINK
        ).pack(pady=(65, 15))

        tk.Label(
            card,
            text="GUESS THE HIDDEN WORD",
            font=("Arial", 16, "bold"),
            bg=CARD,
            fg=CYAN
        ).pack(pady=10)

        tk.Label(
            card,
            text="• Guess the hidden word letter by letter\n"
                 "• Use hints to help you\n"
                 "• You have only 6 wrong attempts\n"
                 "• Earn 10 points for every win",
            font=("Arial", 13),
            bg=CARD,
            fg=WHITE,
            justify="left"
        ).pack(pady=25)

        tk.Button(
            card,
            text="▶ START GAME",
            command=self.start_game,
            font=("Arial", 16, "bold"),
            bg=PINK,
            fg=WHITE,
            activebackground=PURPLE,
            relief="flat",
            padx=35,
            pady=12
        ).pack(pady=20)

        tk.Button(
            card,
            text="EXIT GAME",
            command=self.exit_game,
            font=("Arial", 11, "bold"),
            bg="#352342",
            fg=WHITE,
            relief="flat",
            padx=20,
            pady=8
        ).pack(pady=5)

        tk.Label(
            card,
            text="POWERED BY PYTHON • TKINTER",
            font=("Arial", 9, "bold"),
            bg=CARD,
            fg=PURPLE
        ).pack(side="bottom", pady=20)

    # SELECT RANDOM WORD
    def choose_word(self):
        pool = []

        for group, entries in WORDS.items():

            if self.category.get() != "ALL":
                if group != self.category.get():
                    continue

            for word, hint in entries:
                length = len(word)
                level = self.difficulty.get()

                if level == "EASY" and length > 5:
                    continue

                if level == "MEDIUM" and not 6 <= length <= 8:
                    continue

                if level == "HARD" and length < 9:
                    continue

                pool.append((word, hint, group))

        if not pool:
            return None

        choices = [
            item for item in pool
            if item[0] != self.previous_word
        ]

        if not choices:
            choices = pool

        return random.choice(choices)

    # START GAME
    def start_game(self):
        self.clear_screen()
        self.build_game_screen()
        self.new_round()

    # GAME SCREEN
    def build_game_screen(self):
        self.heading(self.root)

        self.card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=PURPLE,
            highlightthickness=2
        )
        self.card.pack(padx=30, pady=15, fill="both", expand=True)

        filters = tk.Frame(self.card, bg=CARD)
        filters.pack(pady=10)

        tk.Label(
            filters,
            text="CATEGORY",
            bg=CARD,
            fg=CYAN,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=8)

        tk.OptionMenu(
            filters,
            self.category,
            "ALL",
            *WORDS.keys()
        ).grid(row=1, column=0, padx=8)

        tk.Label(
            filters,
            text="DIFFICULTY",
            bg=CARD,
            fg=PINK,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=8)

        tk.OptionMenu(
            filters,
            self.difficulty,
            "ALL", "EASY", "MEDIUM", "HARD"
        ).grid(row=1, column=1, padx=8)

        tk.Button(
            filters,
            text="NEW ROUND",
            command=self.new_round,
            bg=PURPLE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=12,
            pady=5
        ).grid(row=1, column=2, padx=12)

        self.canvas = tk.Canvas(
            self.card,
            width=190,
            height=145,
            bg=CARD,
            highlightthickness=0
        )
        self.canvas.pack(pady=4)

        self.word_label = tk.Label(
            self.card,
            font=("Arial", 26, "bold"),
            bg=CARD,
            fg=CYAN
        )
        self.word_label.pack(pady=5)

        self.hint_label = tk.Label(
            self.card,
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=PINK,
            wraplength=750
        )
        self.hint_label.pack(pady=5)

        self.category_label = tk.Label(
            self.card,
            font=("Arial", 10, "bold"),
            bg=CARD,
            fg=PURPLE
        )
        self.category_label.pack()

        self.info = tk.Label(
            self.card,
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=RED
        )
        self.info.pack(pady=4)

        self.score_label = tk.Label(
            self.card,
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=CYAN
        )
        self.score_label.pack(pady=4)

        tk.Label(
            self.card,
            text="SELECT YOUR LETTER",
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg=PINK
        ).pack(pady=5)

        self.keyboard = tk.Frame(self.card, bg=CARD)
        self.keyboard.pack()

        self.buttons = {}

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):

            btn = tk.Button(
                self.keyboard,
                text=letter,
                width=3,
                font=("Arial", 10, "bold"),
                bg="#281044",
                fg=CYAN,
                activebackground=PINK,
                activeforeground=WHITE,
                relief="flat",
                command=lambda x=letter: self.guess(x)
            )

            btn.grid(
                row=i // 9,
                column=i % 9,
                padx=4,
                pady=4
            )

            self.buttons[letter] = btn

        self.message = tk.Label(
            self.card,
            text="LET'S PLAY!",
            font=("Arial", 14, "bold"),
            bg=CARD,
            fg=PINK
        )
        self.message.pack(pady=8)

    # NEW ROUND
    def new_round(self):
        selected = self.choose_word()

        if selected is None:
            self.message.config(
                text="NO WORDS AVAILABLE! CHANGE FILTERS.",
                fg=RED
            )
            return

        self.word, self.hint, self.group = selected
        self.previous_word = self.word

        self.guessed = []
        self.wrong = 0
        self.finished = False
        self.rounds += 1

        for btn in self.buttons.values():
            btn.config(
                state="normal",
                bg="#281044",
                fg=CYAN
            )

        self.message.config(
            text="⚡ LET'S PLAY!",
            fg=PINK
        )

        self.update_screen()

    # DRAW HANGMAN
    def draw_hangman(self):
        self.canvas.delete("all")

        self.canvas.create_line(
            25, 130, 165, 130,
            fill=CYAN,
            width=4
        )

        self.canvas.create_line(
            55, 130, 55, 10,
            fill=CYAN,
            width=4
        )

        self.canvas.create_line(
            55, 10, 125, 10,
            fill=CYAN,
            width=4
        )

        self.canvas.create_line(
            125, 10, 125, 30,
            fill=CYAN,
            width=3
        )

        parts = [
            lambda: self.canvas.create_oval(
                110, 30, 140, 60,
                outline=PINK,
                width=3
            ),
            lambda: self.canvas.create_line(
                125, 60, 125, 95,
                fill=PINK,
                width=3
            ),
            lambda: self.canvas.create_line(
                125, 70, 105, 85,
                fill=PINK,
                width=3
            ),
            lambda: self.canvas.create_line(
                125, 70, 145, 85,
                fill=PINK,
                width=3
            ),
            lambda: self.canvas.create_line(
                125, 95, 105, 120,
                fill=PINK,
                width=3
            ),
            lambda: self.canvas.create_line(
                125, 95, 145, 120,
                fill=PINK,
                width=3
            )
        ]

        for part in parts[:self.wrong]:
            part()

    # UPDATE GAME SCREEN
    def update_screen(self):
        display = "   ".join(
            letter if letter in self.guessed else "_"
            for letter in self.word
        )

        self.word_label.config(text=display)
        self.hint_label.config(text="HINT: " + self.hint)

        self.category_label.config(
            text="CATEGORY: " + self.group
        )

        self.info.config(
            text=f"ATTEMPTS LEFT: {MAX_ATTEMPTS - self.wrong}"
        )

        self.score_label.config(
            text=f"SCORE: {self.score}   |   ROUND: {self.rounds}"
        )

        self.draw_hangman()

    # GUESS LETTER
    def guess(self, letter):
        if self.finished:
            return

        self.guessed.append(letter)

        self.buttons[letter].config(
            state="disabled",
            bg="#352342",
            fg="#777777"
        )

        if letter in self.word:
            self.sound("correct")
            self.message.config(
                text="CORRECT GUESS!",
                fg=GREEN
            )
        else:
            self.wrong += 1
            self.sound("wrong")
            self.message.config(
                text="WRONG GUESS! TRY AGAIN!",
                fg=RED
            )

        self.update_screen()

        if all(x in self.guessed for x in self.word):
            self.finished = True
            self.score += 10
            self.sound("win")
            self.show_result(True)

        elif self.wrong >= MAX_ATTEMPTS:
            self.finished = True
            self.sound("lose")
            self.show_result(False)

    # FINAL SCORE SCREEN
    def show_result(self, won):
        self.clear_screen()
        self.heading(self.root)

        card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=PURPLE,
            highlightthickness=2
        )
        card.pack(padx=70, pady=35, fill="both", expand=True)

        if won:
            title = "YOU WIN!"
            color = GREEN
            result = "Congratulations! You guessed the word."
        else:
            title = "GAME OVER!"
            color = RED
            result = "Better luck next time!"

        tk.Label(
            card,
            text=title,
            font=("Arial", 30, "bold"),
            bg=CARD,
            fg=color
        ).pack(pady=(55, 15))

        tk.Label(
            card,
            text=result,
            font=("Arial", 14, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(pady=10)

        tk.Label(
            card,
            text=f"THE WORD WAS: {self.word}",
            font=("Arial", 17, "bold"),
            bg=CARD,
            fg=CYAN
        ).pack(pady=15)

        tk.Label(
            card,
            text=f"TOTAL SCORE: {self.score}\n"
                 f"ROUNDS PLAYED: {self.rounds}\n"
                 f"POINTS EARNED: {10 if won else 0}",
            font=("Arial", 15, "bold"),
            bg=CARD,
            fg=PINK,
            justify="center"
        ).pack(pady=20)

        tk.Button(
            card,
            text="▶ PLAY AGAIN",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg=PINK,
            fg=WHITE,
            relief="flat",
            padx=30,
            pady=10
        ).pack(pady=10)

        tk.Button(
            card,
            text="⌂ HOME",
            command=self.show_welcome,
            font=("Arial", 11, "bold"),
            bg=PURPLE,
            fg=WHITE,
            relief="flat",
            padx=25,
            pady=7
        ).pack(pady=5)

        tk.Button(
            card,
            text="EXIT GAME",
            command=self.exit_game,
            font=("Arial", 11, "bold"),
            bg="#352342",
            fg=WHITE,
            relief="flat",
            padx=20,
            pady=7
        ).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    game = NeonHangman(root)
    root.mainloop()
