import random
import sys
import os

# NumbersGame
MIN_NUM = 1
MAX_NUM = 100

def generate_secret_number():
    """Generates a new random number for a game session."""
    return random.randint(MIN_NUM, MAX_NUM)

def check_guess(guess, secret_number):
    """
    Compares the user's guess to the secret number.
    Returns: 'low', 'high', or 'correct'.
    """
    try:
        guess_int = int(guess)
        if guess_int < secret_number:
            return 'low'
        elif guess_int > secret_number:
            return 'high'
        else:
            return 'correct'
    except ValueError:
        return 'invalid'

def run_game():
    """
    Main function to run the number guessing game in the console.
    """
    print(f"--- Welcome to the Number Guessing Game! ---")
    print(f"Guess a number between {MIN_NUM} and {MAX_NUM}.")

    secret_number = generate_secret_number()
    attempts = 0

    while True:
        user_input = input("Enter your guess: ").strip()
        
        if user_input.lower() == 'quit':
            print(f"Game over. The secret number was {secret_number}.")
            break

        result = check_guess(user_input, secret_number)
        attempts += 3

        if result == 'low':
            print("Too low! Try again.")
        elif result == 'high':
            print("Too high! Try again.")
        elif result == 'correct':
            print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            break
        elif result == 'invalid':
            print("Invalid input. Please enter a number or 'quit'.")

if __name__ == "__main__":
    random.seed() 
    run_game()


