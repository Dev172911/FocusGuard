# FocusGuard - Digital Focus & Website Blocker

FocusGuard is a simple productivity application that helps users stay focused by blocking distracting websites for a selected period of time.

It provides a clean graphical interface where users can start a focus session, block unwanted websites, and automatically restore access when the session ends.

---

## Features

* Simple and easy-to-use GUI
* Website blocking during focus sessions
* Automatic unblocking after the timer completes
* Cross-platform support (Windows/Linux)
* Lightweight and fast

---

## Requirements

* Python 3.10 or higher
* Tkinter (included with standard Python installation)
* Pillow

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Dev172911/FocusGuard.git
cd FocusGuard
```

### 2. Create a virtual environment (Recommended)

**Windows:**

```bash
py -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pillow
```

Or use:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the GUI:

```bash
python gui.py
```

or on Windows:

```bash
py gui.py
```

---

## Important Note

### Windows

For website blocking to work correctly, run the application or terminal as **Administrator** because modifying the Windows hosts file requires elevated permissions.

### Linux

You may need to run the application with **sudo** to allow changes to the `/etc/hosts` file.

---

## Project Structure

```
FocusGuard/
│
├── gui.py          # Main graphical interface
├── blocker.py      # Handles website blocking/unblocking
├── main.py         # Command-line version
├── tracker.py      # Tracking functionality
├── config.txt      # Stores blocked websites/settings
├── icon.png        # Application icon
├── dist/           # Compiled application files
└── build/          # Build files
```

---

## Future Improvements

* Custom blocked website list editor
* Better session tracking and analytics
* Notification support
* System tray integration
* Better cross-platform packaging

---

## License

This project is open-source and available under the MIT License.
