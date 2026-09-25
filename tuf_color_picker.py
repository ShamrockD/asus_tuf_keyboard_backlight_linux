import os
import sys
import tkinter as tk
from tkinter import messagebox, colorchooser

# Path to the ASUS TUF RGB interface
DRIVER_PATH = "/sys/devices/platform/asus-nb-wmi/leds/asus::kbd_backlight/kbd_rgb_mode"

def apply_color(r, g, b):
    """Writes the RGB color payload directly to the system driver."""
    if not os.path.exists(DRIVER_PATH):
        messagebox.showerror("Error", f"ASUS driver path not found:\n{DRIVER_PATH}\n\nAre you sure this is an ASUS TUF laptop running Linux?")
        return False
        
    # Format: "mode speed R G B extra" (mode 1 = Static, speed 0 = constant)
    payload = f"1 0 {r} {g} {b} 0\n"
    
    try:
        with open(DRIVER_PATH, "w") as f:
            f.write(payload)
        return True
    except PermissionError:
        messagebox.showerror("Permission Denied", "This program must be run with root privileges.\n\nPlease run it via terminal using:\nsudo python3 tuf_color_picker.py")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to driver:\n{str(e)}")
        return False

class TUFColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASUS TUF Keyboard Color Picker")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # Check permissions early (cosmetic warning)
        if os.geteuid() != 0:
            lbl_warn = tk.Label(root, text="⚠️ Warning: Running without 'sudo'", fg="orange", font=("Helvetica", 10, "bold"))
            lbl_warn.pack(pady=5)

        # Title Label
        title = tk.Label(root, text="ASUS TUF Backlight Color", font=("Helvetica", 14, "bold"))
        title.pack(pady=10)

        # Color Preview Block
        self.preview = tk.Frame(root, width=150, height=50, relief=tk.SOLID, borderwidth=1, bg="#00ff96")
        self.preview.pack(pady=10)

        # RGB Slider Framework
        self.r_slider = self.create_slider("Red (R):", "#ff4444", 0)
        self.g_slider = self.create_slider("Green (G):", "#00c851", 255) # Default color, just cuz i like it
        self.b_slider = self.create_slider("Blue (B):", "#33b5e5", 0)
        
        # Color Dialog Palette Button
        btn_palette = tk.Button(root, text="Open Color Wheel", command=self.open_color_dialog)
        btn_palette.pack(pady=5)

        # Action Button
        btn_apply = tk.Button(root, text="Apply to Keyboard", font=("Helvetica", 11, "bold"), 
                              bg="#2bbbad", fg="white", padx=10, pady=5, command=self.on_apply_click)
        btn_apply.pack(pady=15)
        
        self.update_preview()

    def create_slider(self, label_text, color_fg, default_val):
        """Creates a stylized slider row."""
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=20, pady=2)
        
        lbl = tk.Label(frame, text=label_text, width=10, anchor="w", fg=color_fg, font=("Helvetica", 10, "bold"))
        lbl.pack(side=tk.LEFT)
        
        slider = tk.Scale(frame, from_=0, to_=255, orient=tk.HORIZONTAL, command=lambda x: self.update_preview())
        slider.set(default_val)
        slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return slider

    def update_preview(self):
        """Dynamic color preview panel hex converter."""
        r, g, b = self.r_slider.get(), self.g_slider.get(), self.b_slider.get()
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.preview.config(bg=hex_color)

    def open_color_dialog(self):
        """Launches native Linux OS color wheel selector."""
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[0]:  # If a color was selected
            r, g, b = [int(x) for x in color_code[0]]
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b)
            self.update_preview()

    def on_apply_click(self):
        r, g, b = self.r_slider.get(), self.g_slider.get(), self.b_slider.get()
        apply_color(r, g, b)

if __name__ == "__main__":
    window = tk.Tk()
    app = TUFColorPickerApp(window)
    window.mainloop()
