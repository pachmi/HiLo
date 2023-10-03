// Daniel Thibault
// daniel.thibault@csu.fullerton.edu
// @JustDanielThanks
// Partners: @pachmi

#include <iostream>

int main(int argc, char const *argv[]) {
  // X: Add statements that implement the guessing game described in the
  // README. Then delete this comment.
  int secret_number{0};
  int guess{0};
  std::cout << "Player 1, enter the secret number: ";
  std::cin >> secret_number;
  std::cout << "Player 2, enter your first guess: ";
  std::cin >> guess;
  if (guess == secret_number) {
    std::cout << "Correct, you win!";
  } else if (guess > secret_number) {
    std::cout << "Too high\n";
  } else {
    std::cout << "Too low\n";
  }
  std::cout << "Player 2, enter your second guess: ";
  std::cin >> guess;
  if (guess == secret_number) {
    std::cout << "Correct, you win!";
  } else {
    std::cout << "Incorrect, the secret number was " << secret_number
              << " you lose.";
  }
  return 0;
}
