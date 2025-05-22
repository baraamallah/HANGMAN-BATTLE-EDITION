import tkinter as tk
from tkinter import simpledialog, ttk, font
import string
import random
import tkinter.messagebox as messagebox
from random import randint
import json
import os

# ---------------------
# Hangman ASCII Art
# ---------------------
Hangman_Stages = [
    """
    +---+
    |   |
        |
        |
        |
        |
    ========""",
    """
    +---+
    |   |
    O   |
        |
        |
        |
    ========""",
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    ========""",
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    ========""",
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    ========""",
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    ========""",
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    ========"""
]

# ---------------------
# Game State Variables
# ---------------------
User = ""
display = []
tries = 0
guessed_letters = set()
player1_name = ""
player2_name = ""
player1_score = 0
player2_score = 0
round_number = 1
current_guesser = ""
guess_timer = 30
running_timer = None
hints_remaining = 2
game_window = None

# ---------------------
# Custom Styles
# ---------------------
def configure_styles():
    style = ttk.Style()
    style.configure('TFrame', background='white')
    style.configure('TLabel', background='white', foreground='#333333', font=('Poppins', 12))
    style.configure('TButton', font=('Poppins', 12, 'bold'), padding=10)
    style.map('TButton',
              background=[('active', '#e94560'), ('!disabled', '#0f3460')],
              foreground=[('!disabled', 'white')])

# ---------------------
# Input Page
# ---------------------
def create_input_page():
    input_frame = tk.Frame(root, bg='#1a1a2e')
    input_frame.pack(fill='both', expand=True)

    # Main container for centering
    center_container = tk.Frame(input_frame, bg='#1a1a2e')
    center_container.place(relx=0.5, rely=0.5, anchor='center')

    # Add school logo at the top
    try:
        logo = tk.PhotoImage(file="school_logo.png")  # Replace with your logo path
        logo_label = tk.Label(center_container, image=logo, bg='#2c3e50')
        logo_label.image = logo  # Keep a reference
        logo_label.pack(pady=(0, 20))
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Title with gradient effect
    title_frame = tk.Frame(center_container, bg='#2c3e50')
    title_frame.pack(pady=(0, 20))
    
    title = tk.Label(title_frame, text="HANGMAN GAME", font=('Poppins', 48, 'bold'), 
                    bg='#1a1a2e', fg='#e94560')  # Vibrant pink title
    title.pack()

    # Subtitle with animation
    subtitle = tk.Label(center_container, text="Enter Player Names", font=('Poppins', 18), 
                       bg='#2c3e50', fg='#ecf0f1')
    subtitle.pack(pady=(0, 40))

    # Input Fields with modern design
    form_frame = tk.Frame(center_container, bg='#2c3e50')
    form_frame.pack()

    # Player 1 Input
    player1_frame = tk.Frame(form_frame, bg='#2c3e50')
    player1_frame.grid(row=0, column=0, padx=20, pady=10, sticky='ew')
    tk.Label(player1_frame, text="Player 1:", font=('Poppins', 14), 
            bg='#2c3e50', fg='white').pack(side='left', padx=(0, 10))
    player1_entry = tk.Entry(player1_frame, font=('Poppins', 14), bd=0, 
                            relief='flat', width=20, highlightthickness=2,
                            highlightbackground="#3498db", highlightcolor="#3498db")
    player1_entry.pack(side='right', padx=10, ipady=5)

    # Player 2 Input
    player2_frame = tk.Frame(form_frame, bg='#2c3e50')
    player2_frame.grid(row=1, column=0, padx=20, pady=10, sticky='ew')
    tk.Label(player2_frame, text="Player 2:", font=('Poppins', 14), 
            bg='#2c3e50', fg='white').pack(side='left', padx=(0, 10))
    player2_entry = tk.Entry(player2_frame, font=('Poppins', 14), bd=0, 
                            relief='flat', width=20, highlightthickness=2,
                            highlightbackground="#3498db", highlightcolor="#3498db")
    player2_entry.pack(side='right', padx=10, ipady=5)

    # Start and Exit buttons with hover effect
    def start_game():
        global player1_name, player2_name, current_guesser
        player1_name = player1_entry.get().strip()
        player2_name = player2_entry.get().strip()

        if not player1_name or not player2_name:
            messagebox.showerror("Error", "Both player names are required!")
            return

        current_guesser = player1_name
        input_frame.destroy()
        ask_for_word()

    def exit_game():
        root.destroy()

    button_container = tk.Frame(center_container, bg='#2c3e50')
    button_container.pack(pady=(30, 0))
    
    # Start Button
    start_btn = tk.Button(button_container, text="START GAME", command=start_game,
                         font=('Poppins', 16, 'bold'), bg='#e94560', fg='white',  # Vibrant pink button
                         activebackground='#d63649', bd=0, padx=30, pady=15,
                         relief='raised', overrelief='sunken')
    start_btn.pack(side='left', padx=10)

    # Exit Button
    exit_btn = tk.Button(button_container, text="EXIT", command=exit_game,
                        font=('Poppins', 16, 'bold'), bg='#0f3460', fg='white',  # Deep blue button
                        activebackground='#0a2647', bd=0, padx=30, pady=15,
                        relief='raised', overrelief='sunken')
    exit_btn.pack(side='right', padx=10)

    # Credits at the bottom
    credits_frame = tk.Frame(input_frame, bg='#2c3e50')
    credits_frame.pack(side='bottom', pady=20)
    
    credits = tk.Label(credits_frame, 
                      text="© 2025 Created by Baraa El-Mallah & Adam Doha",
                      font=('Poppins', 10, 'italic'), bg='#2c3e50', fg='#7f8c8d')
    credits.pack()

    # Focus on first entry
    player1_entry.focus_set()

    # Center the form
    input_frame.update()

def ask_for_word():
    try:
        word = simpledialog.askstring("Word Input", 
                                    f"{player2_name}, enter a word for {player1_name} to guess:",
                                    parent=root)
        
        if not word:
            return ask_for_word()
            
        is_valid, error_msg = validate_word(word)
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return ask_for_word()
            
        return open_game_window(word)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return ask_for_word()

# ---------------------
# Game Functions
# ---------------------
def update_display():
    if 'word_label' in globals():
        word_label.config(text=" ".join(display))

def update_hangman():
    if 'hangman_label' in globals():
        hangman_label.config(text=Hangman_Stages[tries])

def update_score_tab():
    if 'score_list' not in globals() or 'live_score_label' not in globals():
        return
        
    # Clear existing entries
    score_list.delete(0, tk.END)
    
    # Add stylized header
    score_list.insert(tk.END, "🎯 SCOREBOARD 🎯")
    score_list.insert(tk.END, "━━━━━━━━━━━━━━━━━")
    score_list.insert(tk.END, "")  # Spacing
    
    # Sort players by score
    players = [(player1_name, player1_score), (player2_name, player2_score)]
    players.sort(key=lambda x: x[1], reverse=True)
    
    # Add player scores with medals and better formatting
    for i, (name, score) in enumerate(players):
        medal = "👑" if i == 0 else "🥈"
        score_list.insert(tk.END, f"{medal} {name}")
        score_list.insert(tk.END, f"   Points: {score}")
        score_list.insert(tk.END, "")  # Add spacing between players
    
    score_list.insert(tk.END, "━━━━━━━━━━━━━━━━━")
    score_list.insert(tk.END, f"📍 Round {round_number}")
    score_list.insert(tk.END, f"🎲 Turn: {current_guesser}")
    
    # Update leader display with improved formatting
    if players[0][1] > 0:
        leader_color = "#f1c40f"  # Gold for active leader
        leader_text = f"👑 Leader: {players[0][0]} ({players[0][1]} pts)"
    else:
        leader_color = "#95a5a6"  # Gray when no points yet
        leader_text = "Game in progress..."
    
    live_score_label.config(text=leader_text, fg=leader_color)

def guess_letter(letter):
    global tries, player2_score, player1_score, guess_timer
    
    if letter in guessed_letters or tries >= 6:
        return
        
    if running_timer:
        root.after_cancel(running_timer)
        
    guess_timer = 30
    guessed_letters.add(letter)
    
    if letter in letter_buttons:
        letter_buttons[letter].config(state="disabled", bg="#bdc3c7")

    if letter in User:
        for i in range(len(User)):
            if User[i] == letter:
                display[i] = letter
        update_display()
        if letter in letter_buttons:
            letter_buttons[letter].config(bg="#2ecc71", fg="white")
    else:
        tries += 1
        update_hangman()
        if letter in letter_buttons:
            letter_buttons[letter].config(bg="#e74c3c", fg="white")

    if "_" not in display:
        if current_guesser == player1_name:
            player1_score += 2
        else:
            player2_score += 2
        if 'result_label' in globals():
            result_label.config(text=f"🎉 {current_guesser} guessed it and earns 2 points!", fg="#2ecc71")
        disable_buttons()
    elif tries >= 6:
        if 'result_label' in globals():
            result_label.config(text=f"💀 {current_guesser} failed! Word was: {User}", fg="#e74c3c")
        disable_buttons()
    
    if running_timer:
        update_timer()

def continue_game():
    global User, display, tries, guessed_letters, round_number, current_guesser, guess_timer, hints_remaining, running_timer
    
    if running_timer:
        root.after_cancel(running_timer)
        running_timer = None
        
    hints_remaining = 2

    current_guesser = player2_name if current_guesser == player1_name else player1_name

    word = simpledialog.askstring("New Word", 
                                f"{player2_name if current_guesser == player1_name else player1_name}, enter a word for {current_guesser} to guess:",
                                parent=game_window)
    if not word:
        return
        
    is_valid, error_msg = validate_word(word)
    if not is_valid:
        messagebox.showerror("Error", error_msg)
        return continue_game()

    User = word.lower()
    display = ["_" for _ in User]
    guessed_letters.clear()
    tries = 0
    round_number += 1
    guess_timer = 30

    update_display()
    update_hangman()
    update_score_tab()
    if 'result_label' in globals():
        result_label.config(text=f"🔍 {current_guesser} is now guessing!", fg="#3498db")
    enable_buttons()
    if 'continue_button' in globals():
        continue_button.config(state="disabled")
    update_timer()

def create_confetti(canvas, x, y):
    colors = ['#FF69B4', '#87CEEB', '#98FB98', '#DDA0DD', '#F0E68C']
    size = randint(5, 15)
    color = colors[randint(0, len(colors)-1)]
    
    confetti_id = canvas.create_oval(x, y, x+size, y+size, fill=color, tags='confetti')
    
    def update_confetti():
        canvas.move(confetti_id, 0, 5)
        pos = canvas.coords(confetti_id)
        if pos[1] < canvas.winfo_height():
            canvas.after(50, update_confetti)
        else:
            canvas.delete(confetti_id)
    
    update_confetti()

def show_winner_popup(winner_name, score):
    popup = tk.Toplevel()
    popup.title('🎉 Winner!')
    popup.attributes('-fullscreen', True)
    popup.configure(bg='white')
    
    canvas = tk.Canvas(popup, width=popup.winfo_screenwidth(), height=popup.winfo_screenheight(), 
                     bg='white', highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    
    # Center content vertically and horizontally
    canvas.create_text(popup.winfo_screenwidth()//2, popup.winfo_screenheight()//2 - 100, 
                     text=f'🏆 WINNER! 🏆', font=('Poppins', 48, 'bold'), fill='#2c3e50')
    canvas.create_text(popup.winfo_screenwidth()//2, popup.winfo_screenheight()//2, 
                     text=f'{winner_name}\nScore: {score} points',
                     font=('Poppins', 36), fill='#2c3e50')
    
    # Add credits text
    canvas.create_text(popup.winfo_screenwidth()//2, popup.winfo_screenheight() - 50, 
                     text='© 2025 Made by Baraa El-Mallah & Adam Doha',
                     font=('Poppins', 14, 'italic'), fill='#7f8c8d')
    
    # Add confetti animation
    for _ in range(100):
        create_confetti(canvas, randint(0, popup.winfo_screenwidth()), randint(-50, 0))

def enable_buttons():
    if 'letter_buttons' in globals():
        for btn in letter_buttons.values():
            btn.config(
                state="normal",
                bg="#3498db",  # Nice blue color
                fg="white",
                activebackground="#2980b9",  # Darker blue on hover
                activeforeground="white",
                relief="raised",
                bd=2
            )

def disable_buttons():
    if 'letter_buttons' in globals():
        for btn in letter_buttons.values():
            btn.config(
                state="disabled",
                bg="#95a5a6",  # Gray for disabled
                relief="sunken"
            )
    
    if 'continue_button' in globals() and 'end_game_button' in globals():
        continue_button.config(
            state="normal",
            bg="#2ecc71",  # Green for continue
            activebackground="#27ae60"
        )
        end_game_button.config(
            state="normal",
            bg="#e74c3c",  # Red for end
            activebackground="#c0392b"
        )
    
    if running_timer:
        root.after_cancel(running_timer)

def validate_word(word):
    if not word:
        return False, "Word cannot be empty"
    if not word.isalpha():
        return False, "Word must contain only letters"
    if len(word) > 9:
        return False, "Word must be 9 letters or less"
    return True, ""

def update_timer():
    global guess_timer, running_timer
    try:
        if not hasattr(root, 'winfo_exists') or not root.winfo_exists():
            return
            
        if guess_timer > 0:
            if 'timer_display' in globals():
                timer_display.config(text=f"⏱ Time: {guess_timer}s",
                             fg="#e74c3c" if guess_timer <= 10 else "#2ecc71",
                             font=('Poppins', 14, 'bold'))
            
            if 'timer_canvas' in globals():
                extent = (guess_timer / 30) * 360
                timer_canvas.delete('timer_circle')
                timer_circle = timer_canvas.create_arc(5, 5, 55, 55, start=90, extent=extent,
                                                     fill='#3498db' if guess_timer > 10 else '#e74c3c',
                                                     tags='timer_circle')
                timer_canvas.itemconfig(timer_text, text=str(guess_timer),
                                      fill='#2c3e50' if guess_timer > 10 else '#e74c3c')
            guess_timer -= 1
            running_timer = root.after(1000, update_timer)
        else:
            try:
                if current_guesser == player1_name:
                    player2_score += 1
                    if 'result_label' in globals():
                        result_label.config(text=f"⏰ Time's Up! {player2_name} gets 1 point!", fg="#e74c3c")
                else:
                    player1_score += 1
                    if 'result_label' in globals():
                        result_label.config(text=f"⏰ Time's Up! {player1_name} gets 1 point!", fg="#e74c3c")
                disable_buttons()
                update_score_tab()
            except tk.TclError as e:
                print(f"Tkinter error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                if running_timer:
                    root.after_cancel(running_timer)
                    running_timer = None
    except Exception as e:
        print(f"Timer error: {e}")
def handle_timeout():
    """Separate function to handle timer timeout logic"""
    global player1_score, player2_score
    
    try:
        if current_guesser == player1_name:
            player2_score += 1
            update_timeout_ui(player2_name)
        else:
            player1_score += 1
            update_timeout_ui(player1_name)
    except Exception as e:
        print(f"Timeout handling error: {e}")

def update_timeout_ui(winner_name):
    """Update UI elements after timeout"""
    if 'result_label' in globals():
        result_label.config(text=f"⏰ Time's Up! {winner_name} gets 1 point!", fg="#e74c3c")
    disable_buttons()
    update_score_tab()

def end_game():
    global player1_score, player2_score, running_timer
    
    if running_timer:
        root.after_cancel(running_timer)
        running_timer = None
    
    if player1_score == player2_score:
        show_winner_popup('Tie Game', '🤝 It\'s a tie!')
    else:
        winner = player1_name if player1_score > player2_score else player2_name
        winner_score = max(player1_score, player2_score)
        show_winner_popup(winner, winner_score)
    
    disable_buttons()
    if 'continue_button' in globals() and 'end_game_button' in globals():
        continue_button.config(state='disabled')
        end_game_button.config(state='disabled')
    update_score_tab()
    
    # Add a delay before closing the application
    root.after(3000, lambda: root.destroy())

# ---------------------
# Game Window
# ---------------------
def open_game_window(word):
    global User, display, tries, guessed_letters
    global word_label, hangman_label, result_label, letter_buttons, continue_button
    global timer_display, end_game_button, score_list, live_score_label, game_window
    global timer_canvas, timer_text, timer_circle

    User = word.lower()
    display = ["_" for _ in User]
    tries = 0
    guessed_letters.clear()

    game_window = tk.Toplevel(root)
    game_window.title("🎮 Hangman Game")
    game_window.attributes('-fullscreen', True)
    game_window.configure(bg="#2c3e50")

    # Main container
    main_container = tk.Frame(game_window, bg="#2c3e50")
    main_container.pack(fill='both', expand=True)

    # Game area container
    game_area = tk.Frame(main_container, bg="#2c3e50")
    game_area.pack(fill='both', expand=True)

    # Center container for game elements
    center_container = tk.Frame(game_area, bg="#2c3e50")
    center_container.place(relx=0.5, rely=0.5, anchor='center')

    # Left panel (Game area)
    left_panel = tk.Frame(center_container, bg="#2c3e50")
    left_panel.pack(side='left', fill='both', expand=True)

    # Right panel (Rules only)
    right_panel = tk.Frame(center_container, bg="#34495e", width=300)
    right_panel.pack(side='right', fill='y')
    right_panel.pack_propagate(False)

    # Rules section
    rules_title = tk.Label(right_panel, text="GAME RULES",
                          font=('Poppins', 24, 'bold'),
                          bg="#34495e", fg="#ecf0f1", pady=10)
    rules_title.pack()

    rules_text = """
    🎮 How to Play:
    
    1. Players take turns guessing words
    2. Each player has 30 seconds per turn
    3. Correct guess: +2 points
    4. Time's up: +1 point to opponent
    5. Max 6 wrong guesses allowed
    6. Words must be 9 letters or less
    
    ⌛ Timer Rules:
    • 30 seconds per turn
    • Red timer = 10 seconds left
    
    🎯 Scoring:
    • Correct guess: +2 points
    • Opponent timeout: +1 point
    """

    rules_label = tk.Label(right_panel, text=rules_text, font=('Poppins', 11),
                          bg="#34495e", fg="#ecf0f1", justify='left', wraplength=250)
    rules_label.pack(fill='x', padx=20)

    # Timer and score
    timer_frame = tk.Frame(left_panel, bg="#2c3e50")
    timer_frame.pack(fill='x', pady=10)

    timer_display = tk.Label(timer_frame, text=f"⏱ Time: {guess_timer}s", 
                           font=('Poppins', 14, 'bold'), bg="#2c3e50", fg="#2ecc71")
    timer_display.pack(side='left')

    live_score_label = tk.Label(timer_frame, text="", font=('Poppins', 14, 'bold'), 
                              bg="#2c3e50", fg="#f1c40f")
    live_score_label.pack(side='right')

    # Word display
    word_frame = tk.Frame(left_panel, bg='#e94560', bd=5, relief='ridge')  # Pink frame
    word_frame.pack(fill='x', pady=20)
    word_label = tk.Label(word_frame, text=" ".join(display), font=('Poppins', 36, 'bold'), 
                         bg='#ffffff', fg='#1a1a2e', padx=20, pady=10)  # White background with dark text
    word_label.pack()

    # Hangman display
    hangman_frame = tk.Frame(left_panel, bg="#2c3e50")
    hangman_frame.pack(fill='x', pady=20)
    hangman_label = tk.Label(hangman_frame, text=Hangman_Stages[tries], font=('Courier', 14), 
                            bg="#2c3e50", fg="white", justify='left')
    hangman_label.pack()

    # Keyboard
    keyboard_frame = tk.Frame(left_panel, bg="#2c3e50")
    keyboard_frame.pack(fill='x', pady=20)

    letter_buttons = {}
    for i, letter in enumerate(string.ascii_lowercase):
        row = i // 7
        col = i % 7
        btn = tk.Button(keyboard_frame, text=letter.upper(), width=4, height=2,
                       font=('Poppins', 12, 'bold'), bg='#0f3460', fg='white',  # Deep blue buttons
                       activebackground='#e94560', command=lambda l=letter: guess_letter(l))  # Pink on hover
        btn.grid(row=row, column=col, padx=5, pady=5)
        letter_buttons[letter] = btn

    # Result message
    result_label = tk.Label(left_panel, text="", font=('Poppins', 18, 'bold'), 
                           bg="#2c3e50", fg="#e74c3c")
    result_label.pack(fill='x', pady=20)

    # Control buttons
    button_frame = tk.Frame(left_panel, bg="#2c3e50")
    button_frame.pack(fill='x', pady=10)

    continue_button = tk.Button(button_frame, text="➡️ Continue", command=continue_game,
                              font=('Poppins', 14), bg="#4CAF50", fg="white",  # Green continue button
                              activebackground="#388E3C", padx=20, pady=10)
    continue_button.pack(side='left', padx=10)
    continue_button.config(state="disabled")

    end_game_button = tk.Button(button_frame, text="🏁 End Game", command=end_game,
                               font=('Poppins', 14), bg='#e94560', fg='white',  # Pink end button
                               activebackground='#d63649', padx=20, pady=10)
    end_game_button.pack(side='left', padx=10)

    # Timer visualization
    timer_canvas = tk.Canvas(left_panel, width=60, height=60, bg='#2c3e50', highlightthickness=0)
    timer_canvas.pack(pady=10)
    timer_canvas.create_oval(5, 5, 55, 55, outline='#3498db', width=3)
    timer_circle = timer_canvas.create_arc(5, 5, 55, 55, start=90, extent=360, 
                                        fill='#3498db', tags='timer_circle')
    timer_text = timer_canvas.create_text(30, 30, text=str(guess_timer), 
                                       font=('Poppins', 14, 'bold'), fill='white')

    # ---------------------
    # Scoreboard
    # ---------------------
    score_title = tk.Label(right_panel, text="SCOREBOARD", font=('Poppins', 24, 'bold'),
                          bg="#34495e", fg="#f1c40f")
    score_title.pack(pady=20)

    score_list = tk.Listbox(right_panel, font=('Poppins', 14), bg="#2c3e50", fg="white",
                          selectmode='none', bd=0, highlightthickness=0)
    score_list.pack(fill='both', expand=True, padx=20)

    # Credits
    credits = tk.Label(right_panel, text="© 2025 Made by Baraa El-Mallah & Adam Doha",
                      font=('Poppins', 10, 'italic'), bg="#34495e", fg="#7f8c8d")
    credits.pack(side='bottom', pady=20)

    # Initialize game
    update_display()
    update_hangman()
    update_score_tab()
    update_timer()

# ---------------------
# Main Application
# ---------------------
root = tk.Tk()
root.title("Hangman Game")
root.attributes('-fullscreen', True)
root.configure(bg="#2c3e50")

# Set the Poppins font if available
try:
    # Try to load Poppins font if it's installed
    custom_font = font.Font(family="Poppins", size=12)
except:
    # Fallback to default font
    custom_font = font.Font(family="Helvetica", size=12)

configure_styles()
create_input_page()

root.mainloop()