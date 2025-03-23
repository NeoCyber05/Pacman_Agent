class Menu:
    def __init__(self):
        self.options = ["Start Game", "Exit"]

    def display(self):
        print("Menu:")
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option}")

    def handle_selection(self, choice):
        if choice == 1:
            self.start_game()
        elif choice == 2:
            self.exit_game()
        else:
            print("Invalid choice. Please select again.")

    def start_game(self):
        print("Starting game...")

    def exit_game(self):
        print("Exiting game...")

    def handle_end_game(self):
        print("Game Over")
        self.display()
        choice = int(input("Select an option: "))
        self.handle_selection(choice)