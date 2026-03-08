# cs-black-flash

> Replaces the white flashbang effect with a black screen in CS2, CS:GO and CS 1.6

---

## Preview

[![Watch on YouTube](https://img.youtube.com/vi/lmuxObEzlGs/maxresdefault.jpg)](https://youtube.com/shorts/lmuxObEzlGs)
---

## How it works

Script creates an overlay and then scans a small square in the middle of the screen and when it turns completely white (like whe you are flashbanged), script uses the overlay to change white color to black. Everything else is untouched - flashes will have same duration, same mechanics, just much easier on the eyes. Since Valve still did not implement this, we have to do ourselves!

---

## Installation

1. Install Python. Go to https://www.python.org/downloads/ and download the latest stable version. make sure to click «Add Python to PATH» during installation. 

2. Now run CMD (Win+R) and enter command
   python -m pip install mss numpy

3. Put the script in C: folder or any other and then run Windows Powershell as an admin.

4. In PowerShell run command
   python3 cs2_overlay.py

   Make sure you run it in the same folder as the script, for example if you put script in C: folder you need to run it from C:, so dont forget to change directories using cd command.

5. Enjoy black flashbangs!
   

---



## Notes

- Does NOT interfere with game files
- Uses Windows Display API
- 100% VAC friendly

---

## License

MIT
