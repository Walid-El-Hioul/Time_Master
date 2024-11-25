try:
  from color import Colors
except ImportError:
  from src.color import Colors
from datetime import datetime
import json
import os
import sys


class Manager:
    def __init__(self):
        self.style = Colors()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.schedule_dir = os.path.join(self.current_dir, 'schedule')
        self.tasks_dir = os.path.join(self.current_dir, 'tasks')
        self.schedule_path = os.path.join(self.schedule_dir, 'schedule.json')
        self.tasks = {"daily": [], "monthly": []}

    def load_class_schedule(self):
        """Load the class schedule from JSON file"""
        try:
            with open(self.schedule_path, 'r', encoding='utf-8') as file:
                self.class_schedule = json.load(file)
                self.analyze_schedule()
        except FileNotFoundError:
            print(self.style.warning_msg("No class schedule found!"))
            self.class_schedule = {"schedule": {}}
            self.handle_missing_schedule()

    def save_tasks(self):
        """Save tasks to separate JSON files based on due dates"""
        self.load_tasks()
        try:
            tasks_by_date = {}

            for task_type in ["daily", "monthly"]:
                for task in self.tasks[task_type]:
                    due_date = task["due_date"]
                    if due_date not in tasks_by_date:
                        tasks_by_date[due_date] = {"daily": [], "monthly": []}
                    tasks_by_date[due_date][task_type].append(task)

            for file in os.listdir(self.tasks_dir):
                if file.endswith('.json'):
                    os.remove(os.path.join(self.tasks_dir, file))

            for due_date, tasks in tasks_by_date.items():
                filename = os.path.join(self.tasks_dir, f'tasks_{due_date}.json')
                try:
                    with open(filename, 'w') as f:
                        json.dump(tasks, f, indent=4)
                    print(self.style.success_msg(f"Saved tasks for {due_date}"))
                except Exception as e:
                    print(self.style.error_msg(f"Error writing to file {filename}: {e}"))

        except Exception as e:
            print(self.style.error_msg(f"Error saving tasks: {e}"))

    def handle_missing_schedule(self):
        """Handle the scenario where schedule.json is missing"""
        while True:
            try:
                print(self.style.warning_msg("\nSchedule file not found in the expected location:"))
                print(self.style.info_msg(self.schedule_path))
                print(f"\n{self.style.info_msg('1.')} {self.style.bold_msg('Create a new schedule')}")
                print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Import existing schedule.json')}")
                print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Exit')}")

                choice = input(self.style.info_msg("\nChoose an option (1-3): ")).strip()

                if choice == "1":
                    try:
                        self.load_class_schedule()
                        self.class_schedule = {"schedule": {}}
                        self.modify_schedule()
                        if self.class_schedule["schedule"]:
                            break
                        else:
                            print(self.style.warning_msg("\nSchedule creation was incomplete. Please try again."))
                    except Exception as e:
                        print(self.style.error_msg(f"\nError creating schedule: {str(e)}"))
                        print(self.style.info_msg("Please try again."))

                elif choice == "2":
                    while True:
                        try:
                            self.load_class_schedule()
                            print(self.style.info_msg("\nTip: Press 'Ctrl+C' to cancel import and return to menu"))
                            filepath = input("Enter the path to the existing schedule.json file: ").strip()

                            if filepath.lower() == 'cancel':
                                print(self.style.info_msg("\nImport cancelled. Returning to menu..."))
                                break

                            if os.path.exists(filepath):
                                try:
                                    with open(filepath, 'r', encoding='utf-8') as file:
                                        imported_schedule = json.load(file)

                                    if "schedule" in imported_schedule:
                                        self.class_schedule = imported_schedule
                                        self.save_class_schedule()
                                        self.analyze_schedule()
                                        print(self.style.success_msg("\nSchedule imported successfully."))
                                        return
                                    else:
                                        print(self.style.error_msg("\nInvalid schedule format in the imported file."))
                                        retry = input("Would you like to try another file? (y/n): ").lower()
                                        if retry != 'y':
                                            break
                                except json.JSONDecodeError:
                                    print(self.style.error_msg("\nInvalid JSON file format."))
                                    retry = input("Would you like to try another file? (y/n): ").lower()
                                    if retry != 'y':
                                        break
                            else:
                                print(self.style.error_msg("\nFile not found!"))
                                retry = input("Would you like to try another file? (y/n): ").lower()
                                if retry != 'y':
                                    break

                        except KeyboardInterrupt:
                            print(self.style.info_msg("\nImport cancelled. Returning to menu..."))
                            break
                        except Exception as e:
                            print(self.style.error_msg(f"\nError during import: {str(e)}"))
                            retry = input("Would you like to try again? (y/n): ").lower()
                            if retry != 'y':
                                break

                elif choice == "3":
                    confirm = input(self.style.warning_msg("\nAre you sure you want to exit? (y/n): ")).lower()
                    if confirm == 'y':
                        print(self.style.info_msg("\nExiting the application."))
                        sys.exit(0)

                else:
                    print(self.style.error_msg("\nInvalid choice! Please enter 1, 2, or 3."))

            except KeyboardInterrupt:
                print(self.style.info_msg("\n\nReturning to main menu..."))
                break
            except Exception as e:
                print(self.style.error_msg(f"\nAn error occurred: {str(e)}"))
                print(self.style.info_msg("Please try again."))

        if not hasattr(self, 'class_schedule') or not self.class_schedule.get("schedule"):
            self.class_schedule = {"schedule": {}}

    def analyze_schedule(self):
        """Analyze class schedule to find free time slots"""
        self.load_class_schedule()
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
        self.load_class_schedule()
        print(self.style.header_msg("\n=== Weekly Schedule ==="))
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
            print(f"\n{self.style.bold_msg(day.upper())}:")
            print(self.style.info_msg("Classes:"))
            if day in self.class_schedule.get('schedule', {}):
                for class_info in self.class_schedule['schedule'][day]:
                    print(f"  {self.style.info_msg(class_info['time'])}: "
                            f"{self.style.bold_msg(class_info['subject'])} - "
                            f"Room: {self.style.info_msg(class_info.get('room', 'N/A'))}")
            else:
                print(self.style.warning_msg("  No classes scheduled."))

            print(self.style.info_msg("Free Slots:"))
            if self.free_slots.get(day):
                for slot in self.free_slots[day]:
                    print(f"  {self.style.info_msg(slot)}: "
                            f"{self.style.success_msg('Available for study/tasks')}")
            else:
                print(self.style.warning_msg("  No free slots."))

    def modify_schedule(self):
        """Modify the class schedule"""
        self.load_class_schedule()
        print(self.style.header_msg("\n=== Modify Schedule ==="))
        while True:
            print(self.style.bold_msg("\nOptions:"))
            print(f"{self.style.info_msg('1.')} {self.style.bold_msg('Add a session')}")
            print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Remove a session')}")
            print(f"{self.style.info_msg('3.')} {self.style.bold_msg('View Schedule')}")
            print(f"{self.style.info_msg('4.')} {self.style.bold_msg('Save and Exit')}")

            choice = input(self.style.info_msg("\nChoose an option (1-4): "))

            if choice == "1":
                self.add_session()
            elif choice == "2":
                self.remove_session()
            elif choice == "3":
                self.display_schedule()
            elif choice == "4":
                self.save_class_schedule()
                print(self.style.success_msg("Schedule saved successfully."))
                break
            else:
                print(self.style.error_msg("Invalid choice!"))

    def save_tasks(self):
        """Save tasks to separate JSON files based on due dates"""
        self.load_tasks()
        try:
            tasks_by_date = {}

            for task_type in ["daily", "monthly"]:
                for task in self.tasks[task_type]:
                    due_date = task["due_date"]
                    if due_date not in tasks_by_date:
                        tasks_by_date[due_date] = {"daily": [], "monthly": []}
                    tasks_by_date[due_date][task_type].append(task)

            tasks_dir = os.path.join(self.tasks_dir)
            if not os.path.exists(tasks_dir):
                os.makedirs(tasks_dir)
                print(self.style.success_msg(f"Created directory: {tasks_dir}"))

            for due_date, tasks in tasks_by_date.items():
                filename = os.path.join(tasks_dir, f'tasks_{due_date}.json')
                try:
                    with open(filename, 'w') as f:
                        json.dump(tasks, f, indent=4)
                    print(self.style.success_msg(f"Saved tasks for {due_date} to {filename}"))
                except Exception as e:
                    print(self.style.error_msg(f"Error writing to file {filename}: {e}"))

        except Exception as e:
            print(self.style.error_msg(f"Error saving tasks: {e}"))

    def load_tasks(self):
        """Load tasks from all JSON files in the tasks directory"""
        try:
            self.tasks = {"daily": [], "monthly": []}

            if not os.path.exists(self.tasks_dir):
                os.makedirs(self.tasks_dir)
                return

            for filename in os.listdir(self.tasks_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.tasks_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            date_tasks = json.load(f)
                            self.tasks["daily"].extend(date_tasks.get("daily", []))
                            self.tasks["monthly"].extend(date_tasks.get("monthly", []))
                    except Exception as e:
                        print(self.style.error_msg(f"Error loading {filename}: {e}"))

        except Exception as e:
            print(self.style.error_msg(f"Error loading tasks: {e}"))
            self.tasks = {"daily": [], "monthly": []}

    def get_priority(self, current_priority=None):
        """Helper method to get priority from user input"""
        print(self.style.header_msg("\nPriority Levels:"))
        print(f"{self.style.info_msg('1.')} {self.style.bold_msg('High')}")
        print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Medium')}")
        print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Low')}")

        if current_priority:
            print(self.style.info_msg(f"Press Enter to keep current priority ({current_priority.capitalize()})"))

        priority_input = input(self.style.info_msg("Select priority (1-3): "))
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
            print(self.style.warning_msg("Invalid priority! Setting to medium by default."))
            return "medium"

    def mark_task_complete(self):
        self.load_tasks()
        self.view_tasks()
        if not self.task_list:
            print(self.style.warning_msg("No tasks to mark as complete."))
            return
        try:
            task_number = int(input(self.style.info_msg("Enter task number to mark as complete: "))) - 1
            if task_number < 0 or task_number >= len(self.task_list):
                print(self.style.error_msg("Invalid task number!"))
                return

            task_type, idx, task = self.task_list[task_number]
            task['completed'] = True

            self.tasks[task_type][idx] = task

            self.save_tasks()
            print(self.style.success_msg("Task marked as complete!"))

        except ValueError:
            print(self.style.error_msg("Invalid input!"))

    def add_session(self):
        """Add a class session to the schedule"""
        self.load_class_schedule()
        print(self.style.header_msg("\nAdd a Session"))

        day = input(self.style.info_msg("Enter day (e.g., monday): ")).lower()
        valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        if day not in valid_days:
            print(self.style.error_msg("Invalid day!"))
            return

        time_slot = input(self.style.info_msg("Enter time slot (e.g., 09-11): "))
        if time_slot not in ["09-11", "11-13", "15-17", "17-19"]:
            print(self.style.error_msg("Invalid time slot!"))
            return

        subject = input(self.style.info_msg("Enter subject: "))
        professor = input(self.style.info_msg("Enter professor (optional): "))
        room = input(self.style.info_msg("Enter room (optional): "))

        session = {
            "time": time_slot,
            "subject": subject
        }
        if professor:
            session["professor"] = professor
        if room:
            session["room"] = room
        if 'schedule' not in self.class_schedule:
            self.class_schedule['schedule'] = {}
        if day not in self.class_schedule['schedule']:
            self.class_schedule['schedule'][day] = []

        existing_times = [s['time'] for s in self.class_schedule['schedule'][day]]
        if time_slot in existing_times:
            print(self.style.warning_msg("A session already exists at that time."))
            return

        self.class_schedule['schedule'][day].append(session)
        self.analyze_schedule()
        print(self.style.success_msg("Session added successfully."))

    def remove_session(self):
        """Remove a class session from the schedule"""
        self.load_class_schedule()
        print(self.style.header_msg("\nRemove a Session"))

        day = input(self.style.info_msg("Enter day (e.g., monday): ")).lower()
        if day not in self.class_schedule.get('schedule', {}):
            print(self.style.warning_msg("No sessions scheduled on that day."))
            return

        day_schedule = self.class_schedule['schedule'][day]

        if not day_schedule:
            print(self.style.warning_msg("No sessions to remove on that day."))
            return

        print(self.style.info_msg(f"\nSessions on {day.capitalize()}:"))
        for idx, session in enumerate(day_schedule, 1):
            print(f"{self.style.info_msg(str(idx))}. {session['time']}: {self.style.bold_msg(session['subject'])}")

        try:
            session_num = int(input(self.style.info_msg("Enter the session number to remove: "))) - 1
            if 0 <= session_num < len(day_schedule):
                removed_session = day_schedule.pop(session_num)
                self.analyze_schedule()
                print(self.style.success_msg(
                    f"Removed session: {removed_session['subject']} at {removed_session['time']}")
                )
            else:
                print(self.style.error_msg("Invalid session number!"))
        except ValueError:
            print(self.style.error_msg("Invalid input! Please enter a number."))

    def save_class_schedule(self):
        """Save the class schedule to 'schedule.json'"""
        self.load_class_schedule()
        try:
            schedule_dir = os.path.dirname(self.schedule_path)
            if not os.path.exists(schedule_dir):
                os.makedirs(schedule_dir)

            with open(self.schedule_path, 'w', encoding='utf-8') as f:
                json.dump(self.class_schedule, f, indent=4)
            print(self.style.success_msg("Schedule saved successfully."))
        except Exception as e:
            print(self.style.error_msg(f"Error saving schedule: {e}"))

    def view_tasks(self):
        """Display tasks in a formatted way with clear organization"""
        self.load_tasks()
        def format_date(date_str):
            """Format and add status to date based on proximity"""
            task_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            days_until = (task_date.date() - today.date()).days

            if days_until < 0:
                return f"{date_str} {self.style.error_msg('(OVERDUE)')}"
            elif days_until == 0:
                return f"{date_str} {self.style.warning_msg('(TODAY)')}"
            elif days_until == 1:
                return f"{date_str} {self.style.info_msg('(TOMORROW)')}"
            else:
                return date_str

        self.task_list = []
        all_tasks = []
        for idx, task in enumerate(self.tasks["daily"]):
            all_tasks.append(('daily', idx, task))
        for idx, task in enumerate(self.tasks["monthly"]):
            all_tasks.append(('monthly', idx, task))

        # Sort tasks
        all_tasks = sorted(all_tasks, key=lambda x: (
            x[2]['due_date'],
            x[2].get('completed', False)
        ))

        current_date_str = datetime.now().strftime("%Y-%m-%d")
        print(self.style.header_msg("\n" + "=" * 60))
        print(self.style.header_msg(f"Task List (Current Date: {current_date_str})"))
        print(self.style.header_msg("=" * 60))

        if not all_tasks:
            print(self.style.warning_msg("\nNo tasks."))
        else:
            current_date = None
            task_number = 1
            for task_type, idx, task in all_tasks:
                if task['due_date'] != current_date:
                    current_date = task['due_date']
                    formatted_date = format_date(current_date)
                    print(f"\n  {self.style.bold_msg('Due Date:')} {formatted_date}")

                status = self.style.success_msg("✓") if task.get("completed", False) else self.style.error_msg("×")
                description = task['description']
                priority = self.style.priority_msg(task.get('priority', 'normal'))

                print(f"    {self.style.info_msg(str(task_number))}. [{status}] [{priority}] "
                        f"({self.style.bold_msg(task_type)}) {description}")

                if 'notes' in task and task['notes']:
                    print(f"      {self.style.info_msg('Notes:')} {task['notes']}")
                if 'category' in task and task['category']:
                    print(f"      {self.style.info_msg('Category:')} {task['category']}")

                self.task_list.append((task_type, idx, task))
                task_number += 1

            total_tasks = len(all_tasks)
            completed_tasks = sum(1 for _, _, task in all_tasks if task.get("completed", False))
            pending_tasks = total_tasks - completed_tasks
            completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            print(self.style.header_msg("\n" + "-" * 60))
            print(self.style.bold_msg("Summary:"))
            print(f"  {self.style.info_msg('Total Tasks:')} {total_tasks}")
            print(f"  {self.style.success_msg('Completed:')} {completed_tasks}")
            print(f"  {self.style.warning_msg('Pending:')} {pending_tasks}")
            print(f"  {self.style.info_msg('Progress:')} {completion_percentage:.1f}%")
            print(self.style.header_msg("-" * 60 + "\n"))

    def add_task(self):
        """Add a new task with color formatting and back option"""
        self.load_tasks()
        print(self.style.header_msg("\nAdd Task"))
        print(self.style.info_msg("Type 'back' at any prompt to return to the previous step"))
        print(self.style.info_msg("Type 'cancel' at any prompt to cancel task creation"))

        while True:
            task_type = input(self.style.info_msg("Task type (daily/monthly): ")).lower()
            if task_type == 'cancel':
                print(self.style.warning_msg("Task creation cancelled."))
                return
            if task_type in ["daily", "monthly"]:
                break
            print(self.style.error_msg("Invalid task type! Please enter 'daily' or 'monthly'"))

        while True:
            description = input(self.style.info_msg("Task description: "))
            if description == 'cancel':
                print(self.style.warning_msg("Task creation cancelled."))
                return
            if description == 'back':
                continue
            if description.strip():
                break
            print(self.style.error_msg("Description cannot be empty!"))

        while True:
            due_date = input(self.style.info_msg("Due date (YYYY-MM-DD): "))
            if due_date == 'cancel':
                print(self.style.warning_msg("Task creation cancelled."))
                return
            if due_date == 'back':
                continue
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
                break
            except ValueError:
                print(self.style.error_msg(
                    "Invalid date format! Please use YYYY-MM-DD and ensure the date exists."
                ))

        while True:
            print(self.style.header_msg("\nPriority Levels:"))
            print(f"{self.style.info_msg('1.')} {self.style.bold_msg('High')}")
            print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Medium')}")
            print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Low')}")

            priority_input = input(self.style.info_msg("Select priority (1-3): "))
            if priority_input == 'cancel':
                print(self.style.warning_msg("Task creation cancelled."))
                return
            if priority_input == 'back':
                continue

            priority_map = {"1": "high", "2": "medium", "3": "low"}
            if priority_input in priority_map:
                priority = priority_map[priority_input]
                break
            print(self.style.error_msg("Invalid priority! Please select 1, 2, or 3"))

        print("\nTask Summary:")
        print(f"Type: {self.style.bold_msg(task_type)}")
        print(f"Description: {self.style.bold_msg(description)}")
        print(f"Due Date: {self.style.bold_msg(due_date)}")
        print(f"Priority: {self.style.bold_msg(priority)}")

        confirm = input(self.style.info_msg("\nConfirm task creation? (y/n): ")).lower()
        if confirm != 'y':
            print(self.style.warning_msg("Task creation cancelled."))
            return

        task = {
            "description": description,
            "due_date": due_date,
            "completed": False,
            "priority": priority
        }

        self.tasks[task_type].append(task)
        self.save_tasks()
        print(self.style.success_msg("Task added successfully!"))

    def edit_task(self):
        """Edit an existing task with color formatting and back option"""
        self.load_tasks()
        self.view_tasks()
        if not self.task_list:
            print(self.style.warning_msg("No tasks to edit."))
            return

        print(self.style.info_msg("Type 'back' at any prompt to return to the previous step"))
        print(self.style.info_msg("Type 'cancel' at any prompt to cancel editing"))

        while True:
            task_input = input(self.style.info_msg("Enter task number to edit: "))
            if task_input == 'cancel':
                print(self.style.warning_msg("Task editing cancelled."))
                return

            try:
                task_number = int(task_input) - 1
                if 0 <= task_number < len(self.task_list):
                    break
                print(self.style.error_msg("Invalid task number!"))
            except ValueError:
                print(self.style.error_msg("Please enter a valid number"))

        task_type, idx, task = self.task_list[task_number]
        print(f"\n{self.style.header_msg('Editing task:')} {self.style.bold_msg(task['description'])}")

        while True:
            new_description = input(self.style.info_msg("New description (press Enter to keep current): "))
            if new_description == 'cancel':
                print(self.style.warning_msg("Task editing cancelled."))
                return
            if new_description == 'back':
                continue
            if new_description or new_description == '':
                break

        while True:
            new_due_date = input(self.style.info_msg("New due date (YYYY-MM-DD, press Enter to keep current): "))
            if new_due_date == 'cancel':
                print(self.style.warning_msg("Task editing cancelled."))
                return
            if new_due_date == 'back':
                continue
            if not new_due_date:
                break
            try:
                datetime.strptime(new_due_date, '%Y-%m-%d')
                break
            except ValueError:
                print(self.style.error_msg("Invalid date format! Please use YYYY-MM-DD"))

        current_priority = task.get('priority', 'medium')
        while True:
            print(self.style.header_msg("\nPriority Levels:"))
            print(f"{self.style.info_msg('1.')} {self.style.bold_msg('High')}")
            print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Medium')}")
            print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Low')}")
            print(self.style.info_msg(f"Current priority: {current_priority}"))

            priority_input = input(self.style.info_msg("Select new priority (1-3, press Enter to keep current): "))
            if priority_input == 'cancel':
                print(self.style.warning_msg("Task editing cancelled."))
                return
            if priority_input == 'back':
                continue
            if priority_input == '':
                priority = current_priority
                break

            priority_map = {"1": "high", "2": "medium", "3": "low"}
            if priority_input in priority_map:
                priority = priority_map[priority_input]
                break
            print(self.style.error_msg("Invalid priority! Please select 1, 2, or 3"))

        print("\nProposed Changes:")
        if new_description:
            print(f"Description: {self.style.bold_msg(task['description'])} → {self.style.bold_msg(new_description)}")
        if new_due_date:
            print(f"Due Date: {self.style.bold_msg(task['due_date'])} → {self.style.bold_msg(new_due_date)}")
        if priority != current_priority:
            print(f"Priority: {self.style.bold_msg(current_priority)} → {self.style.bold_msg(priority)}")

        confirm = input(self.style.info_msg("\nConfirm these changes? (y/n): ")).lower()
        if confirm != 'y':
            print(self.style.warning_msg("Task editing cancelled."))
            return

        if new_description:
            task['description'] = new_description
        if new_due_date:
            task['due_date'] = new_due_date
        task['priority'] = priority

        self.tasks[task_type][idx] = task
        self.save_tasks()
        print(self.style.success_msg("Task updated successfully!"))

    def remove_task(self):
        """Remove a task with color formatting and confirmation"""
        self.load_tasks()
        self.view_tasks()
        if not self.task_list:
            print(self.style.warning_msg("No tasks to remove."))
            return

        try:
            task_number = int(input(self.style.info_msg("Enter task number to remove: "))) - 1
            if task_number < 0 or task_number >= len(self.task_list):
                print(self.style.error_msg("Invalid task number!"))
                return

            task_type, idx, task = self.task_list[task_number]

            print("\nTask to remove:")
            print(f"Description: {self.style.bold_msg(task['description'])}")
            print(f"Due Date: {self.style.bold_msg(task['due_date'])}")
            print(f"Priority: {self.style.bold_msg(task.get('priority', 'medium'))}")
            print(f"Type: {self.style.bold_msg(task_type)}")

            confirm = input(self.style.warning_msg("\nAre you sure you want to remove this task? (y/n): ")).lower()
            if confirm != 'y':
                print(self.style.info_msg("Task removal cancelled."))
                return

            self.tasks[task_type].pop(idx)
            
            if os.path.exists(self.tasks_dir):
                for file in os.listdir(self.tasks_dir):
                    if file.endswith('.json'):
                        os.remove(os.path.join(self.tasks_dir, file))
            
            self.save_tasks()

            self.load_tasks()
            
            print(self.style.success_msg(f"Successfully removed task: {task['description']}"))

        except ValueError:
            print(self.style.error_msg("Invalid input! Please enter a valid task number."))
        except Exception as e:
            print(self.style.error_msg(f"Error removing task: {str(e)}"))