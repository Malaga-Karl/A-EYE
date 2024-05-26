import customtkinter as ctk
import tkinter as tk

class CustomPopup(ctk.CTkToplevel):
    def __init__(self, master=None, prompt="", callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.title("Input Dialog")
        
        self.label = ctk.CTkLabel(self, text=prompt)
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.submit)

        # Disable the close button (X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Disable minimizing and maximizing
        self.resizable(False, False)
        self.attributes('-toolwindow', True)  # Hide maximize button
        self.attributes('-topmost', True)  # Keep window on top

        # Flag to track whether input was submitted
        self.input_submitted = False

        # Schedule setting focus to the entry field after a short delay
        self.after(100, self.focus_entry)
        
        # Center the popup on the screen
        self.after(100, self.center_popup)

    def center_popup(self):
        self.update_idletasks()  # Ensure all geometry is calculated
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def focus_entry(self):
        self.entry.focus_set()

    def submit(self, event=None):
        if self.callback:
            self.callback(self.entry.get())
            self.input_submitted = True
        self.destroy()

    def on_closing(self):
        # Disable closing the window
        pass

def show_custom_popup(prompt):
    result = []

    def on_submit(value):
        result.append(value)
        root.quit()

    while True:  # Continuously loop until input is provided
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        popup = CustomPopup(root, prompt=prompt, callback=on_submit)
        root.mainloop()
        root.destroy()

        # Check if the user submitted input or closed the window without submitting
        if popup.input_submitted:
            return result[0]
        else:
            # If the window was closed without submitting, append an empty string to the result
            result.append("")
