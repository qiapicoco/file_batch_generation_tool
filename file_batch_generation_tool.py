import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser


def browse_file(entry, path_label):
    """
    打开文件选择对话框，选择文件并更新输入框和路径标签
    :param entry: 输入框对象
    :param path_label: 路径标签对象
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        # 清空输入框原有内容
        entry.delete(0, tk.END)
        # 插入所选文件的文件名
        entry.insert(0, os.path.basename(file_path))
        # 更新路径标签显示文件所在目录
        path_label.config(text=f"文件路径: {os.path.dirname(file_path)}")


def browse_dir(entry):
    """
    打开目录选择对话框，选择目录并更新输入框
    :param entry: 输入框对象
    """
    dir_path = filedialog.askdirectory()
    if dir_path:
        # 清空输入框原有内容
        entry.delete(0, tk.END)
        # 插入所选目录的路径
        entry.insert(0, dir_path)


def generate_files(original_entry, new_name_entry, ext_entry, num_entry, output_entry, path_label):
    """
    根据用户输入生成文件或文件夹
    :param original_entry: 原文件名输入框对象
    :param new_name_entry: 新文件名输入框对象
    :param ext_entry: 文件扩展名输入框对象
    :param num_entry: 新建文件数量输入框对象
    :param output_entry: 生成文件目录输入框对象
    :param path_label: 路径标签对象
    """
    # 获取原文件名
    original_name = original_entry.get()
    # 获取新文件名
    new_name = new_name_entry.get()
    # 获取文件扩展名
    ext = ext_entry.get()
    # 获取新建文件数量
    num_str = num_entry.get()
    # 获取生成文件目录
    output_dir = output_entry.get()

    # 检查必填项是否填写
    if not new_name or not num_str or not output_dir:
        messagebox.showerror("错误", "请填写所有必填项！")
        return

    try:
        # 将新建文件数量转换为整数
        num = int(num_str)
    except ValueError:
        # 若转换失败，弹出错误提示框
        messagebox.showerror("错误", "新建文件数量必须是整数！")
        return

    # 检查生成目录是否存在
    if not os.path.exists(output_dir):
        messagebox.showerror("错误", "指定的生成目录不存在！")
        return

    # 获取原文件所在目录
    original_path = path_label.cget("text").replace("文件路径: ", "")
    if original_name and original_path:
        # 拼接原文件的完整路径
        original_file = os.path.join(original_path, original_name)
        # 检查原文件是否存在
        if not os.path.exists(original_file):
            messagebox.showerror("错误", "原文件不存在！")
            return
        try:
            # 以二进制模式打开原文件并读取内容
            with open(original_file, 'rb') as src_file:
                content = src_file.read()
            for i in range(num):
                if ext:
                    # 拼接新文件的完整路径
                    new_file = os.path.join(output_dir, f"{new_name}_{i + 1}.{ext}")
                    # 以二进制模式打开新文件并写入原文件内容
                    with open(new_file, 'wb') as dst_file:
                        dst_file.write(content)
                else:
                    # 若未填写扩展名，创建新文件夹
                    new_dir = os.path.join(output_dir, f"{new_name}_{i + 1}")
                    os.makedirs(new_dir, exist_ok=True)
        except Exception as e:
            # 若复制文件时出错，弹出错误提示框
            messagebox.showerror("错误", f"复制文件时出错: {str(e)}")
    else:
        for i in range(num):
            if ext:
                # 拼接新文件的完整路径
                new_file = os.path.join(output_dir, f"{new_name}_{i + 1}.{ext}")
                # 创建新文件
                with open(new_file, 'w') as f:
                    pass
            else:
                # 若未填写扩展名，创建新文件夹
                new_dir = os.path.join(output_dir, f"{new_name}_{i + 1}")
                os.makedirs(new_dir, exist_ok=True)

    # 弹出成功提示框
    messagebox.showinfo("成功", "文件生成成功！")
    # 打开生成文件的目录
    webbrowser.open(output_dir)


def clear_all(original_entry, new_name_entry, ext_entry, num_entry, output_entry, path_label):
    """
    清空所有输入框和路径标签的内容
    :param original_entry: 原文件名输入框对象
    :param new_name_entry: 新文件名输入框对象
    :param ext_entry: 文件扩展名输入框对象
    :param num_entry: 新建文件数量输入框对象
    :param output_entry: 生成文件目录输入框对象
    :param path_label: 路径标签对象
    """
    original_entry.delete(0, tk.END)
    new_name_entry.delete(0, tk.END)
    ext_entry.delete(0, tk.END)
    num_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)
    path_label.config(text="")


# 创建主窗口
root = tk.Tk()
root.title("文件(夹)批量生成工具")

# 设置字体为微软雅黑
root.option_add('*Font', '微软雅黑 10')
root.option_add('*Label.padx', 10)
root.option_add('*Label.pady', 5)
root.option_add('*Entry.padx', 10)
root.option_add('*Entry.pady', 5)
root.option_add('*Button.padx', 10)
root.option_add('*Button.pady', 5)

# 分隔线
separator = tk.Frame(root, width=2, bd=1, relief=tk.SUNKEN)
separator.grid(row=0, column=2, rowspan=8, sticky='ns', padx=(20, 10))

# 原文件
label_original = tk.Label(root, text="原文件名:", anchor=tk.E)
label_original.grid(row=0, column=0, sticky=tk.E)
original_entry = tk.Entry(root, width=40)
original_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
button_browse_original = tk.Button(root, text="浏览", command=lambda: browse_file(original_entry, file_path_label))
button_browse_original.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.E + tk.N)
file_path_label = tk.Label(root, text="", fg="gray")
file_path_label.grid(row=1, column=1, columnspan=2, sticky=tk.W)
label_original_note = tk.Label(root, text="1. 非必填项。用于提取文件名，点击“浏览”选择原文件。", anchor=tk.W,
                               justify=tk.LEFT)
label_original_note.grid(row=0, column=4, padx=10, pady=5, rowspan=2, sticky=tk.W)

# 新文件名
label_new_name = tk.Label(root, text="⭐新文件名:", anchor=tk.E)
label_new_name.grid(row=2, column=0, sticky=tk.E)
new_name_entry = tk.Entry(root, width=40)
new_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
label_new_name_note = tk.Label(root, text="2. 必填项。输入新文件名称（不用填扩展名），如 `report`。", anchor=tk.W,
                               justify=tk.LEFT)
label_new_name_note.grid(row=2, column=4, padx=10, pady=5, sticky=tk.W)

# 文件扩展名
label_ext = tk.Label(root, text="文件扩展名:", anchor=tk.E)
label_ext.grid(row=3, column=0, sticky=tk.E)
ext_entry = tk.Entry(root, width=40)
ext_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
label_ext_note = tk.Label(root, text="3. 非必填项。自行填写，如 `txt`、`docx`；不填写则生成空文件夹。", anchor=tk.W,
                          justify=tk.LEFT)
label_ext_note.grid(row=3, column=4, padx=10, pady=5, sticky=tk.W)

# 新建文件数量
label_num = tk.Label(root, text="⭐新建文件数量:", anchor=tk.E)
label_num.grid(row=4, column=0, sticky=tk.E)
num_entry = tk.Entry(root, width=40)
num_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
label_num_note = tk.Label(root, text="4. 必填项。输入要生成的文件数量，如 `5`。", anchor=tk.W, justify=tk.LEFT)
label_num_note.grid(row=4, column=4, padx=10, pady=5, sticky=tk.W)

# 生成文件目录
label_output = tk.Label(root, text="⭐生成文件目录:", anchor=tk.E)
label_output.grid(row=5, column=0, sticky=tk.E)
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
button_browse_output = tk.Button(root, text="浏览", command=lambda: browse_dir(output_entry))
button_browse_output.grid(row=5, column=1, padx=(10, 0), pady=5, sticky=tk.E + tk.N)
label_output_note = tk.Label(root, text="5. 必填项。点击“浏览”选择存放新文件的目录。", anchor=tk.W, justify=tk.LEFT)
label_output_note.grid(row=5, column=4, padx=10, pady=5, sticky=tk.W)

# 生成按钮
button_generate = tk.Button(root, text="😁生成",
                            command=lambda: generate_files(original_entry, new_name_entry, ext_entry, num_entry,
                                                           output_entry, file_path_label))
button_generate.grid(row=6, column=1, padx=10, pady=20, sticky=tk.W)

# 清空全部按钮
button_clear = tk.Button(root, text="清空全部",
                         command=lambda: clear_all(original_entry, new_name_entry, ext_entry, num_entry,
                                                   output_entry, file_path_label))
button_clear.grid(row=6, column=1, padx=10, pady=20, sticky=tk.E)

# 注意事项说明
instructions = """注意事项：

    - 分为两种模式
    模式1--> 生成空文件模式（不选原文件）：
    当不填“原文件名” 且 填写了“文件扩展名”，生成空文件，比如空白的的记事本。

    模式2--> 复制原文件模式（选原文件）：
    当填了“原文件名” 且 填写了和原文件相同的“文件扩展名”，生成和原文件内容一模一样的文件。
    当然，您也可以填和原文件不同的“文件扩展名”，试试吧！🎈
"""
label_instructions = tk.Label(root, text=instructions, anchor=tk.W, justify=tk.LEFT)
label_instructions.grid(row=7, column=4, padx=10, pady=10, sticky=tk.W)

# 运行主循环
root.mainloop()
