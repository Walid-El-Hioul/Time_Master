import sys
import argparse
try:
  from .manager import Manager
except ImportError:
  from manager import Manager



class TimeManager:
  def __init__(self):
      self.manager = Manager()

  def run(self):
      while True:
          print("\n=== Time Management System ===")
          print("1. Display Weekly Schedule")
          print("2. Modify Schedule")
          print("3. Task Manager")
          print("4. Exit")

          choice = input("\nChoose option (1-4): ")

          if choice == "1":
              self.manager.display_schedule()
          elif choice == "2":
              self.manager.modify_schedule()
          elif choice == "3":
              self.task_manager_menu()
          elif choice == "4":
              break
          else:
              print("Invalid choice!")

  def parse_arguments(self):
      """Parse command line arguments"""
      parser = argparse.ArgumentParser(description='Time Management System')
      parser.add_argument('-s', '--schedule', action='store_true', help='Display weekly schedule')
      parser.add_argument('--modify-schedule', action='store_true', help='Modify the class schedule')
      parser.add_argument('-t', '--tasks', action='store_true', help='View all tasks')
      parser.add_argument('--add-task', action='store_true', help='Add a new task')

      args = parser.parse_args()

      if args.schedule:
          self.manager.display_schedule()
          sys.exit(0)
      elif args.modify_schedule:
          self.manager.modify_schedule()
          sys.exit(0)
      elif args.tasks:
          self.manager.view_tasks()
          sys.exit(0)
      elif args.add_task:
          self.manager.add_task()
          sys.exit(0)

  def task_manager_menu(self):
      while True:
          print("\n=== Task Manager ===")
          print("1. View Tasks")
          print("2. Add Task")
          print("3. Edit Task")
          print("4. Remove Task")
          print("5. Mark Task as Complete")
          print("6. Back to Main Menu")

          choice = input("\nChoose option (1-6): ")

          if choice == "1":
              self.manager.view_tasks()
          elif choice == "2":
              self.manager.add_task()
          elif choice == "3":
              self.manager.edit_task()
          elif choice == "4":
              self.manager.remove_task()
          elif choice == "5":
              self.manager.mark_task_complete()
          elif choice == "6":
              break
          else:
              print("Invalid choice!")


def main():
  time_manager = TimeManager()
  time_manager.parse_arguments()
  time_manager.run()

if __name__ == "__main__":
    main()