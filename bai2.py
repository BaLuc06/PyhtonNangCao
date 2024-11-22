import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='Kuluc27062004')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='tranbaluc')

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create a PanedWindow to split the layout into two sections
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame for connection, insert, delete sections
        left_frame = tk.Frame(paned_window)
        paned_window.add(left_frame, width=300)

        # Right frame for loading data section
        right_frame = tk.Frame(paned_window)
        paned_window.add(right_frame, width=500)

        # Left Frame widgets (Connection, Insert, Delete)
        self.create_connection_widgets(left_frame)
        self.create_insert_widgets(left_frame)
        self.create_delete_widgets(left_frame)

        # Right Frame widgets (Load Data)
        self.create_load_widgets(right_frame)

    def create_connection_widgets(self, parent):
        connection_frame = tk.Frame(parent)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="#").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

    def create_insert_widgets(self, parent):
        insert_frame = tk.Frame(parent)
        insert_frame.pack(pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame, text="mssv:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="hoten:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

    def create_delete_widgets(self, parent):
        delete_frame = tk.Frame(parent)
        delete_frame.pack(pady=10)

        self.delete_mssv = tk.StringVar()

        tk.Label(delete_frame, text="mssv to delete:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(delete_frame, textvariable=self.delete_mssv).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(delete_frame, text="Delete Data", command=self.delete_data).grid(row=1, columnspan=2, pady=10)

    def create_load_widgets(self, parent):
        query_frame = tk.Frame(parent)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        # Create Treeview widget for displaying data in a table format
        self.treeview = ttk.Treeview(parent, columns=("mssv", "hoten"), show="headings")
        self.treeview.heading("mssv", text="MSSV")
        self.treeview.heading("hoten", text="Họ Tên")
        self.treeview.column("mssv", width=100, anchor="center")
        self.treeview.column("hoten", width=200, anchor="w")
        self.treeview.pack(pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Clear existing data in Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Insert data into Treeview
            for row in rows:
                self.treeview.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (mssv, hovaten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def delete_data(self):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (self.delete_mssv.get(),))
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
