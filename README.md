# Time Master System 📅

> A comprehensive time and task management application with an intuitive CLI interface

## 🌟 Features

### 1. Schedule Management

- Create and manage weekly class schedules
- View available time slots
- Add/remove sessions flexibly
- Color-coded interface for better visibility
- Automatic free slot detection

### 2. Task Management

- Create daily and monthly tasks
- Set priority levels (High/Medium/Low)
- Track task completion status
- Add detailed notes and categories
- Progress tracking with completion percentages

### 3. Smart Organization

- Automatic task sorting by due dates
- Color-coded priorities and statuses
- Overdue task highlighting
- Progress summaries and statistics

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Terminal with color support

### 🚀 Installation
#### Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/Time_Master.git
cd Time_Master
```

### Option 1: Using Virtual Environment (Recommended)
>Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```
or
```bash
python -m venv venv
venv\Scripts\activate     # On Windows

```

### Option 2: System-wide Installation
>If you really need to install system-wide, use one of these 

#### methods:
> Method 1: Using --break-system-packages flag (Not Recommended)
```bash
pip install --break-system-packages -e .
```

> Method 2: Using --user flag (Preferred for system-wide)
```bash
pip install --user -e .
```

⚠️ **Note**: System-wide installation is not recommended. Always prefer using a virtual environment to avoid:
- Package conflicts
- System Python corruption
- Security risks
- Version compatibility issues

## 📖 Usage Guide

### Main Menu

- `1` - Display Weekly Schedule
- `2` - Modify Schedule
- `3` - Task Manager
- `4` - Exit

### Schedule Management

1. View your weekly schedule:

- Shows all classes and free slots
- Color-coded time slots
- Room and professor information

1. Modify schedule:

- Add new sessions
- Remove existing sessions
- Available time slots: 09-11, 11-13, 15-17, 17-19

### Task Management

1. View Tasks:

- Organized by due dates
- Shows priority levels
- Completion status
- Progress tracking

1. Add Tasks:

- Choose daily/monthly
- Set description
- Set due date
- Choose priority level

1. Edit Tasks:

- Modify any task detail
- Update status
- Change priority

## 🎨 Color Coding

- 🔴 Red: High priority/Error messages
- 🟡 Yellow: Medium priority/Warnings
- 🟢 Green: Low priority/Success messages
- 🔵 Blue: Information

## 📁 File Structure

```
time_master_v1.0.0/              # Project root directory
├── src/
│   ├── __init__.py
│   ├── manager.py           # Core management logic
│   ├── color.py            # Color formatting
│   └── time_master.py      # Main application
├── schedule/                   # Schedule storage
├── tasks/                     # Task storage
├── .github/                   # GitHub templates
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License file
├── README.md                # Project documentation
├── pyproject.toml           # Build system requirements
├── setup.cfg               # Package configuration
└── setup.py               # Setup script
```

## ⚙️ Configuration

The system automatically creates necessary directories and files:

- `schedule/schedule.json` - Stores class schedule
- `tasks/*.json` - Stores tasks organized by date

## 🛠️ Command Line Arguments

```
Options:
-h, --help          Show help message-
-s, --schedule      Display weekly schedule
--modify-schedule   Modify the class schedule
-t, --tasks         View all tasks
--add-task         Add a new task
```

## 📝 Notes

- All times are in 24-hour format
- Tasks are automatically sorted by due date
- The system provides visual feedback for all actions
- Use Ctrl+C to cancel any operation

## 🤝 Contributing

1. Fork the repository
1. Create your feature branch
1. Commit your changes
1. Push to the branch
1. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details

## 👤 Author

Walid El-Hioul

- GitHub: [@Walid-El-Hioul](https://github.com/Walid-El-Hioul)
- LinkedIn: [Walid El-Hioul](https://linkedin.com/in/walid-el-hioul)

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by the need for better time management tools

<br>
