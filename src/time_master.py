try:
  from manager import Manager
  from color import Colors
except ImportError:
  from src.manager import Manager
  from src.color import Colors
import sys
import argparse
import time


class TimeMaster:
    def __init__(self):
        self.style = Colors()
        self.manager = Manager()

    def run(self):
        args = self.parse_arguments()

        if not any(vars(args).values()):
            self.header()
            while True:
                print(self.style.header_msg("\n=== Time Master System ===\n"))
                print(f"{self.style.info_msg('1.')} {self.style.bold_msg('Display Weekly Schedule')}")
                print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Modify Schedule')}")
                print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Task Manager')}")
                print(f"{self.style.info_msg('4.')} {self.style.bold_msg('Exit')}")

                choice = input(self.style.info_msg("\nChoose option (1-4): "))

                if choice == "1":
                    self.manager.display_schedule()
                elif choice == "2":
                    self.manager.modify_schedule()
                elif choice == "3":
                    self.task_manager_menu()
                elif choice == "4":
                    print(self.style.success_msg("\nThank you for using Time Master System. Goodbye!"))
                    break
                else:
                    print(self.style.error_msg("Invalid choice!"))
    
    def task_manager_menu(self):
        while True:
            print(self.style.header_msg("\n=== Task Manager ==="))
            print(f"{self.style.info_msg('1.')} {self.style.bold_msg('View Tasks')}")
            print(f"{self.style.info_msg('2.')} {self.style.bold_msg('Add Task')}")
            print(f"{self.style.info_msg('3.')} {self.style.bold_msg('Edit Task')}")
            print(f"{self.style.info_msg('4.')} {self.style.bold_msg('Remove Task')}")
            print(f"{self.style.info_msg('5.')} {self.style.bold_msg('Mark Task as Complete')}")
            print(f"{self.style.info_msg('6.')} {self.style.bold_msg('Back to Main Menu')}")

            choice = input(self.style.info_msg("\nChoose option (1-6): "))

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
                print(self.style.success_msg("Returning to main menu..."))
                break
            else:
                print(self.style.error_msg("Invalid choice!"))

    def slowprint(self, charge):
        for second in charge + '\n':
            sys.stdout.write(second)
            sys.stdout.flush()
            time.sleep(0.1 / 100)

    def header(self):
        c = self.style
        self.slowprint(f"""
        {c.BOLD}{c.WHITE}============================={c.B_C} =========================================================================={c.RESET}                   

                {c.B_C}▄▄▄█████▓ ██▓ ███▄ ▄███▓▓█████{c.RESET}     ███▄ ▄███▓ ▄▄▄        ██████ ▄▄▄█████▓▓█████  ██▀███
                {c.B_C}▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▓█   ▀{c.RESET}    ▓██▒▀█▀ ██▒▒████▄    ▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
                {c.B_C}▒ ▓██░ ▒░▒██▒▓██    ▓██░▒███{c.RESET}      ▓██    ▓██░▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
                {c.B_C}░ ▓██▓ ░ ░██░▒██    ▒██ ▒▓█  ▄{c.RESET}    ▒██    ▒██ ░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
                {c.B_C}  ▒██▒ ░ ░██░▒██▒   ░██▒░▒████▒{c.RESET}   ▒██▒   ░██▒ ▓█   ▓██▒▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
                {c.B_C}  ▒ ░░   ░▓  ░ ▒░   ░  ░░░ ▒░ ░{c.RESET}   ░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
                {c.B_C}    ░     ▒ ░░  ░      ░ ░ ░  ░{c.RESET}   ░  ░      ░  ▒   ▒▒ ░░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
                {c.B_C}  ░       ▒ ░░      ░      ░{c.RESET}      ░      ░     ░   ▒   ░  ░  ░    ░         ░     ░░   ░
                {c.B_C}          ░         ░      ░  ░{c.RESET}          ░         ░  ░      ░              ░  ░   ░

        {c.B_C}============================={c.BOLD}{c.WHITE} ==========================================================================={c.RESET}
        
        {c.BOLD}{c.WHITE}======================================{c.RESET}
            {c.header_msg(f"{c.B_C}Task Management Application{self.style.RESET}")}
        {c.BOLD}{c.WHITE}======================================{c.RESET}
            {c.bold_msg("Developer:")} {c.info_msg(f"{c.bold_msg("Walid-El-Hioul")}")}
            📎 {c.bold_msg("github.com")}/Walid-El-Hioul/Time_Master
            💼 {c.bold_msg("linkedin.com")}/in/walid-el-hioul
        {c.BOLD}{c.WHITE}======================================{c.RESET}
        """)


    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description=self.style.header_msg('=== Time Master System ==='),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False
        )

        parser.add_argument('-h', '--help', 
            action='help',
            default=argparse.SUPPRESS,
            help=self.style.info_msg('show this help message and exit'))
        parser.add_argument('-s', '--schedule', action='store_true', 
            help=self.style.info_msg('Display weekly schedule'))
        parser.add_argument('--modify-schedule', action='store_true', 
            help=self.style.info_msg('Modify the class schedule'))
        parser.add_argument('-t', '--tasks', action='store_true', 
            help=self.style.info_msg('View all tasks'))
        parser.add_argument('--add-task', action='store_true', 
            help=self.style.info_msg('Add a new task'))

        parser.usage = f"{self.style.info_msg(parser.format_usage().strip())}"

        args = parser.parse_args()
        self.handle_arguments(args)
        return args
    
    def handle_arguments(self, args):
        """Handle the parsed command line arguments"""
        if args.schedule:
            self.manager.display_schedule()
            sys.exit(0)

        if args.modify_schedule:
            self.manager.modify_schedule()
            sys.exit(0)

        if args.tasks:
            self.manager.view_tasks()
            sys.exit(0)

        if args.add_task:
            self.manager.add_task()
            sys.exit(0)

    def slowprint(self, charge):
        for second in charge + '\n':
            sys.stdout.write(second)
            sys.stdout.flush()
            time.sleep(0.1 / 100)


def main():
    time_master = TimeMaster()
    time_master.run()


if __name__ == "__main__":
    main()