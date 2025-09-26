/**
 * Simple Calculator Module
 * Handles basic arithmetic operations: +, -, *, /
 */
class Calculator {
  constructor(displayElementId) {
    this.display = document.getElementById(displayElementId);
    this.currentInput = "0";
    this.previousInput = null;
    this.operator = null;
    this.waitingForInput = false;

    this.initializeEventListeners();
  }

  /**
   * Update the calculator display
   */
  updateDisplay() {
    this.display.textContent = this.currentInput;
  }

  /**
   * Input a number digit
   * @param {string} num - The digit to input
   */
  inputNumber(num) {
    if (this.waitingForInput) {
      this.currentInput = num;
      this.waitingForInput = false;
    } else {
      this.currentInput =
        this.currentInput === "0" ? num : this.currentInput + num;
    }
    this.updateDisplay();
  }

  /**
   * Input an operator
   * @param {string} nextOperator - The operator (+, -, *, /)
   */
  inputOperator(nextOperator) {
    if (this.previousInput === null) {
      this.previousInput = this.currentInput;
    } else if (this.operator && !this.waitingForInput) {
      const result = this.performCalculation();
      if (result === null) return; // Error occurred

      this.currentInput = String(result);
      this.previousInput = this.currentInput;
      this.updateDisplay();
    }

    this.waitingForInput = true;
    this.operator = nextOperator;
  }

  /**
   * Perform the calculation
   */
  calculate() {
    if (this.operator && this.previousInput !== null && !this.waitingForInput) {
      const result = this.performCalculation();
      if (result === null) return; // Error occurred

      this.currentInput = String(result);
      this.previousInput = null;
      this.operator = null;
      this.waitingForInput = true;
      this.updateDisplay();
    }
  }

  /**
   * Perform the actual calculation based on operator
   * @returns {number|null} The result or null if error
   */
  performCalculation() {
    const prev = parseFloat(this.previousInput);
    const current = parseFloat(this.currentInput);

    if (isNaN(prev) || isNaN(current)) return null;

    let result;

    switch (this.operator) {
      case "+":
        result = prev + current;
        break;
      case "-":
        result = prev - current;
        break;
      case "*":
        result = prev * current;
        break;
      case "/":
        if (current === 0) {
          alert("Cannot divide by zero!");
          return null;
        }
        result = prev / current;
        break;
      default:
        return null;
    }

    // Round to avoid floating point errors
    return Math.round(result * 100000000) / 100000000;
  }

  /**
   * Clear the calculator display and reset state
   */
  clearDisplay() {
    this.currentInput = "0";
    this.previousInput = null;
    this.operator = null;
    this.waitingForInput = false;
    this.updateDisplay();
  }

  /**
   * Remove the last entered digit
   */
  backspace() {
    if (this.currentInput.length > 1) {
      this.currentInput = this.currentInput.slice(0, -1);
    } else {
      this.currentInput = "0";
    }
    this.updateDisplay();
  }

  /**
   * Input a decimal point
   */
  inputDecimal() {
    if (this.waitingForInput) {
      this.currentInput = "0.";
      this.waitingForInput = false;
    } else if (this.currentInput.indexOf(".") === -1) {
      this.currentInput += ".";
    }
    this.updateDisplay();
  }

  /**
   * Initialize keyboard and button event listeners
   */
  initializeEventListeners() {
    // Keyboard support
    document.addEventListener("keydown", (event) => {
      this.handleKeyPress(event);
    });

    // Button click effects
    document.addEventListener("DOMContentLoaded", () => {
      const buttons = document.querySelectorAll(".calc-btn");
      buttons.forEach((button) => {
        button.addEventListener("click", function () {
          this.style.transform = "scale(0.95)";
          setTimeout(() => {
            this.style.transform = "scale(1)";
          }, 100);
        });
      });
    });
  }

  /**
   * Handle keyboard input
   * @param {KeyboardEvent} event - The keyboard event
   */
  handleKeyPress(event) {
    const key = event.key;

    if (key >= "0" && key <= "9") {
      this.inputNumber(key);
    } else if (key === "+") {
      this.inputOperator("+");
    } else if (key === "-") {
      this.inputOperator("-");
    } else if (key === "*") {
      this.inputOperator("*");
    } else if (key === "/") {
      event.preventDefault(); // Prevent browser search
      this.inputOperator("/");
    } else if (key === "Enter" || key === "=") {
      event.preventDefault();
      this.calculate();
    } else if (key === "Escape" || key.toLowerCase() === "c") {
      this.clearDisplay();
    } else if (key === "Backspace") {
      event.preventDefault();
      this.backspace();
    } else if (key === ".") {
      this.inputDecimal();
    }
  }
}

// Export for use in other files
if (typeof module !== "undefined" && module.exports) {
  module.exports = Calculator;
} else {
  window.Calculator = Calculator;
}
