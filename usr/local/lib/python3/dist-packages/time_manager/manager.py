from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
import json
import os


class Manager:
  def __init__(self):
    self.class_schedule = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    self.schedule_path = os.path.join(current_dir, 'schedule', 'schedule.json')
    self.tasks = {"daily": [], "monthly": []}
    self.load_class_schedule()
    self.load_tasks()

  def load_class_schedule(self):
      """Load the class schedule from JSON file"""
      try:
          with open(self.schedule_path, 'r', encoding='utf-8') as file:
              self.class_schedule = json.load(file)
          self.analyze_schedule()
      except FileNotFoundError:
          print("No class schedule found!")
          self.class_schedule = {"schedule": {}}
          self.handle_missing_schedule()

  def handle_missing_schedule(self):
       """Handle the scenario where schedule.json is missing"""
       print("\nSchedule file 'schedule.json' not found.")
       print("1. Create a new schedule")
       print("2. Import existing schedule.json")
       print("3. Exit")

       choice = input("Choose an option (1-3): ")

       if choice == "1":
           self.class_schedule = {"schedule": {}}
           self.modify_schedule()
       elif choice == "2":
           # Using prompt_toolkit for path completion
           filepath = prompt("Enter the path to the existing 'schedule.json' file: ", completer=PathCompleter())
           if os.path.exists(filepath):
               with open(filepath, 'r', encoding='utf-8') as file:
                   self.class_schedule = json.load(file)
               self.save_class_schedule()
               self.analyze_schedule()
               print("Schedule imported successfully.")
           else:
               print("File not found. Please try again.")
               self.handle_missing_schedule()
       elif choice == "3":
           print("Exiting the application.")
           exit()
       else:
           print("Invalid choice!")
           self.handle_missing_schedule()

  def analyze_schedule(self):
      """Analyze class schedule to find free time slots"""
      self.free_slots = {
          "monday": [], "tuesday": [], "wednesday": [],
          "thursday": [], "friday": [], "saturday": []
      }

      time_slots = ["09-11", "11-13", "15-17", "17-19"]

      for day in self.free_slots.keys():
          day_schedule = self.class_schedule.get('schedule', {}).get(day, [])
          busy_times = [class_info['time'] for class_info in day_schedule]

          for slot in time_slots:
              if slot not in busy_times:
                  self.free_slots[day].append(slot)

  def display_schedule(self):
      """Display weekly schedule with classes and free slots"""
      print("\n=== Weekly Schedule ===")
      for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
          print(f"\n{day.upper()}:")
          print("Classes:")
          if day in self.class_schedule.get('schedule', {}):
              for class_info in self.class_schedule['schedule'][day]:
                  print(f"  {class_info['time']}: {class_info['subject']} - Room: {class_info.get('room', 'N/A')}")
          else:
              print("  No classes scheduled.")
          print("Free Slots:")
          if self.free_slots.get(day):
              for slot in self.free_slots[day]:
                  print(f"  {slot}: Available for study/tasks")
          else:
              print("  No free slots.")

  def modify_schedule(self):
      """Modify the class schedule"""
      print("\n=== Modify Schedule ===")
      while True:
          print("\nOptions:")
          print("1. Add a session")
          print("2. Remove a session")
          print("3. View Schedule")
          print("4. Save and Exit")

          choice = input("Choose an option (1-4): ")

          if choice == "1":
              self.add_session()
          elif choice == "2":
              self.remove_session()
          elif choice == "3":
              self.display_schedule()
          elif choice == "4":
              self.save_class_schedule()
              print("Schedule saved successfully.")
              break
          else:
              print("Invalid choice!")

  def add_session(self):
      """Add a class session to the schedule"""
      print("\nAdd a Session")

      day = input("Enter day (e.g., monday): ").lower()
      valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
      if day not in valid_days:
          print("Invalid day!")
          return

      time_slot = input("Enter time slot (e.g., 09-11): ")
      if time_slot not in ["09-11", "11-13", "15-17", "17-19"]:
          print("Invalid time slot!")
          return

      subject = input("Enter subject: ")
      professor = input("Enter professor (optional): ")
      room = input("Enter room (optional): ")

      session = {
          "time": time_slot,
          "subject": subject
      }
      if professor:
          session["professor"] = professor
      if room:
          session["room"] = room

      # Initialize the day's schedule if it doesn't exist
      if 'schedule' not in self.class_schedule:
          self.class_schedule['schedule'] = {}
      if day not in self.class_schedule['schedule']:
          self.class_schedule['schedule'][day] = []

      # Check for conflicts
      existing_times = [s['time'] for s in self.class_schedule['schedule'][day]]
      if time_slot in existing_times:
          print("A session already exists at that time.")
          return

      self.class_schedule['schedule'][day].append(session)
      self.analyze_schedule()
      print("Session added successfully.")

  def remove_session(self):
      """Remove a class session from the schedule"""
      print("\nRemove a Session")

      day = input("Enter day (e.g., monday): ").lower()
      if day not in self.class_schedule.get('schedule', {}):
          print("No sessions scheduled on that day.")
          return

      day_schedule = self.class_schedule['schedule'][day]

      if not day_schedule:
          print("No sessions to remove on that day.")
          return

      print(f"\nSessions on {day.capitalize()}:")
      for idx, session in enumerate(day_schedule, 1):
          print(f"{idx}. {session['time']}: {session['subject']}")

      try:
          session_num = int(input("Enter the session number to remove: ")) - 1
          if 0 <= session_num < len(day_schedule):
              removed_session = day_schedule.pop(session_num)
              self.analyze_schedule()
              print(f"Removed session: {removed_session['subject']} at {removed_session['time']}")
          else:
              print("Invalid session number!")
      except ValueError:
          print("Invalid input! Please enter a number.")

  def save_class_schedule(self):
    """Save the class schedule to 'schedule.json'"""
    try:
        schedule_dir = os.path.dirname(self.schedule_path)
        if not os.path.exists(schedule_dir):
            os.makedirs(schedule_dir)
        
        with open(self.schedule_path, 'w', encoding='utf-8') as f:
            json.dump(self.class_schedule, f, indent=4)
    except Exception as e:
        print(f"Error saving schedule: {e}")

  def save_tasks(self):
      """Save tasks to separate JSON files based on due dates"""
      try:
          tasks_by_date = {}

          for task_type in ["daily", "monthly"]:
              for task in self.tasks[task_type]:
                  due_date = task["due_date"]
                  if due_date not in tasks_by_date:
                      tasks_by_date[due_date] = {"daily": [], "monthly": []}
                  tasks_by_date[due_date][task_type].append(task)

          tasks_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tasks')
          if not os.path.exists(tasks_dir):
              os.makedirs(tasks_dir)
              print(f"Created directory: {tasks_dir}")

          for due_date, tasks in tasks_by_date.items():
              filename = os.path.join(tasks_dir, f'tasks_{due_date}.json')
              try:
                  with open(filename, 'w') as f:
                      json.dump(tasks, f, indent=4)
                  print(f"Saved tasks for {due_date} to {filename}")
              except Exception as e:
                  print(f"Error writing to file {filename}: {e}")

      except Exception as e:
          print(f"Error saving tasks: {e}")

  def load_tasks(self):
      """Load tasks from all JSON files in the tasks directory"""
      try:
          tasks_dir = os.path.join(os.path.dirname(__file__), 'tasks')
          if not os.path.exists(tasks_dir):
              os.makedirs(tasks_dir)
              print(f"Created directory: {tasks_dir}")
              self.tasks = {"daily": [], "monthly": []}
              return

          self.tasks = {"daily": [], "monthly": []}

          for filename in os.listdir(tasks_dir):
              if filename.endswith('.json'):
                  filepath = os.path.join(tasks_dir, filename)
                  with open(filepath, 'r') as f:
                      date_tasks = json.load(f)
                      self.tasks["daily"].extend(date_tasks.get("daily", []))
                      self.tasks["monthly"].extend(date_tasks.get("monthly", []))
      except Exception as e:
          print(f"Error loading tasks: {e}")
          self.tasks = {"daily": [], "monthly": []}

  def view_tasks(self):
      """Display tasks in a formatted way with clear organization"""
      from datetime import datetime

      def format_date(date_str):
          """Format and add status to date based on proximity"""
          task_date = datetime.strptime(date_str, "%Y-%m-%d")
          today = datetime.now()
          days_until = (task_date.date() - today.date()).days

          if days_until < 0:
              return f"{date_str} (OVERDUE)"
          elif days_until == 0:
              return f"{date_str} (TODAY)"
          elif days_until == 1:
              return f"{date_str} (TOMORROW)"
          else:
              return date_str

      # Prepare a combined list of tasks with their types and indices
      # Each element will be (task_type, idx, task)
      self.task_list = []

      # Combine daily and monthly tasks with their type
      all_tasks = []
      for idx, task in enumerate(self.tasks["daily"]):
          all_tasks.append(('daily', idx, task))
      for idx, task in enumerate(self.tasks["monthly"]):
          all_tasks.append(('monthly', idx, task))

      # Sort all tasks by due date and completion status
      all_tasks = sorted(all_tasks, key=lambda x: (
          x[2]['due_date'],  # x[2] is task
          x[2].get('completed', False)
      ))

      current_date_str = datetime.now().strftime("%Y-%m-%d")
      print("\n" + "=" * 60)
      print(f"Task List (Current Date: {current_date_str})")
      print("=" * 60)

      if not all_tasks:
          print("\nNo tasks.")
      else:
          current_date = None
          task_number = 1
          for task_type, idx, task in all_tasks:
              if task['due_date'] != current_date:
                  current_date = task['due_date']
                  formatted_date = format_date(current_date)
                  print(f"\n  Due Date: {formatted_date}")

              status = "✓" if task.get("completed", False) else "×"
              description = task['description']

              priority = task.get('priority', 'normal').upper()

              print(f"    {task_number}. [{status}] [{priority}] ({task_type}) {description}")

              if 'notes' in task and task['notes']:
                  print(f"      Notes: {task['notes']}")
              if 'category' in task and task['category']:
                  print(f"      Category: {task['category']}")

              self.task_list.append((task_type, idx, task))

              task_number += 1

      total_tasks = len(all_tasks)
      completed_tasks = sum(1 for _, _, task in all_tasks
                            if task.get("completed", False))
      pending_tasks = total_tasks - completed_tasks

      if total_tasks > 0:
          completion_percentage = (completed_tasks / total_tasks) * 100
      else:
          completion_percentage = 0

      print("\n" + "-" * 60)
      print("Summary:")
      print(f"  Total Tasks: {total_tasks}")
      print(f"  Completed: {completed_tasks}")
      print(f"  Pending: {pending_tasks}")
      print(f"  Progress: {completion_percentage:.1f}%")
      print("-" * 60 + "\n")

  def get_priority(self, current_priority=None):
      """Helper method to get priority from user input"""
      print("\nPriority Levels:")
      print("1. High")
      print("2. Medium")
      print("3. Low")
      if current_priority:
          print(f"Press Enter to keep current priority ({current_priority.capitalize()})")
      priority_input = input("Select priority (1-3): ")
      priority_map = {
          "1": "high",
          "2": "medium",
          "3": "low"
      }
      if priority_input in priority_map:
          return priority_map[priority_input]
      elif current_priority and priority_input == '':
          return current_priority
      else:
          print("Invalid priority! Setting to medium by default.")
          return "medium"

  def add_task(self):
    print("\nAdd Task")
    task_type = input("Task type (daily/monthly): ").lower()
    if task_type not in ["daily", "monthly"]:
        print("Invalid task type!")
        return

    description = input("Task description: ")

    while True:
        due_date = input("Due date (YYYY-MM-DD): ")
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format or invalid date! Please use YYYY-MM-DD and ensure the date exists.")

    priority = self.get_priority()

    task = {
        "description": description,
        "due_date": due_date,
        "completed": False,
        "priority": priority
    }

    self.tasks[task_type].append(task)
    self.save_tasks()
    print("Task added successfully!")

  def edit_task(self):
      self.view_tasks()
      if not self.task_list:
          print("No tasks to edit.")
          return
      try:
          task_number = int(input("Enter task number to edit: ")) - 1
          if task_number < 0 or task_number >= len(self.task_list):
              print("Invalid task number!")
              return

          task_type, idx, task = self.task_list[task_number]
          print(f"\nEditing task: {task['description']}")

          new_description = input("New description (press Enter to keep current): ")
          new_due_date = input("New due date (YYYY-MM-DD, press Enter to keep current): ")

          priority = self.get_priority(task.get('priority', 'medium'))

          if new_description:
              task['description'] = new_description
          if new_due_date:
              try:
                  datetime.strptime(new_due_date, '%Y-%m-%d')
                  task['due_date'] = new_due_date
              except ValueError:
                  print("Invalid date format! Date not updated.")
          task['priority'] = priority

          self.tasks[task_type][idx] = task

          self.save_tasks()
          print("Task updated successfully!")

      except ValueError:
          print("Invalid input!")

  def remove_task(self):
      self.view_tasks()
      if not self.task_list:
          print("No tasks to remove.")
          return
      try:
          task_number = int(input("Enter task number to remove: ")) - 1
          if task_number < 0 or task_number >= len(self.task_list):
              print("Invalid task number!")
              return

          task_type, idx, removed_task = self.task_list[task_number]

          del self.tasks[task_type][idx]

          self.save_tasks()
          print(f"Removed task: {removed_task['description']}")

      except ValueError:
          print("Invalid input!")

  def mark_task_complete(self):
      self.view_tasks()
      if not self.task_list:
          print("No tasks to mark as complete.")
          return
      try:
          task_number = int(input("Enter task number to mark as complete: ")) - 1
          if task_number < 0 or task_number >= len(self.task_list):
              print("Invalid task number!")
              return

          task_type, idx, task = self.task_list[task_number]
          task['completed'] = True

          self.tasks[task_type][idx] = task

          self.save_tasks()
          print("Task marked as complete!")

      except ValueError:
          print("Invalid input!")