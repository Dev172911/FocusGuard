import os
import platform

# Determine OS and set hosts path accordingly
if platform.system() == "Windows":
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_PATH = "/etc/hosts"

REDIRECT = "127.0.0.1"

WEBSITES = [
    "youtube.com", "www.youtube.com",
    "m.youtube.com", "youtu.be",
    "facebook.com", "www.facebook.com"
]

def block_sites():
    try:
        with open(HOSTS_PATH, "r+") as file:
            content = file.read()
            for site in WEBSITES:
                if site not in content:
                    file.write(f"\n{REDIRECT} {site}")
        print("Blocked.")
    except PermissionError:
        print("Error: Administrator privileges required to modify hosts file.")
    except Exception as e:
        print(f"Error blocking sites: {e}")

def unblock_sites():
    try:
        with open(HOSTS_PATH, "r+") as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if not any(site in line for site in WEBSITES):
                    file.write(line)

            file.truncate()
        print("Unblocked.")
    except PermissionError:
        print("Error: Administrator privileges required to modify hosts file.")
    except Exception as e:
        print(f"Error unblocking sites: {e}")