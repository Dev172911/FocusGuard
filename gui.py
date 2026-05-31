import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from blocker import block_sites, unblock_sites
from PIL import Image, ImageTk
class FocusOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus OS Ultra")
        self.root.geometry("350x450")
          
        try:
           img = Image.open("icon.png")
           self.icon = ImageTk.PhotoImage(img)
           self.root.iconphoto(True, self.icon)
        except Exception as e:
           print("Icon load failed:", e)
        self.timer_id = None
        self.seconds_left = 0

        tk.Label(root, text="Focus OS 🔥", font=("Helvetica", 20, "bold")).pack(pady=20)
        
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

        # 📊 Graph Button
        self.graph_btn = tk.Button(root, text="SHOW GRAPH 📊", command=self.show_graph,
                                  bg="#007bff", fg="white", width=20)
        self.graph_btn.pack(pady=10)

    # 🔔 Sound
    def play_sound(self):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga &")

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

        messagebox.showinfo("Focus Complete", "Time is up!")

    # 📈 Graph
    def show_graph(self):
        try:
            import matplotlib.pyplot as plt

            times = []
            durations = []

            # Ensure you are reading the correct file
            with open("log.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    
                    if "," in line:
                        t, d = line.split(",")
                        times.append(t[-5:])
                        durations.append(int(d))
                    elif " - " in line:
                        t, d = line.split(" - ")
                        # Strip " minutes" and convert to int
                        val = d.replace(" minutes", "").strip()
                        times.append(t[-5:])
                        durations.append(int(val))

            if not times:
                messagebox.showinfo("No Data", "No sessions yet")
                return

            plt.figure(figsize=(8, 5))
            plt.plot(times, durations, marker='o', linestyle='-', color='b')
            plt.xlabel("Time")
            plt.ylabel("Minutes Focused")
            plt.title("Focus Sessions")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            messagebox.showinfo("No Data", "No log file found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate graph: {str(e)}")
# 🚀 Run
if __name__ == "__main__":
    root = tk.Tk()
    app = FocusOS(root)
    root.mainloop()