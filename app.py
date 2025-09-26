import sys
import os


class Calculator:
    """
    Console-based calculator supporting basic arithmetic operations.
    Converted from the original JavaScript calculator.
    """
    
    def __init__(self):
        self.current_input = "0"
        self.previous_input = None
        self.operator = None
        self.waiting_for_input = False
        self.history = []
    
    def display(self):
        """Display the current value"""
        print(f"Display: {self.current_input}")
    
    def input_number(self, num):
        """Input a number digit"""
        if self.waiting_for_input:
            self.current_input = num
            self.waiting_for_input = False
        else:
            self.current_input = num if self.current_input == "0" else self.current_input + num
    
    def input_operator(self, next_operator):
        """Input an operator (+, -, *, /)"""
        if self.previous_input is None:
            self.previous_input = self.current_input
        elif self.operator and not self.waiting_for_input:
            result = self.perform_calculation()
            if result is None:
                return False  # Error occurred
            
            self.current_input = str(result)
            self.previous_input = self.current_input
        
        self.waiting_for_input = True
        self.operator = next_operator
        return True
    
    def calculate(self):
        """Perform the calculation"""
        if self.operator and self.previous_input is not None and not self.waiting_for_input:
            result = self.perform_calculation()
            if result is None:
                return False  # Error occurred
            
            # Store calculation in history
            calculation = f"{self.previous_input} {self.operator} {self.current_input} = {result}"
            self.history.append(calculation)
            
            self.current_input = str(result)
            self.previous_input = None
            self.operator = None
            self.waiting_for_input = True
            return True
        return False
    
    def perform_calculation(self):
        """Perform the actual calculation based on operator"""
        try:
            prev = float(self.previous_input)
            current = float(self.current_input)
        except ValueError:
            print("Error: Invalid number format!")
            return None
        
        if self.operator == "+":
            result = prev + current
        elif self.operator == "-":
            result = prev - current
        elif self.operator == "*":
            result = prev * current
        elif self.operator == "/":
            if current == 0:
                print("Error: Cannot divide by zero!")
                return None
            result = prev / current
        else:
            return None
        
        # Round to avoid floating point errors
        result = round(result * 100000000) / 100000000
        
        # Return integer if result is a whole number
        if result.is_integer():
            return int(result)
        return result
    
    def clear_display(self):
        """Clear the calculator display and reset state"""
        self.current_input = "0"
        self.previous_input = None
        self.operator = None
        self.waiting_for_input = False
    
    def backspace(self):
        """Remove the last entered digit"""
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
    
    def input_decimal(self):
        """Input a decimal point"""
        if self.waiting_for_input:
            self.current_input = "0."
            self.waiting_for_input = False
        elif "." not in self.current_input:
            self.current_input += "."
    
    def show_history(self):
        """Show calculation history"""
        if not self.history:
            print("No calculation history.")
        else:
            print("\n--- Calculation History ---")
            for i, calc in enumerate(self.history[-10:], 1):  # Show last 10
                print(f"{i:2}. {calc}")
            print()


def main():
    """Main function to run the console calculator"""
    calc = Calculator()
    
    print("🧮 Console Calculator")
    print("=" * 30)
    print("Available commands:")
    print("  Numbers: 0-9")
    print("  Operations: +, -, *, /")
    print("  Special: = (calculate), c (clear), b (backspace)")
    print("  Other: h (history), q (quit), help (show this menu)")
    print("=" * 30)
    
    while True:
        calc.display()
        
        try:
            user_input = input("\nEnter command: ").strip().lower()
            
            if user_input == 'q' or user_input == 'quit':
                print("Thank you for using the calculator!")
                break
            elif user_input == 'help':
                print("\nAvailable commands:")
                print("  Numbers: 0-9 (enter digits)")
                print("  Operations: +, -, *, / (arithmetic operators)")
                print("  = : Calculate result")
                print("  c : Clear calculator")
                print("  b : Backspace (remove last digit)")
                print("  . : Decimal point")
                print("  h : Show history")
                print("  q : Quit calculator")
                continue
            elif user_input == 'c':
                calc.clear_display()
                print("Calculator cleared.")
                continue
            elif user_input == 'b':
                calc.backspace()
                continue
            elif user_input == 'h':
                calc.show_history()
                continue
            elif user_input == '=':
                if calc.calculate():
                    print(f"Result: {calc.current_input}")
                else:
                    print("No calculation to perform.")
                continue
            elif user_input in ['+', '-', '*', '/']:
                if calc.input_operator(user_input):
                    print(f"Operator '{user_input}' entered.")
                continue
            elif user_input == '.':
                calc.input_decimal()
                continue
            elif user_input.replace('.', '').isdigit():
                # Handle multi-digit numbers
                calc.input_number(user_input)
                continue
            else:
                print("Invalid input! Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Type 'help' for available commands.")


if __name__ == '__main__':
    main()