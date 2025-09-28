import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import database


database.connect_db()


root = tb.Window(themename="flatly")  # choose theme: flatly, darkly, cyborg, solar, journal
root.title("Student Management System")
root.geometry("1000x600")


title_frame = tb.Frame(root, bootstyle="primary")
title_frame.pack(fill=X)

tb.Label(title_frame, text="📚 Student Management System",
         font=("Segoe UI", 18, "bold"), bootstyle="inverse-primary").pack(pady=10)

frame_form = tb.Labelframe(root, text=" Student Details ", bootstyle="info", padding=15)
frame_form.pack(side=LEFT, fill=Y, padx=10, pady=10)

frame_table = tb.Frame(root, padding=10)
frame_table.pack(side=RIGHT, expand=True, fill=BOTH)

labels = ["Name:", "Roll No:", "Course:", "Year:", "Email:"]
entries = {}

for i, lbl in enumerate(labels):
    tb.Label(frame_form, text=lbl, font=("Segoe UI", 11)).grid(row=i, column=0, sticky="w", pady=5)
    entry = tb.Entry(frame_form, font=("Segoe UI", 10), width=25, bootstyle="info")
    entry.grid(row=i, column=1, pady=5, padx=5)
    entries[lbl[:-1].lower()] = entry


columns = ("id", "name", "roll_no", "course", "year", "email")
tree = tb.Treeview(frame_table, columns=columns, show="headings", bootstyle="info")
tree.pack(expand=True, fill=BOTH, side=LEFT)

for col in columns:
    tree.heading(col, text=col.title())
    tree.column(col, anchor="center", width=150)

scrollbar = tb.Scrollbar(frame_table, command=tree.yview, bootstyle="round-success")
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

def clear_form():
    for entry in entries.values():
        entry.delete(0, "end")

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in database.view_students():
        tree.insert("", "end", values=row)

def add_student():
    data = [entries["name"].get(), entries["roll no"].get(),
            entries["course"].get(), entries["year"].get(), entries["email"].get()]
    if not data[0] or not data[1] or not data[2]:
        messagebox.showwarning("Input Error", "Name, Roll No, and Course are required.")
        return
    try:
        database.insert_student(*data)
        refresh_table()
        clear_form()
        messagebox.showinfo("Success", "Student added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Error", "Please select a record to update")
        return
    student_id = tree.item(selected)["values"][0]
    data = [entries["name"].get(), entries["roll no"].get(),
            entries["course"].get(), entries["year"].get(), entries["email"].get()]
    database.update_student(student_id, *data)
    refresh_table()
    clear_form()
    messagebox.showinfo("Success", "Student updated successfully!")

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Error", "Please select a record to delete")
        return
    student_id = tree.item(selected)["values"][0]
    database.delete_student(student_id)
    refresh_table()
    clear_form()
    messagebox.showinfo("Success", "Student deleted successfully!")

def search_student():
    keyword = entry_search.get()
    results = database.search_student(keyword)
    for row in tree.get_children():
        tree.delete(row)
    for row in results:
        tree.insert("", "end", values=row)

def on_row_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected)["values"]
        clear_form()
        entries["name"].insert(0, values[1])
        entries["roll no"].insert(0, values[2])
        entries["course"].insert(0, values[3])
        entries["year"].insert(0, values[4])
        entries["email"].insert(0, values[5])

tree.bind("<<TreeviewSelect>>", on_row_select)


btn_frame = tb.Frame(frame_form)
btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

tb.Button(btn_frame, text="Add", bootstyle="success-outline", command=add_student, width=10).grid(row=0, column=0, padx=5)
tb.Button(btn_frame, text="Update", bootstyle="warning-outline", command=update_selected, width=10).grid(row=0, column=1, padx=5)
tb.Button(btn_frame, text="Delete", bootstyle="danger-outline", command=delete_selected, width=10).grid(row=1, column=0, padx=5, pady=5)
tb.Button(btn_frame, text="Clear", bootstyle="secondary-outline", command=clear_form, width=10).grid(row=1, column=1, padx=5, pady=5)

search_frame = tb.Frame(root, padding=10)
search_frame.pack(fill=X)
entry_search = tb.Entry(search_frame, font=("Segoe UI", 11), width=40, bootstyle="info")
entry_search.pack(side=LEFT, padx=10)
tb.Button(search_frame, text="Search", bootstyle="primary", command=search_student).pack(side=LEFT, padx=5)
tb.Button(search_frame, text="Show All", bootstyle="secondary", command=refresh_table).pack(side=LEFT, padx=5)

refresh_table()
root.mainloop()
