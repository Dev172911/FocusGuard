HOSTS_PATH = "/etc/hosts"
REDIRECT = "127.0.0.1"

WEBSITES = [
    "youtube.com", "www.youtube.com",
    "m.youtube.com", "youtu.be",
    "facebook.com", "www.facebook.com"
]

def block_sites():
    with open(HOSTS_PATH, "r+") as file:
        content = file.read()
        for site in WEBSITES:
            if site not in content:
                file.write(f"\n{REDIRECT} {site}")
    print("Blocked.")

def unblock_sites():
    with open(HOSTS_PATH, "r+") as file:
        lines = file.readlines()
        file.seek(0)

        for line in lines:
            if not any(site in line for site in WEBSITES):
                file.write(line)

        file.truncate()
    print("Unblocked.")