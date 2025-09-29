import os
import shutil
import platform
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



def open_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    else:  # Linux and other Unix-like OS
        subprocess.run(["xdg-open", path])

def create_document(output_folder):
    pass
    # create PDF

    # create E-Book

def create_latex_head(photo_path, title, output_folder):
    pass

def create_latex_backbone(output_folder="./output"):
    # ================
    # >>> main doc <<<
    # ================
    main_doc = r"""
    % Load + Define document
    \documentclass[fontsize=11pt,paper=a5,pagesize=auto]{scrbook}

    % Settings
    \include{preambel}

    % Start Document
    \begin{document}

        % Title Page
        \include{titlepage}

        % Add Photo Pages
        \include{photos}

    \end{document}



    """
    with open(os.path.join(output_folder, "main.tex"), "w") as f:
        f.write(main_doc)

    # ====================
    # >>> preambel doc <<<
    # ====================
    preambel_doc = r"""
    % Set margins
    \usepackage[
        a5paper,
        top=2cm,
        bottom=2cm,
        left=2cm,
        right=2cm
    ]{geometry}

    % Font encoding & Font Style
    \usepackage[T1]{fontenc}
    \usepackage{lmodern}
    \usepackage{helvet}
    \renewcommand{\familydefault}{\sfdefault}

    % Dummy Texts
    \usepackage[german]{babel}  % required from blindtext
    \usepackage{blindtext}

    % Better text justification
    \usepackage{microtype}

    % Turn-Off additional space after a sentence
    \frenchspacing

    % Make hpyer links and references and table-of-content clickable
    \usepackage[
        colorlinks=true,
        linkcolor=black,      % for table-of-content & ref
        urlcolor=blue,       % for URL links
        citecolor=blue       % for \cite
    ]{hyperref}

    % For Images
    \usepackage{float}
    \usepackage{graphicx}
    \usepackage{placeins}
    \usepackage{tikz}
    \usetikzlibrary{shadows}"""
    with open(os.path.join(output_folder, "preambel.tex"), "w") as f:
        f.write(preambel_doc)

def create_or_clean_output_folder(output_folder="./output"):
    os.makedirs(output_folder, exist_ok=True)

    shutil.rmtree(output_folder)


def main(photo_path, title, output_folder="./output"):
    create_or_clean_output_folder(output_folder)
    create_latex_backbone(output_folder)
    create_latex_head(photo_path, title, output_folder)
    create_document(output_folder)
    open_folder(output_folder)

def gui():
    def start_button_event(name:str, photo_path:str, output_path:str, output_var, root):
        try:
            main(photo_path=photo_path, title=name, output_folder=output_path)
            output = "Successfull generated your Latex / PDF / Ebook"
        except Exception as e:
            output = f"Error occured: {e}"
        output_var.set(f"Output:\n{output}")
        update_size(root)

    
    def show_warning(root, msg="⚠️ This folder will be cleared!", row=4, column=2, columnspan=2, pady=5):
        # create a warning label
        warning_label = ttk.Label(main_window, text=msg, foreground="red")
        warning_label.grid(row=row, column=column, columnspan=columnspan, pady=pady)

        # remove it after 3 seconds
        root.after(3000, warning_label.destroy)

    def update_size(root):
        root.minsize(0, 0)
        width = root.winfo_width()
        height = root.winfo_height()
        root.geometry('')
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        root.geometry(f"{width}x{height}")

    root = tk.Tk()
    root.title("Auto Photo Album Creator")
    root.geometry("600x400")
    # root.minsize(400, 200)

    main_window = ttk.Frame(root)
    main_window.pack(expand=True, fill='both')

    # make gui title
    header = ttk.Label(
        main_window,
        text="Automatic Photo Album Generator\n📷 -> 📖",
        font=("Segoe UI", 16, "bold"),
        anchor="center",
        justify="center",
        padding=10
    )
    header.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=(10, 20))

    # get title
    input_label = ttk.Label(main_window, text="Title:")
    input_label.grid(row=1, column=1, sticky="e", pady=10, padx=20)

    user_input = tk.StringVar()
    input_entry = ttk.Entry(main_window, textvariable=user_input)
    user_input.set("My awesome photo album")
    input_entry.grid(row=1, column=2, sticky="we", pady=10, padx=20)

    # search photo folder
    def enable_button():
        run_button["state"] = "normal"
        directory_button_open["state"] = "normal"

    selected_directory = tk.StringVar()
    
    def browse_directory():
        path = filedialog.askdirectory()
        if path:
            selected_directory.set(path)
            enable_button()

    browse_button = ttk.Button(main_window, text="Browse Directory", command=browse_directory)
    browse_button.grid(row=2, column=1, columnspan=1, sticky="es", pady=10)

    directory_display = ttk.Label(main_window, textvariable=selected_directory)
    directory_display.grid(row=2, column=2, columnspan=1, sticky="s", pady=13)

    directory_button_open = ttk.Button(main_window, text="Open", command=lambda:open_folder(path=selected_directory.get()))
    directory_button_open.grid(row=2, column=3, columnspan=1, sticky="ws", pady=10)
    directory_button_open["state"] = "disabled"

    # output directoy
    selected_directory_output = tk.StringVar()
    selected_directory_output.set(os.path.abspath("./output"))

    def browse_directory_output():
        path = filedialog.askdirectory()
        if path:
            selected_directory_output.set(path)
            show_warning(root=root, msg="⚠️ This folder will be cleared!", row=3, column=2, columnspan=2, pady=(18, 13))

    browse_button = ttk.Button(main_window, text="Browse Output Directory", command=browse_directory_output)
    browse_button.grid(row=3, column=1, columnspan=1, sticky="en", pady=10)

    directory_display_output = ttk.Label(main_window, textvariable=selected_directory_output)
    directory_display_output.grid(row=3, column=2, columnspan=1, sticky="n", pady=13)

    directory_button_open_output = ttk.Button(main_window, text="Open", command=lambda:open_folder(path=selected_directory_output.get()))
    directory_button_open_output.grid(row=3, column=3, columnspan=1, sticky="wn", pady=10)

    # run button and output label
    output_var = tk.StringVar()
    output_var.set("Output:")
    output_label = ttk.Label(main_window, textvariable=output_var, borderwidth=2)
    output_label.grid(row=5, rowspan=2, column=1, columnspan=2, sticky="nswe", pady=10, padx=20)

    run_button = ttk.Button(main_window, text="Run", command=lambda: start_button_event(user_input.get(), 
                                                                                        selected_directory.get(), 
                                                                                        selected_directory_output.get(), 
                                                                                        output_var, 
                                                                                        root), takefocus=0)
    run_button.grid(row=4, column=1, columnspan=3, sticky="nswe", ipady=10, padx=20)
    run_button["state"] = "disabled"

    # set weights for resizable
    for i in range(7):
        main_window.grid_rowconfigure(i, weight=1)
    for i in range(5):
        main_window.grid_columnconfigure(i, weight=1)

    update_size(root)
    root.geometry("800x600")
    root.mainloop()



if __name__ == "__main__":
    gui()
    # main()

