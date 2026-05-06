import subprocess
import platform
import re

def display_saved_wifi_passwords():
    """Retrieves and displays saved Wi-Fi SSIDs and passwords on Windows."""

    # 1. System Compatibility Check
    if platform.system() != "Windows":
        print("Error: This specific script is designed for Windows.")
        print("macOS uses the 'security' command, and Linux uses 'nmcli' or NetworkManager files.")
        return

    print("============================================================")
    print(f"{'Wi-Fi Network Name (SSID)':<30} | {'Password'}")
    print("============================================================")

    try:
        # 2. Ask the OS for the list of all saved Wi-Fi profiles
        # Using cp1252 encoding handles special characters common in Windows environments
        profiles_output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            text=True,
            encoding='cp1252'
        )

        # 3. Extract the profile names using a regular expression
        # Looks for "All User Profile : [Network Name]"
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_output)

        if not profiles:
            print("No saved Wi-Fi networks found on this system.")
            return

        # 4. Loop through each discovered network to extract its password
        for profile in profiles:
            profile = profile.strip()

            try:
                # Ask the OS for the specific profile details, including the decrypted key
                profile_info = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                    text=True,
                    encoding='cp1252'
                )

                # Extract the password using regex (Looks for "Key Content : [Password]")
                password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info)

                # Handle networks that have no password (like open public Wi-Fi)
                if password_match:
                    password = password_match.group(1).strip()
                else:
                    password = "{None / Open Network}"

                # Display the result in our formatted table
                print(f"{profile:<30} | {password}")

            except subprocess.CalledProcessError:
                # Triggers if the OS blocks access or the profile is corrupted
                print(f"{profile:<30} | {{Access Denied / Error}}")

    except subprocess.CalledProcessError:
        print("Error: Could not communicate with the Windows Network Shell.")
    except FileNotFoundError:
        print("Error: The 'netsh' command was not found. Are you on a standard Windows machine?")

# --- Run the Tool ---
if __name__ == "__main__":
    display_saved_wifi_passwords()
    print("-" * 60)
