import os
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_folder():
    """打开文件夹选择对话框"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)

def start_renaming():
    """执行重命名逻辑"""
    folder = folder_var.get()
    prefix = prefix_var.get()
    start_num_str = start_num_var.get()
    new_ext = ext_var.get()

    # 1. 检查文件夹路径
    if not os.path.isdir(folder):
        messagebox.showerror("错误", "请选择一个有效的文件夹路径！")
        return

    # 2. 检查起始数字
    try:
        start_num = int(start_num_str)
    except ValueError:
        messagebox.showerror("错误", "起始数字必须是整数！")
        return

    # 3. 处理后缀名格式 (如果用户输入了扩展名，确保包含 ".")
    if new_ext and not new_ext.startswith('.'):
        new_ext = '.' + new_ext

    # 获取文件夹中的所有文件（排除子文件夹），并按名称排序
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.sort()
    
    if not files:
        messagebox.showinfo("提示", "该文件夹中没有任何文件。")
        return

    success_count = 0
    log_text.delete(1.0, tk.END) # 清空日志窗口

    # 为了让编号对齐（例如 01, 02... 10），计算需要填充的零的个数
    max_num_length = len(str(start_num + len(files) - 1))

    for i, filename in enumerate(files):
        old_path = os.path.join(folder, filename)
        
        # 处理后缀名
        if new_ext:
            ext = new_ext
        else:
            _, ext = os.path.splitext(filename) # 保持原后缀

        # 格式化数字，自动补零
        current_num = start_num + i
        num_str = str(current_num).zfill(max_num_length)
        
        # 拼接新文件名
        new_name = f"{prefix}{num_str}{ext}"
        new_path = os.path.join(folder, new_name)

        # 执行重命名
        try:
            # 防止同名文件覆盖
            if os.path.exists(new_path) and old_path != new_path:
                 log_text.insert(tk.END, f"跳过: {new_name} 已存在\n")
                 continue
                 
            os.rename(old_path, new_path)
            success_count += 1
            log_text.insert(tk.END, f"成功: {filename} -> {new_name}\n")
        except Exception as e:
            log_text.insert(tk.END, f"失败: {filename} (错误: {e})\n")

    log_text.insert(tk.END, f"\n--- 完成！共重命名 {success_count} 个文件 ---")
    messagebox.showinfo("完成", f"重命名完成！\n成功处理 {success_count} 个文件。")

# ================= 界面设计 =================

# 创建主窗口
root = tk.Tk()
root.title("批量文件重命名工具")
root.geometry("500x450")
root.resizable(False, False)

# 变量绑定
folder_var = tk.StringVar()
prefix_var = tk.StringVar(value="文件_")
start_num_var = tk.StringVar(value="1")
ext_var = tk.StringVar(value="")

# 1. 文件夹选择
tk.Label(root, text="文件夹路径:").place(x=20, y=20)
tk.Entry(root, textvariable=folder_var, width=40).place(x=100, y=20)
tk.Button(root, text="浏览...", command=browse_folder).place(x=400, y=15)

# 2. 前缀设置
tk.Label(root, text="文件前缀:").place(x=20, y=60)
tk.Entry(root, textvariable=prefix_var, width=15).place(x=100, y=60)

# 3. 起始数字设置
tk.Label(root, text="起始数字:").place(x=250, y=60)
tk.Entry(root, textvariable=start_num_var, width=10).place(x=320, y=60)

# 4. 后缀名设置
tk.Label(root, text="新后缀名:").place(x=20, y=100)
tk.Entry(root, textvariable=ext_var, width=15).place(x=100, y=100)
tk.Label(root, text="(例如 .jpg，留空则保持原后缀)", fg="gray").place(x=220, y=100)

# 5. 执行按钮
tk.Button(root, text="开始批量重命名", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=start_renaming).place(x=180, y=140)

# 6. 日志输出框
tk.Label(root, text="执行日志:").place(x=20, y=180)
log_text = tk.Text(root, width=65, height=15)
log_text.place(x=20, y=200)

# 运行主循环
root.mainloop()