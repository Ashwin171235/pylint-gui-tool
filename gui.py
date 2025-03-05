import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import subprocess
import os
import threading
import webbrowser

# DARK THEME COLORS
BG_COLOR = "#1e1e1e"  # Dark gray background
TEXT_COLOR = "#ffffff"  # White text
BUTTON_COLOR = "#0078D7"  # Blue buttons
TEXTBOX_COLOR = "#252526"  # Dark gray text box

# Initialize Tkinter window
root = tk.Tk()
root.title("Code Review and Refactoring Tool")
root.geometry("700x500")  # Increased size for better UI
root.configure(bg=BG_COLOR)
root.resizable(True, True)  # Allow resizing

# File selection
tk.Label(root, text="Select Python File:", font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
file_entry = tk.Entry(root, width=50, font=("Arial", 10), bg=TEXTBOX_COLOR, fg=TEXT_COLOR, bd=0)
file_entry.pack(pady=5)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

tk.Button(root, text="Browse", command=select_file, font=("Arial", 10), fg=TEXT_COLOR, bg=BUTTON_COLOR).pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=5)

# Function to run pylint in a separate thread (Real-Time Updates)
def run_analysis():
    file_path = file_entry.get()
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Error", "Please select a valid Python file!")
        return

    # Clear previous output
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

    def run_pylint():
        progress_bar.start()  # Start progress bar
        try:
            process = subprocess.Popen(
                ["pylint", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output_text.config(state=tk.NORMAL)  # Enable text box
            for line in iter(process.stdout.readline, ''):
                output_text.insert(tk.END, line)
                output_text.see(tk.END)  # Auto-scroll
                root.update_idletasks()  # Update UI dynamically
            
            process.stdout.close()
            process.wait()
            progress_bar.stop()  # Stop progress bar
            
            # Extract pylint score and update label
            score_line = [line for line in output_text.get(1.0, tk.END).split("\n") if "rated at" in line]
            if score_line:
                score_label.config(text=f"✅ Pylint Score: {score_line[0].split()[-1]}", fg="light green", bg=BG_COLOR)
            else:
                score_label.config(text="⚠️ No Pylint Score Found", fg="red", bg=BG_COLOR)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run pylint:\n{e}")
        finally:
            output_text.config(state=tk.DISABLED)  # Lock text box

    threading.Thread(target=run_pylint, daemon=True).start()  # Run pylint in background

tk.Button(root, text="Run Code Review", command=run_analysis, font=("Arial", 12), fg=TEXT_COLOR, bg="blue").pack(pady=10)

# Output display (Scrollable Text Box)
output_text = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD, font=("Courier", 10), bg=TEXTBOX_COLOR, fg=TEXT_COLOR)
output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)

# Score label
score_label = tk.Label(root, text="✅ Pylint Score: --", font=("Arial", 12, "bold"), bg=BG_COLOR, fg="light green")
score_label.pack(pady=5)

# Save report function

def save_report():
    report_text = output_text.get(1.0, tk.END).strip()
    if not report_text:
        messagebox.showwarning("Warning", "No output to save!")
        return

    # Ask the user to choose file format (TXT or HTML)
    file_path = filedialog.asksaveasfilename(
        defaultextension="",
        filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html")],
        title="Save Report"
    )

    # If user cancels the save dialog, do nothing
    if not file_path:
        return

    if file_path.endswith(".html"):
        # Generate HTML content with styling
        html_content = f"""
        <html>
        <head>
            <title>Code Review Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #1e1e1e;
                    color: white;
                    padding: 20px;
                }}
                h1 {{
                    color: lightgreen;
                }}
                pre {{
                    background-color: #252526;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <h1>Code Review Report</h1>
            <pre>{report_text}</pre>
        </body>
        </html>
        """

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        messagebox.showinfo("Success", "HTML report saved successfully!")

        # Ask if user wants to open the report
        if messagebox.askyesno("Open Report", "Do you want to open the report now?"):
            webbrowser.open(file_path)

    else:
        # Save as plain text
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        messagebox.showinfo("Success", "Text report saved successfully!")

# Restore the "Save Report" button to the GUI
tk.Button(root, text="Save Report", command=save_report, font=("Arial", 12), fg=TEXT_COLOR, bg="green").pack(pady=10)


# Run the GUI event loop
root.mainloop()
