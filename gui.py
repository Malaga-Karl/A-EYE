import tkinter as tk
from tkinter import ttk
import lexer
import syntax
import semantics
import imageio
import re
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip 
from PIL import ImageSequence
import generator
#import generatedCode

table = None

def analyze_code():
    code = text_widget.get("1.0", "end").strip()
    
    placeholder_text = 'Start the code here ...................'
    if code == placeholder_text:
        return
    result, errors = lexer.analyze_text(code)

    terminal_text.config(state="normal")
    terminal_text.delete("1.0", "end")
    if errors:
        for error in errors:
            terminal_text.insert(tk.END, error.as_string() + "\n")
    else:
        terminal_text.insert(tk.END, "Lexical analysis successful" + "\n")
        terminal_text.config(state="disabled")
        terminal_text.tag_configure("success", foreground="green")
        terminal_text.tag_add("success", "1.0", "end")

    table_headers = ["Line #", "Lexeme", "Token"]
    table.delete(*table.get_children()) 
    
    for token in result:
        row = [str(token.line_number), token.value if token.value else "", token.type]
        table.insert("", "end", values=row)

    terminal_text.config(state="disabled")

def analyze_syntax():
    code = text_widget.get("1.0", "end").strip()
    
    placeholder_text = 'Start the code here ...................'
    if code == placeholder_text:
        return
    result, errors = lexer.analyze_text(code)
    if not errors:
        syntax_result = syntax.analyze_syntax(result)
        generator.generate(code)
   

    terminal_text.config(state="normal")
    terminal_text.delete("1.0", "end")
    if errors:
        for error in errors:
            terminal_text.insert(tk.END, error.as_string() + "\n")
        terminal_text.config(state="disabled")
    else:
        output = open("output.txt", "r")
        terminal_text.insert(tk.END, syntax_result + "\n")
        terminal_text.insert(tk.END, output.read() + "\n")
        terminal_text.config(state="disabled")
        if syntax_result == "Output:":
            terminal_text.tag_configure("success", foreground="light green")
            terminal_text.tag_add("success", "1.0", "end")

    table_headers = ["Line #", "Lexeme", "Token"]
    table.delete(*table.get_children()) 
    
    for token in result:
        row = [str(token.line_number), token.value if token.value else "", token.type]
        table.insert("", "end", values=row)

    terminal_text.config(state="disabled")

def analyze_semantics():
    code = text_widget.get("1.0", "end").strip()
    
    placeholder_text = 'Start the code here ...................'
    if code == placeholder_text:
        return
    result, errors = lexer.analyze_text(code)
    if not errors:
        syntax_result = syntax.analyze_syntax(result)
        semantics_result = semantics.analyze(result)

    terminal_text.config(state="normal")
    terminal_text.delete("1.0", "end")
    if errors:
        for error in errors:
            terminal_text.insert(tk.END, error.as_string() + "\n")
        terminal_text.config(state="disabled")
    else:
        terminal_text.insert(tk.END, syntax_result + "\n")
        if syntax_result == "Output:":
            terminal_text.tag_configure("success", foreground="light green")
            terminal_text.tag_add("success", "1.0", "end")
        terminal_text.insert(tk.END, semantics_result + "\n")
        terminal_text.config(state="disabled")
        if semantics_result == "Semantic analysis successful":
            terminal_text.tag_configure("success", foreground="green")
            terminal_text.tag_add("success", "1.0", "end")
        else:
            terminal_text.tag_configure("error", foreground="red") 
            terminal_text.tag_add("error", "end-2l", "end")  
        
    table_headers = ["Line #", "Lexeme", "Token"]
    table.delete(*table.get_children()) 
    
    for token in result:
        row = [str(token.line_number), token.value if token.value else "", token.type]
        table.insert("", "end", values=row)

    terminal_text.config(state="disabled")
    
def update_line_numbers(*args):
    first_line = int(text_widget.index("@0,0").split(".")[0])
    last_line = int(text_widget.index("@0," + str(text_widget.winfo_height())).split(".")[0])

    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    lines = [str(i) for i in range(first_line, last_line + 1)]
    lines_text = "\n".join(lines)
    line_numbers.insert("1.0", lines_text)
    line_numbers.config(state="disabled")

    update_line_visibility(*args)

def update_line_visibility(*args):
    text_widget.yview(*args)
    line_numbers.yview(*args)

def on_enter(event):
    event.widget.config(bg="#2E2E2E")  
    root.config(cursor="hand2")

def on_leave(event):
    event.widget.config(bg="#0F0F0F")  
    root.config(cursor="")

def on_click(event):
    event.widget.config(relief=tk.FLAT)

def on_release(event):
    event.widget.config(relief=tk.FLAT)

def close_app(): #For Delete Button
    root.destroy()

def clear_text_and_outputs():
    text_widget.delete(1.0, "end-1c") 
    table.delete(*table.get_children()) 
    terminal_text.config(state="normal")
    terminal_text.delete("1.0", "end")  
    terminal_text.config(state="disabled")
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    line_numbers.config(state="disabled")

        
def on_delete(event):
    current_text = text_widget.get("1.0", "end-1c")
    current_line_count = int(text_widget.index(tk.END).split(".")[0])

    text_widget.edit_separator()
    text_widget.edit_separator()
    text_widget.edit_delete("insert", tk.END)
    update_line_numbers_on_scroll()
    text_widget.edit_separator()

    new_line_count = int(text_widget.index(tk.END).split(".")[0])
    if current_line_count > new_line_count:
        update_line_numbers_on_scroll()

    text_widget.bind("<Delete>", on_delete)
    
# # #GIF Runtime
# def load_gif_frames(gif_path):
#     gif = Image.open(gif_path)
#     frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
#     return frames

# # #MoviePy Video
# def play_intro():
#     video_path = "A-Eye Intro.mp4"  
#     clip = VideoFileClip(video_path)
#     intro_window = tk.Toplevel(root)
#     intro_window.attributes("-fullscreen", True)
#     clip = clip.resize(width=intro_window.winfo_screenwidth(), height=intro_window.winfo_screenheight())
#     video_label = tk.Label(intro_window)
#     video_label.pack(expand="true", fill="both")
#     clip.preview(fps=24)

#     intro_window.destroy()
#     clip.close() 

# def update_frame(frame_index=0):
#     frame = frames[frame_index]
#     background_label.configure(image=frame)
#     background_label.image = frame  
#     root.after(10, update_frame, (frame_index + 1) % len(frames))  

#Main Window
root = tk.Tk()
root.title("A-Eye Compiler")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.attributes("-fullscreen", True)  # Set full screen
root.configure(bg="#373737")
icon_image = tk.PhotoImage(file="A-Eye Logo.png")
root.iconphoto(True, icon_image)

# gif_path = "background.gif"

# def load_gif_frames(gif_path):
#     reader = imageio.get_reader(gif_path, format='gif')
#     frames = [ImageTk.PhotoImage(Image.fromarray(frame)) for frame in reader]
#     return frames

# frames = load_gif_frames(gif_path)

# play_intro() 

frame_content = tk.Frame(root, bg="#7C1520")
frame_content.place(x=0, y=0, width=screen_width, height=screen_height)

# def update_frame(frame_index=0):
#     frame = frames[frame_index]
#     background_label.configure(image=frame)
#     background_label.image = frame  
#     root.after(100, update_frame, (frame_index + 1) % len(frames))  

background_label = tk.Label(frame_content, bg="#7C1520")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# update_frame()

style = ttk.Style()
style.theme_use("default")

frame_navbar = tk.Frame(root, bg="#0F0F0F")
frame_navbar.place(x=0, y=0, width=screen_width, height=50)

#A-Eye Logo
logo_image = tk.PhotoImage(file="A-Eye Logo.png") 
logo_image = logo_image.subsample(7, 7)  
logo_label = tk.Label(frame_navbar, image=logo_image, bg="#0F0F0F")
logo_label.pack(side="left", padx=10)  

#Title
title_label = tk.Label(frame_navbar, text="A - Eye Compiler", font=("Pirate Scroll", 22), fg="white", bg="#0F0F0F")
title_label.pack(side="left", pady=6)

frame_navbar.lift()
frame_btnsNavBar = tk.Frame(frame_navbar)
frame_btnsNavBar.pack(side="left")  
button_width = 12
button_padding = 5

#Buttons for navigation:




#Lexical Button
btn_lexical = tk.Button(frame_btnsNavBar, text="⚓ Lexical", font=("Pirate Scroll", 16), bg="#0F0F0F", fg="#ff6961", relief="flat", command=analyze_code, width=button_width, padx=10)
btn_lexical.pack(side="left", fill="both", expand=True)
btn_lexical.bind("<Enter>", on_enter)
btn_lexical.bind("<Leave>", on_leave)

#Syntax Button
btn_syntax = tk.Button( frame_btnsNavBar, text="⚓ Syntax", font=("Pirate Scroll", 16), bg="#0F0F0F", fg="#ff6961", relief="flat", command=analyze_syntax, width=button_width, padx=8)
btn_syntax.pack(side="left", fill="both", expand=True)
btn_syntax.bind("<Enter>", on_enter)
btn_syntax.bind("<Leave>", on_leave)

#Semantic button
btn_semantic = tk.Button( frame_btnsNavBar, text="⚓ Semantic", font=("Pirate Scroll", 16), bg="#0F0F0F", fg="#ff6961", relief="flat", command=analyze_semantics, width=button_width, padx=15)
btn_semantic.pack(side="left", fill="both", expand=True)
btn_semantic.bind("<Enter>", on_enter)
btn_semantic.bind("<Leave>", on_leave)
    
#Close Button
btn_close = tk.Button( frame_navbar, text="❌", font=("Pirate Scroll", 11), bg="#0F0F0F", fg="white", relief="flat", command=close_app, width=10, height=30, compound=tk.CENTER, padx=5)
btn_close.pack(side="right")
btn_close.bind("<Enter>", on_enter)
btn_close.bind("<Leave>", on_leave)

#Delete Button
def clear_text_and_outputs(event=None): 
    text_widget.delete("1.0", "end")
    text_widget.config(fg="white", font=("Courier New", 12, "normal"))
    table.delete(*table.get_children())

    terminal_text.config(state="normal", font=("Courier New", 12, "normal"))
    terminal_text.delete("1.0", "end")
    terminal_text.config(state="disabled")

    update_line_numbers()
    
btn_delete = tk.Button( frame_navbar, text="🧹", font=("Pirate Scroll", 15), bg="#0F0F0F", fg="white", relief="flat", command=lambda: (clear_text_and_outputs()), width=10, height=50, compound=tk.CENTER, padx=2)
btn_delete.pack(side="right")

#Text Editor Frame
editor_frame = tk.Frame(frame_content)
editor_frame.place(x=85, y=50, width=1000, height=484)

#Line Numbers Frame
line_number_frame = tk.Frame(editor_frame)
line_number_frame.pack(side="left", fill="y")

text_widget = tk.Text(editor_frame, wrap="none", height=screen_height-50, bg="#121212", fg="white", bd=0, padx=10, font=("Courier New", 12), undo=True, autoseparators=True)
text_widget.pack(side="left", fill="both", expand=True)
text_widget.bind("<Key>", update_line_numbers)
text_widget.config(fg="white", font=("Courier New", 12))
text_widget.focus_set()

text_widget.config(yscrollcommand=lambda *args: (text_widget.yview(*args), update_line_numbers(*args)))

def update_line_numbers_on_scroll(event=None):
    first_visible_line = text_widget.index("@0,0").split(".")[0]
    last_visible_line = text_widget.index("@0," + str(text_widget.winfo_height())).split(".")[0]
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    lines = [str(i) for i in range(int(first_visible_line), int(last_visible_line) + 1)]
    lines_text = "\n".join(lines)
    line_numbers.insert("1.0", lines_text)
    line_numbers.config(state="disabled")

    update_line_visibility()
    
text_widget.bind("<Configure>", update_line_numbers_on_scroll)
text_widget.bind("<MouseWheel>", update_line_numbers_on_scroll)
text_widget.bind("<Button-4>", update_line_numbers_on_scroll)
text_widget.bind("<Button-5>", update_line_numbers_on_scroll)

text_widget.config(insertbackground="#FF6961")    

#Line numbers label
line_numbers = tk.Text(line_number_frame, width=4, bg="#2B2B2B", fg="white", bd=0, wrap="none", font=("Courier New", 12))
line_numbers.pack(fill="both", expand=True)
line_numbers.config(state="disabled")
line_numbers.configure(font=("Courier New", 12, "normal"))

scrollbar = ttk.Scrollbar(editor_frame, command=lambda *args: (text_widget.yview(*args), update_line_numbers(*args)), style="Vertical.TScrollbar")
scrollbar.pack(side="right", fill="y")

style.configure("Vertical.TScrollbar", troughcolor="#121212", gripcount=0, relief="flat")
text_widget.config(yscrollcommand=scrollbar.set)

update_line_numbers()

#Lexical Analyzer Frame
frame_lexical = tk.Frame(frame_content, width=500, height=screen_height-60, bg="#dfd1be")
frame_lexical.place(x=1085, y=50)

table = ttk.Treeview(frame_lexical, selectmode="browse", height=39, columns=("Line Number", "Lexeme", "Token"))
table.pack(side="left", fill="both", expand=True)

table.column("#0", width=0, stretch="no")
table.column("Line Number", anchor="center", width=100, minwidth=100)  
table.column("Lexeme", anchor="center", width=175, minwidth=175)       
table.column("Token", anchor="center", width=175, minwidth=175)        

table.heading("#0", text="", anchor="w")
table.heading("Line Number", text="LINE #", anchor="center")  
table.heading("Token", text="TOKEN", anchor="center")         
table.heading("Lexeme", text="LEXEME", anchor="center")       

style.configure("Treeview.Heading", font=("Pirate Scroll", 16), background="#dfd1be")
style.configure("Treeview", font=("Courier New", 12), background="#dfd1be")

table_scrollbar = ttk.Scrollbar(frame_lexical, orient="vertical", command=table.yview)
table_scrollbar.pack(side="right", fill="y")

table.configure(yscrollcommand=table_scrollbar.set)

style = ttk.Style()
style.configure("Terminal.TFrame", background="#0F0F0F", borderwidth=6, relief="sunken")

#Terminal Frame
frame_terminal = ttk.Frame(frame_content, style="Terminal.TFrame", width=1000, height=330) 
frame_terminal.place(x=85, y=534)

lbl_terminal = tk.Label(frame_terminal, text="TERMINAL :", font=("Pirate Scroll", 14), bg="#0F0F0F", fg="#dfd1be") 
lbl_terminal.place(x=10, y=5)

# Create the terminal text widget with the calculated width
terminal_text = tk.Text(frame_terminal, bg="#0F0F0F", fg="#FF6961", font=("Courier New", 12), width=90, height=16, relief="flat", wrap="word")
terminal_text.place(x=10, y=30)
terminal_text.config(state="disabled")

terminal_scrollbar = ttk.Scrollbar(frame_terminal, command=lambda *args: terminal_text.yview(*args), style="Vertical.TScrollbar")
terminal_scrollbar.place(x=985, y=3, height=324)  
terminal_text['yscrollcommand'] = terminal_scrollbar.set

style.configure("Vertical.TScrollbar", troughcolor="#808080", gripcount=0, relief="flat")


#Other FunctionalitiesL:

#Undo and Redo:
undo_stack = []
redo_stack = []

def undo_action(event=None):
    if undo_stack:
        character = undo_stack.pop()
        redo_stack.append(character)
        text_widget.edit_undo()

def redo_action(event=None):
    if redo_stack:
        character = redo_stack.pop()
        undo_stack.append(character)
        text_widget.edit_redo()

def track_changes(event):
    if event.char and event.keysym != "BackSpace" and event.keysym != "Delete":
        undo_stack.append(event.char)
    elif event.keysym == "":
        char_index = text_widget.index(tk.INSERT)
        if char_index != "1.0":
            character = text_widget.get(char_index + "-1c")
            undo_stack.append(character)
            
text_widget.bind("<Key>", track_changes)

btn_undo = tk.Button(frame_navbar, text="↩️", font=("Pirate Scroll", 11), bg="#0F0F0F", fg="white", relief="flat", command=undo_action, width=10, height=30, compound=tk.CENTER, padx=5)
btn_undo.pack(side="right")
btn_redo = tk.Button(frame_navbar, text="↪️", font=("Pirate Scroll", 11), bg="#0F0F0F", fg="white", relief="flat", command=redo_action, width=10, height=30, compound=tk.CENTER, padx=5)
btn_redo.pack(side="right")

#Colored Reserve Words
def update_text_color(event=None):
    reserved_words = ["onboard", "offboard", "captain", "pint", "fleet", "bull", "doffy", "loyal", "fire", "load", "len", "theo", "alt", "althea", "helm", "chest", "dagger", "four", "whale", "real", "usopp", "and", "oro", "nay", "leak", "sail", "anchor", "pass", "void", "home"]

    text_widget.tag_remove("reserved_words", "1.0", "end")
    text_widget.tag_remove("brackets", "1.0", "end")
    text_widget.tag_remove("quotes", "1.0", "end")

    #For Reserved Words
    for keyword in reserved_words:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        for match in re.finditer(pattern, text_widget.get("1.0", "end"), re.IGNORECASE):
            start_index = "1.0" + "+%dc" % match.start()
            end_index = "1.0" + "+%dc" % match.end()
            text_widget.tag_add("reserved_words", start_index, end_index)

    #For Brackets
    for bracket in ['(', ')', '{', '}', '[', ']']:
        pattern = re.escape(bracket)
        for match in re.finditer(pattern, text_widget.get("1.0", "end")):
            start_index = "1.0" + "+%dc" % match.start()
            end_index = "1.0" + "+%dc" % match.end()
            text_widget.tag_add("brackets", start_index, end_index)
            
    #For Doffy/String
    quote_pairs = [('"', '"'), ("'", "'")]
    for opening, closing in quote_pairs:
        start_index = "1.0"
        while True:
            start_index = text_widget.search(re.escape(opening), start_index, stopindex="end")
            if not start_index:
                break
            end_index = text_widget.search(re.escape(closing), f"{start_index}+1c", stopindex="end")
            if not end_index:
                break
            end_index = f"{end_index}+1c"
            text_widget.tag_add("quotes", start_index, end_index)
            start_index = end_index

    text_widget.tag_config("reserved_words", foreground="#5BBCFF")
    text_widget.tag_config("brackets", foreground="#FDDE55")
    text_widget.tag_config("quotes", foreground="#68D2E8")

    update_line_numbers()

text_widget.bind("<KeyRelease>", update_text_color)

#Indention
def insert_spaces(event):
    text_widget.insert(tk.INSERT, "    ")  
    return 'break'  

text_widget.bind("<Tab>", insert_spaces)
text_widget.indent_level = 0

def indent_next_line(event):
    current_line_index = int(text_widget.index(tk.INSERT).split('.')[0])
    current_line_content = text_widget.get(f"{current_line_index}.0", f"{current_line_index}.end")
    indentation = "    "
    
    leading_spaces = len(current_line_content) - len(current_line_content.lstrip())

    if "{" in current_line_content:
        text_widget.insert(tk.INSERT, "\n" + indentation)
    elif "}" in current_line_content:
        text_widget.indent_level = max(getattr(text_widget, 'indent_level', 0) - 1, 0)
        text_widget.insert(tk.INSERT, "\n" + " " * (text_widget.indent_level * len(indentation)))
        text_widget.see(tk.INSERT)
    else:
        text_widget.insert(tk.INSERT, "\n" + " " * leading_spaces)
    return 'break'

text_widget.bind("<Return>", indent_next_line)

root.mainloop()