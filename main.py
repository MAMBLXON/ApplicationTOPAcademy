import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk


# Создание базы данных и таблицы
def create_db():
    conn = sqlite3.connect('Application.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Application   (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Добавление контакта
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if name and phone and email:
        conn = sqlite3.connect('Application.db')
        c = conn.cursor()
        c.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Контакт успешно добавлен!")
        clear_entries()
        load_Application()
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")


# Загрузка контактов
def load_Application():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('Application.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    for contact in c.fetchall():
        tree.insert("", tk.END, values=contact)
    conn.close()


# Удаление контакта
def delete_contact():
    selected_item = tree.selection()
    if selected_item:
        contact_id = tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('Application.db')
        c = conn.cursor()
        c.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успешно", "Контакт успешно удален!")
        load_Application()
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите контакт для удаления.")


# Очистка полей ввода
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)


# Создание главного окна
root = tk.Tk()
root.title("Книга контактов")

# Поля ввода
tk.Label(root, text="Имя").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Телефон").grid(row=1, column=0)
entry_phone = tk.Entry(root)
entry_phone.grid(row=1, column=1)

tk.Label(root, text="Email").grid(row=2, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1)

# Кнопки
tk.Button(root, text="Добавить контакт", command=add_contact).grid(row=3, columnspan=2)
tk.Button(root, text="Удалить контакт", command=delete_contact).grid(row=4, columnspan=2)

# Таблица для отображения контактов
tree = ttk.Treeview(root, columns=("ID", "Имя", "Телефон", "Email"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Имя", text="Имя")
tree.heading("Телефон", text="Телефон")
tree.heading("Email", text="Email")
tree.grid(row=5, columnspan=2)

# Инициализация базы данных и загрузка контактов
create_db()
load_Application()

root.mainloop()
