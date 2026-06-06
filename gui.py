import tkinter as tk
from tkinter import messagebox
import os
import platform
import subprocess
from datetime import datetime
from blocker import block_sites, unblock_sites
from PIL import Image, ImageTk

class CompactDialog:
    """Custom compact dialog for minimal space"""
    def __init__(self, parent, title, message):
        self.result = None
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("250x100")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Message label
        msg_label = tk.Label(dialog, text=message, font=("Helvetica", 11))
        msg_label.pack(pady=10)
        
        # OK button
        ok_btn = tk.Button(dialog, text="OK", command=dialog.destroy, width=10)
        ok_btn.pack(pady=5)
        
        # Center dialog on parent
        dialog.transient(parent)
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (250 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (100 // 2)
        dialog.geometry(f"+{x}+{y}")

class FocusOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus OS Ultra")
        self.root.geometry("380x600")
        self.photo_img = None  # Keep reference to prevent garbage collection
        self.icon = None
        self._icon_images = []  # For Windows multiple icon sizes
        
        self.timer_id = None
        self.seconds_left = 0

        tk.Label(root, text="Focus OS 🔥", font=("Helvetica", 20, "bold")).pack(pady=10)
        
        # Load and display app icon/image (after title)
        self.load_app_image()
        
        self.entry = tk.Entry(root, font=("Arial", 14), justify="center", width=10)
        self.entry.insert(0, "25")
        self.entry.pack(pady=5)
        
        self.timer_label = tk.Label(root, text="00:00", font=("Courier", 40, "bold"))
        self.timer_label.pack(pady=20)

        self.start_btn = tk.Button(root, text="START FOCUS", command=self.start_focus, 
                                   bg="#28a745", fg="white", width=20)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="STOP", command=self.stop_focus, 
                                  bg="#dc3545", fg="white", width=20, state="disabled")
        self.stop_btn.pack(pady=5)

    # �️ Load App Image
    def load_app_image(self):
        try:
            # Cross-platform path handling
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Try multiple file extensions and locations
            image_names = ["icon.png", "icon.jpg", "icon.jpeg", "app_icon.png", "icon.bmp", "icon.ico"]
            img_path = None
            
            # Check in current directory first
            for img_name in image_names:
                check_path = os.path.join(current_dir, img_name)
                if os.path.exists(check_path):
                    img_path = check_path
                    break
            
            # If not found in script dir, check working directory
            if img_path is None:
                for img_name in image_names:
                    if os.path.exists(img_name):
                        img_path = os.path.abspath(img_name)
                        break
            
            if img_path is None:
                print(f"No icon image found in {current_dir} or current working directory")
                print(f"Searched for: {image_names}")
                return
            
            # Open and resize image
            img = Image.open(img_path)
            
            # Resize to larger size for prominent display (150x150)
            # Use LANCZOS if available (Pillow 10+), otherwise use ANTIALIAS
            resample_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
            img.thumbnail((150, 150), resample_filter)
            
            # Convert to PhotoImage and keep reference
            self.photo_img = ImageTk.PhotoImage(img)
            
            # Display in GUI with frame for better appearance
            frame = tk.Frame(self.root, bg="white", relief="ridge", borderwidth=2)
            frame.pack(pady=15)
            
            img_label = tk.Label(frame, image=self.photo_img, bg="white")
            img_label.pack(padx=5, pady=5)
            
            # Set taskbar icon properly
            self.set_taskbar_icon(img_path, resample_filter)
            
            print(f"App image loaded successfully: {img_path}")
            
        except FileNotFoundError as e:
            print(f"Icon file not found: {e}")
        except Exception as e:
            print(f"Error loading app image: {type(e).__name__}: {e}")
    
    def set_taskbar_icon(self, img_path, resample_filter):
        """Set icon on taskbar (cross-platform)"""
        try:
            icon_img_original = Image.open(img_path)
            
            if platform.system() == "Windows":
                # Windows: Use multiple icon sizes
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
                icon_images = []
                
                for size in icon_sizes:
                    icon_copy = icon_img_original.copy()
                    icon_copy.thumbnail(size, resample_filter)
                    icon_tk = ImageTk.PhotoImage(icon_copy)
                    icon_images.append(icon_tk)
                    self.root.iconphoto(False, icon_tk)
                
                self._icon_images = icon_images
                print("Windows taskbar icon set")
            else:
                # Linux: Set icon and try wmctrl
                icon_img = icon_img_original.copy()
                icon_img.thumbnail((32, 32), resample_filter)
                self.icon = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, self.icon)
                print("Linux taskbar icon set")
                
                # Try to use wmctrl as additional method
                try:
                    self.root.after(1000, self._apply_linux_wmctrl, img_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"Taskbar icon error: {e}")
    
    def _apply_linux_wmctrl(self, img_path):
        """Try to set icon using wmctrl on Linux"""
        try:
            window_id = self.root.winfo_id()
            subprocess.Popen(
                ["xseticon", "-w", str(window_id), img_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except:
            pass

    # �🔔 Sound
    def play_sound(self):
        try:
            if platform.system() == "Windows":
                import winsound
                # Play system sound notification
                winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
            else:
                # Linux
                os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga &")
        except Exception as e:
            print(f"Sound error: {e}")

    # 📊 Save session
    def save_session(self, minutes):
        try:
            with open("log.txt", "a") as f:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                f.write(f"{now},{minutes}\n")
        except Exception as e:
            print("Log error:", e)

    # ⏱ Timer
    def update_timer(self):
        if self.seconds_left > 0:
            mins, secs = divmod(self.seconds_left, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.seconds_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.finish_focus()

    # ▶️ Start
    def start_focus(self):
        try:
            minutes = int(self.entry.get())
            if minutes <= 0:
                raise ValueError

            block_sites()
            self.save_session(minutes)

            self.seconds_left = minutes * 60

            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")

            self.update_timer()

        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    # 🛑 Stop
    def stop_focus(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        unblock_sites()
        self.timer_label.config(text="00:00")

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    # ✅ Finish
    def finish_focus(self):
        unblock_sites()
        self.timer_label.config(text="DONE ✅")
        self.play_sound()

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        CompactDialog(self.root, "Focus Complete", "Time is up!")
# 🚀 Run
if __name__ == "__main__":
    root = tk.Tk()
    app = FocusOS(root)
    root.mainloop()