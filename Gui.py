import tkinter as tk
import ClassLookup as cl


options = []
SELECT_MSG = "Select an Area of Study"

for key in cl.majorsDict:
    options.append(key)

def check_submission(course_a, course_b):
    return course_a != SELECT_MSG and course_b != SELECT_MSG

def form_str(lst):
    out = ""
    for elem in lst:
        out += elem + "\n"
    return out


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600-100+100")

    input_frame = tk.Frame(root, bg="lightgrey")
    input_frame.place(relwidth='0.8', relheight='0.2', relx='0.1', rely='0.1')

    output_frame = tk.Frame(root, bg="lightgrey")
    output_frame.place(relwidth='0.8', relheight='0.5', relx='0.1', rely='0.4')

    var_a = tk.StringVar(input_frame)
    var_a.set(SELECT_MSG)
    om_a = tk.OptionMenu(input_frame, var_a, *options)
    om_a.place(relx='0.1', rely='0.25')

    var_b = tk.StringVar(input_frame)
    var_b.set(SELECT_MSG)
    om_b = tk.OptionMenu(input_frame, var_b, *options)
    om_b.place(relx='0.9', rely='0.25', anchor='ne')

    var_out = tk.StringVar(output_frame)
    var_out.set("Classes in Common will Show up Here")
    out_text = tk.Label(output_frame, textvariable=var_out)
    out_text.place(relx='0.1', rely='0.1', relwidth='0.8', relheight='0.8')

    def start_check():
        a = var_a.get()
        b = var_b.get()

        print(check_submission(a, b))
        if check_submission(a, b):
            display_str = form_str(cl.full_lookup(a, b))
            var_out.set(display_str)

    submit = tk.Button(input_frame, text="submit", command=start_check)
    submit.place(relx='0.5', rely='0.9', anchor='s')

    root.mainloop()