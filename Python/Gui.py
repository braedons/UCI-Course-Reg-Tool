# pyinstaller Gui.py -F --noconsole --icon=chip_logo.ico

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
import ClassLookup as cl


study_areas_dict = cl.read_studyarea_csv()
options = list(study_areas_dict.keys())
options.sort()
SELECT_MSG = "Select an Area of Study"

def check_submission(course_a, course_b):
    return course_a != SELECT_MSG and course_b != SELECT_MSG

def form_str(lst):
    out = ""
    for elem in lst:
        out += elem + "\n"
    return out


def main():
    root = tk.Tk()
    root.geometry("800x600-100+100")
    root.title("Double Dip")
    # root.iconbitmap("chip_logo.ico") #freepik

    input_frame = tk.Frame(root, bg="lightgrey")
    input_frame.place(relwidth='0.8', relheight='0.2', relx='0.1', rely='0.1')

    output_frame = tk.Frame(root, bg="lightgrey")
    output_frame.place(relwidth='0.8', relheight='0.5', relx='0.1', rely='0.4')
    scrollbar = tk.Scrollbar(output_frame)
    scrollbar.pack(side='right', fill='y')
    my_list = tk.Listbox(output_frame, yscrollcommand=scrollbar.set,)
    my_list.insert(tk.END, "Your classes will appear here")

    my_list.pack( side = 'right', fill = tk.BOTH, expand=1)
    scrollbar.config( command = my_list.yview )

    var_a = tk.StringVar(input_frame)
    var_a.set(SELECT_MSG)
    dropdown_a = ttk.Combobox(input_frame, width=35, textvariable=var_a, values=options, state="readonly")
    dropdown_a.place(relx='0.1', rely='0.25', relwidth='0.4')

    var_b = tk.StringVar(input_frame)
    var_b.set(SELECT_MSG)
    dropdown_b = ttk.Combobox(input_frame, width=35, textvariable=var_b, values=options, state="readonly")
    dropdown_b.place(relx='0.9', rely='0.25', relwidth='0.4', anchor='ne')

    # var_out = tk.StringVar(output_frame)
    # var_out.set("Classes in Common will Show up Here")
    # out_text = tk.Label(output_frame, textvariable=var_out)
    # out_text.place(relx='0.1', rely='0.1', relwidth='0.8', relheight='0.8')

    def start_check():
        a = var_a.get()
        b = var_b.get()

        my_list.delete(0, 'end')
        if check_submission(a, b):
            # display_str = form_str(cl.full_lookup(a, b))
            course_list = cl.full_lookup(a, b, study_areas_dict)
            for course in course_list:
                my_list.insert(tk.END, course)
            # var_out.set(display_str)

    submit = tk.Button(input_frame, text="submit", command=start_check)
    submit.place(relx='0.5', rely='0.9', anchor='s')

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    def update_study_areas():
        cl.find_study_area_urls()
        study_areas_dict = cl.read_studyarea_csv()
        options = list(study_areas_dict.keys())
        options.sort()
        print(options)
        dropdown_a.config(values=options)
        dropdown_b.config(values=options)
    filemenu.add_command(label="Refresh Study Area Choices", command=update_study_areas)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    def export():
        a = var_a.get()
        b = var_b.get()

        # try catch for file name weird symbols
        file = open(a + b + ".txt", "w")
        for course in my_list.get(0, my_list.size()):
            file.write(course + "\n")
        file.close()

        messagebox.showinfo("Export Notification", "Export probably successful?")

    export_button = tk.Button(root, text="Export to txt", command=export)
    export_button.place(relx='0.5', rely='0.98', anchor='s')

    root.mainloop()

if __name__ == "__main__":
    main()