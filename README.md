# NetScan Tool

NetScan is a lightweight and portable network utility tool that combines local network scanning, port scanning, and internet speed testing in one convenient package.
Although it's written in Python, the tool has been compiled into a .exe file for Windows users—so no Python installation is required



# 🚀 Features

- 🔍 Device Detection on Local Network: Detects active devices within the local IP range, listing their IP address, hostname, and MAC address.

- 🌐 Internet Speed Test: Measures current ping, download, and upload speeds.

- 🛡️ Port Scanning: Scans the specified IP address for open ports.

- 📝 Logging System: Saves all operations and results to a logs.txt file.

- 🎨 Colorful Terminal Interface: Provides a user-friendly, color-enhanced command-line interface.



# ⚙️ Requirements (If Running as Python File)
If you are running this tool directly from the .py file (instead of .exe), make sure you have:

Python 3.7 or higher

The following Python modules:

speedtest-cli

os (built-in)

socket (built-in)

time (built-in)


### Install the external dependency with:

pip install speedtest-cli



# 💻 Platform Support

✅ Windows (Tested with .exe)

⚠️ macOS/Linux (May work via Python but requires adaptation—no .exe build provided)



# 📁 Output

All network and scan logs will be saved in a file named logs.txt in the working directory.
