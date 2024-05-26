import customtkinter as ctk
import tkinter as tk

class CustomPopup(ctk.CTkToplevel):
    def __init__(self, master=None, prompt="", callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.geometry("300x150")
        self.title("Input Dialog")
        
        self.label = ctk.CTkLabel(self, text=prompt)
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.submit)

        # Disable the close button (X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Schedule setting focus to the entry field after a short delay
        self.after(100, self.focus_entry)

    def focus_entry(self):
        self.entry.focus_set()

    def submit(self, event=None):
        if self.callback:
            self.callback(self.entry.get())
        self.destroy()

    def on_closing(self):
        # Disable closing the window
        pass

def show_custom_popup(prompt):
    result = []
    
    def on_submit(value):
        result.append(value)
        root.quit()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    popup = CustomPopup(root, prompt=prompt, callback=on_submit)
    root.mainloop()
    root.destroy()

    return result[0]