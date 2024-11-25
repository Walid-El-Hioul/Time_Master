class Colors:
  def __init__(self):
      # Basic colors
      self.RED = '\033[31m'
      self.GREEN = '\033[32m'
      self.YELLOW = '\033[33m'
      self.WHITE = '\033[37m'

      # Bright colors
      self.B_C = '\033[96m'

      # Styles
      self.BOLD = '\033[1m'
      self.UNDERLINE = '\033[4m'
      self.STRIKE = '\033[9m'

      # Reset
      self.RESET = '\033[0m'

  # Notification Methods
  def success_msg(self, text):
      return f"{self.GREEN}{text}{self.RESET}"

  def error_msg(self, text):
      return f"{self.RED}{text}{self.RESET}"

  def warning_msg(self, text):
      return f"{self.YELLOW}{text}{self.RESET}"

  def info_msg(self, text):
      return f"{self.B_C}{text}{self.RESET}"

  # Management Methods
  def header_msg(self, text):
      return f"{self.BOLD}{self.WHITE}{text}{self.RESET}"

  def bold_msg(self, text):
      return f"{self.BOLD}{text}{self.RESET}"

  def underline_msg(self, text):
      return f"{self.UNDERLINE}{text}{self.RESET}"

  def strike_msg(self, text):
      return f"{self.STRIKE}{text}{self.RESET}"

  def priority_msg(self, priority):
      if priority.lower() == "high":
          return f"{self.RED}{priority}{self.RESET}"
      elif priority.lower() == "medium":
          return f"{self.YELLOW}{priority}{self.RESET}"
      else:
          return f"{self.GREEN}{priority}{self.RESET}"

  def status_msg(self, completed):
      return f"{self.GREEN}✓{self.RESET}" if completed else f"{self.RED}✗{self.RESET}"