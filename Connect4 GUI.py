from tkinter import *
from tkinter import messagebox
import re

# Global variables for player usernames and passwords
p1_username = None
p1_password = None
p2_username = None
p2_password = None

# Constants
ROWS = 6
COLUMNS = 7

def start_game():
    """
    Function to start the Connect 4 game.
    """
    game_window = Toplevel()
    game_window.title("Connect 4")
    game_window.geometry("700x600")

    player = 'Player1'
    board = [['' for _ in range(COLUMNS)] for _ in range(ROWS)]

    def update_button(row, column):
        btn = board_buttons[row][column]
        if board[row][column] == 'Player1':
            btn.configure(bg="red")
        elif board[row][column] == 'Player2':
            btn.configure(bg="yellow")

    def check_win(player):
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(board[row][col+i] == player for i in range(4)):
                    return True

        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if all(board[row+i][col] == player for i in range(4)):
                    return True

        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(board[row+i][col+i] == player for i in range(4)):
                    return True

        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(board[row-i][col+i] == player for i in range(4)):
                    return True
        return False

    def drop_piece(event):
        column = event.widget.get()
        row = int(event._name[-1])
        if not board[row][int(column)]:
            for i in range(ROWS - 1, -1, -1):
                if board[i][int(column)] == '':
                    board[i][int(column)] = player
                    update_button(i, int(column))
                    if check_win(player):
                        messagebox.showinfo("Game Over", f"Wow {player} wins!")
                        return
                    player = 'Player2' if player == 'Player1' else 'Player1'
                    return

    def check_tie():
        for row in board:
            if '' in row:
                return False
        return True

    def make_move(column):
        nonlocal player
        for row in range(ROWS - 1, -1, -1):
            if board[row][column] == '':
                board[row][column] = player
                update_button(row, column)
                if check_win(player):
                    messagebox.showinfo("Game Over", f"Wow {player} wins!")
                    return
                if check_tie():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    return
                player = 'Player2' if player == 'Player1' else 'Player1'
                return

    board_buttons = [[Button(game_window, bg="blue", width=10, height=4, command=lambda col=column: make_move(col)) for column in range(COLUMNS)] for row in range(ROWS)]

    for row in range(ROWS):
        for column in range(COLUMNS):
            board_buttons[row][column].grid(row=row, column=column, padx=2, pady=2)

def user_entry_window():
    """
    Function to create an entry window for player details.
    """
    global p1_username, p1_password, p2_username, p2_password

    new_window = Toplevel()
    new_window.title("Connect 4 Game")
    new_window.geometry("350x200")

    Label(new_window, text="Player 1:").grid(row=0, column=0)
    Label(new_window, text="Username:").grid(row=1, column=0)
    p1_username = Entry(new_window)
    p1_username.grid(row=1, column=1)

    Label(new_window, text="Password:").grid(row=2, column=0)
    p1_password = Entry(new_window, show="*")
    p1_password.grid(row=2, column=1)

    Label(new_window, text="Player 2:").grid(row=3, column=0)
    Label(new_window, text="Username:").grid(row=4, column=0)
    p2_username = Entry(new_window)
    p2_username.grid(row=4, column=1)

    Label(new_window, text="Password:").grid(row=5, column=0)
    p2_password = Entry(new_window, show="*")
    p2_password.grid(row=5, column=1)
    
    def check_credentials():
        # Defining a password pattern for validation using regex
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'
        
        # Validating Player 1 and Player 2 passwords
        p1_password_valid = re.match(password_pattern, p1_password.get()) is not None
        p2_password_valid = re.match(password_pattern, p2_password.get()) is not None

        if p1_username.get() and p1_password_valid and p2_username.get() and p2_password_valid:
            start_game()  # Start the game if credentials are valid
        else:
            messagebox.showerror("Error", "Invalid username or password. Password must be at least 8 characters long.")

    Button(new_window, text="Submit", command=check_credentials).grid(row=6, columnspan=2)
    
def admin_entry_window():
    """
    Function to open the user entry window.
    """
    new = Toplevel()
    new.title("Connect 4 Game")
    new.geometry("350x200")

    Label(new, text="Enter The Administrator Details:").grid(row=0, column=0)
    Label(new, text="Username:").grid(row=1, column=0)
    username_entry = Entry(new)
    username_entry.grid(row=1, column=1)
    Label(new, text="Password:").grid(row=2, column=0)
    password_entry = Entry(new, show="*")
    password_entry.grid(row=2, column=1)

    def check_credentials():
        if username_entry.get() == "admin" and password_entry.get() == "password":
            admin_panel()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    Button(new, text="Submit", command=check_credentials).grid(row=3, columnspan=2)

def admin_panel():
    """
    Function to create the administrator panel.
    """
    work = Toplevel()
    work.title("Administrator Panel")
    work.geometry("350x200")

    Label(work, text="Enter user details:").grid(row=0, column=0)
    Label(work, text="Username:").grid(row=1, column=0)
    username_entry = Entry(work)
    username_entry.grid(row=1, column=1)
    Label(work, text="Password:").grid(row=2, column=0)
    password_entry = Entry(work, show="*")
    password_entry.grid(row=2, column=1)

    value = IntVar(work)
    Radiobutton(work, text="Create user account", variable=value, value=1).grid(row=4, column=0)
    Radiobutton(work, text="Remove user account", variable=value, value=2).grid(row=5, column=0)

    Button(work, text="Submit", command=lambda: submit_user_info(username_entry, password_entry, value)).grid(row=6, columnspan=2)

def submit_user_info(username_entry, password_entry, value):
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Both username and password are required.")
    elif not is_valid_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters long.")
    else:
        with open("C:/Users/User/Desktop/user_credentials.txt", "a") as file:
            file.write(f"{username}:{password}\n")

        messagebox.showinfo("Success", "User account created successfully.")

def is_valid_password(password):
    """
    Function to check if a password matches the specified policy.
    """
    # Define password policy regex
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'
    return re.match(password_regex, password)

def check_credentials(user1, pass1, user2, pass2):
    with open("C:/Users/User/Desktop/user_credentials.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            username, password = line.strip().split(":")
            if username == user1:
                p1_username.insert(0, username)
                p1_password.insert(0, password)
            elif username == user2:
                p2_username.insert(0, username)
                p2_password.insert(0, password)

root = Tk()
root.title("Connect 4 Game")
root.geometry("250x100")

prompt_label = Label(root, text="Select how you want to enter:")
prompt_label.pack(anchor=W)

radio_value = IntVar()

radio_button1 = Radiobutton(root, text="Administrator", variable=radio_value, value=1)
radio_button2 = Radiobutton(root, text="User/players", variable=radio_value, value=2)

def submit_action():
    if radio_value.get() == 1:
        admin_entry_window()
    elif radio_value.get() == 2:
        user_entry_window()

submit_button = Button(root, text="Submit", command=submit_action)

radio_button1.pack(anchor=W)
radio_button2.pack(anchor=W)
submit_button.pack()

root.mainloop()
