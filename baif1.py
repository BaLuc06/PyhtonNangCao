import tkinter as tk
from tkinter import messagebox

# Hàm xử lý khi nhấn nút Gửi
def submit_info():
    name = entry_name.get()
    phone = entry_phone.get()
    school = entry_school.get()
    
    if name and phone and school:
        messagebox.showinfo("Thông tin sinh viên", f"Tên: {name}\nSố điện thoại: {phone}\nTrường: {school}")
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")

# Tạo cửa sổ chính với kích thước lớn hơn
root = tk.Tk()
root.title("Thông tin sinh viên")
root.geometry("400x300")  # Kích thước cửa sổ lớn hơn

# Tạo các nhãn và ô nhập liệu với khoảng cách rộng hơn
tk.Label(root, text="Tên:", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
entry_name = tk.Entry(root, width=40, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=20, pady=10)

tk.Label(root, text="Số điện thoại:", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
entry_phone = tk.Entry(root, width=40, font=("Arial", 12))
entry_phone.grid(row=1, column=1, padx=20, pady=10)

tk.Label(root, text="Trường:", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
entry_school = tk.Entry(root, width=40, font=("Arial", 12))
entry_school.grid(row=2, column=1, padx=20, pady=10)

# Tạo nút gửi với kích thước lớn hơn
btn_submit = tk.Button(root, text="ENTER", font=("Arial", 12), command=submit_info)
btn_submit.grid(row=3, column=0, columnspan=2, pady=20)

# Chạy vòng lặp chính
root.mainloop()
