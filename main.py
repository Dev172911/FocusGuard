from blocker import block_sites, unblock_sites
import time

def start_focus_session(minutes):
    print(f"\nFocus Mode Started for {minutes} minutes 🔥")
    
    block_sites()
    
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"Time Left: {mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)
        seconds -= 1

    unblock_sites()
    print("\nFocus Session Completed ✅")

def main():
    while True:
        print("\n--- Focus OS ---")
        print("1. Start Focus Mode")
        print("2. Stop Focus Mode")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            minutes = int(input("Enter focus time (minutes): "))
            start_focus_session(minutes)

        elif choice == "2":
            unblock_sites()

        elif choice == "3":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
