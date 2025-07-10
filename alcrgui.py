import customtkinter as ctk
from tkinter import filedialog
import os

# === Import your actual refactoring pipeline ===
from alcr import javatopython, refact, codescan, classifycode

# === App Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ALCR")
app.geometry("800x580")
app.resizable(False, False)

file_path_var = ctk.StringVar()
py_file_path = None

# === File Upload Section ===
file_frame = ctk.CTkFrame(app, width=750, height=180, corner_radius=10)
file_frame.pack(pady=20)

# === Load and place icon ===

icon_label = ctk.CTkLabel(file_frame, text="📄", font=("Arial", 32))
icon_label.pack(pady=(10, 5))

# === Select File Button ===
def select_file():
    path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])
    if path:
        file_path_var.set(path)
        output_box.insert("0.0", f"[INFO] Selected file: {path}\n")

select_button = ctk.CTkButton(file_frame, text="Select java file", command=select_file, width=180)
select_button.pack(pady=(0, 5))

# === Submit Button with actual processing ===
def submit_conversion():
    global py_file_path
    java_path = file_path_var.get()

    if not java_path.endswith(".java"):
        output_box.insert("0.0", "[ERROR] Please select a valid .java file.\n")
        return

    try:
        output_box.insert("0.0", "🔍 Scanning Java code for issues...\n")
        codescan.scanjava(java_path)

        output_box.insert("0.0", "🔍 Classifying Java code...\n")
        classifycode.classify()

        output_box.insert("0.0", "🚀 Converting Java to Python...\n")
        py_file_path = javatopython.convert_java_to_python(java_path)

        output_box.insert("0.0", "🧼 Refactoring Python code...\n")
        refact.refactor_code(py_file_path)

        output_box.insert("0.0", f"🎉 Refactoring complete!\n[RESULT] File saved at: {py_file_path}\n")

        # Load and display converted code
        with open(py_file_path, 'r') as f:
            py_code_box.delete("0.0", "end")
            py_code_box.insert("0.0", f.read())

    except Exception as e:
        output_box.insert("0.0", f"[ERROR] {str(e)}\n")

submit_btn = ctk.CTkButton(app, text="Submit", command=submit_conversion, width=140)
submit_btn.pack(pady=10)

# === Bottom Panel for Output and Python Code ===
bottom_frame = ctk.CTkFrame(app)
bottom_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Output Panel
output_box = ctk.CTkTextbox(bottom_frame, width=380, height=250)
output_box.pack(side="left", padx=(10, 5), pady=10)

# Python File Panel (Removed extra frame)
py_code_box = ctk.CTkTextbox(bottom_frame, width=380, height=250)
py_code_box.pack(side="right", padx=(0, 5), pady=10)


app.mainloop()
