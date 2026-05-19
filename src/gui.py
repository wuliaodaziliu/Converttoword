import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path

from .converter import convert_multiple
from .logger import setup_logger, get_logger


class ConverterGUI:
    def __init__(self):
        self.logger = setup_logger()
        self.pdf_files = []
        self.output_dir = os.path.expanduser("~/Desktop")

        self.root = tk.Tk()
        self.root.title("PDF转Word工具")
        self.root.resizable(False, False)

        self.root.geometry("666x666")
        self._center_window()

        self._setup_ui()
        self.logger.info("程序启动")

    def _center_window(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 666) // 2
        y = (sh - 666) // 2
        self.root.geometry(f"666x666+{x}+{y}")

    def _setup_ui(self):
        # 标题
        title = tk.Label(self.root, text="PDF 转 Word", font=("Arial", 18, "bold"),
                         bg="#2c3e50", fg="white", height=2)
        title.pack(fill="x")

        main = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # PDF文件选择
        frm = tk.Frame(main, bg="#f5f5f5")
        frm.pack(fill="x", pady=(0, 10))
        tk.Label(frm, text="PDF 文件（支持多选）", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w")
        frm2 = tk.Frame(frm)
        frm2.pack(fill="x", pady=(5, 0))
        self.file_list_var = tk.StringVar(value="未选择任何文件")
        tk.Label(frm2, textvariable=self.file_list_var, font=("Arial", 9), bg="white",
                 relief="solid", bd=1, anchor="w", padx=10, pady=8).pack(side="left", fill="x", expand=True)
        tk.Button(frm2, text="浏览", command=self._select_files, width=8).pack(side="right", padx=(5, 0))

        # 输出目录
        frm3 = tk.Frame(main, bg="#f5f5f5")
        frm3.pack(fill="x", pady=(0, 10))
        tk.Label(frm3, text="输出目录", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w")
        frm4 = tk.Frame(frm3)
        frm4.pack(fill="x", pady=(5, 0))
        self.output_var = tk.StringVar(value=self.output_dir)
        tk.Entry(frm4, textvariable=self.output_var, font=("Arial", 10), bg="white",
                 relief="solid", bd=1).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(frm4, text="浏览", command=self._select_output_dir, width=8).pack(side="right")

        # 配置区域
        cfg = tk.Frame(main, bg="#f5f5f5")
        cfg.pack(fill="x", pady=(0, 15))

        tk.Label(cfg, text="DPI（截图清晰度）", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, sticky="w")
        self.dpi_var = tk.StringVar(value="Doc")
        dpi_combo = ttk.Combobox(cfg, textvariable=self.dpi_var, values=["Shot", "Doc", "Pic"], width=12, state="readonly")
        dpi_combo.grid(row=1, column=0, padx=(0, 15))

        # 转换按钮
        btn_frame = tk.Frame(main, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=(0, 10))
        self.convert_btn = tk.Button(btn_frame, text="开始转换", font=("Arial", 12, "bold"),
                                    bg="#27ae60", fg="black", cursor="hand2", command=self._start_convert, height=2)
        self.convert_btn.pack(fill="x")

        # 进度条
        self.progress = ttk.Progressbar(main, mode="determinate", length=100)
        self.progress.pack(fill="x", pady=(0, 5))
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(main, textvariable=self.status_var, font=("Arial", 9), bg="#f5f5f5", fg="#666").pack(anchor="w")

        # 日志区域
        log_frame = tk.Frame(main, bg="#f5f5f5")
        log_frame.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(log_frame, text="日志", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, font=("Arial", 8), height=8,
                                                   state="disabled", bg="#fff")
        self.log_text.pack(fill="both", expand=True, pady=(5, 0))

    def _select_files(self):
        files = filedialog.askopenfilenames(title="选择PDF文件", filetypes=[("PDF文件", "*.pdf")])
        if files:
            self.pdf_files = list(files)
            self.file_list_var.set(f"已选择 {len(files)} 个文件")
            self.logger.info(f"选择文件: {files}")

    def _select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir = dir_path
            self.output_var.set(dir_path)

    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _start_convert(self):
        if not self.pdf_files:
            messagebox.showwarning("提示", "请先选择PDF文件")
            return

        output_dir = self.output_var.get().strip()
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("错误", "请选择有效的输出目录")
            return

        self.convert_btn.config(state="disabled", bg="#95a5a6", fg="gray", text="转换中...")
        self.progress["value"] = 0
        self.status_var.set("转换中...")
        self._log("开始转换...")

        dpi = self.dpi_var.get()

        self.logger.info(f"配置 DPI={dpi}")

        def progress_callback(page, total, overall):
            self.root.after(0, lambda: self._update_progress(page, total, overall))

        self.root.after(100, lambda: self._run_convert(dpi, progress_callback))

    def _run_convert(self, dpi, callback):
        def thread_target():
            try:
                results = convert_multiple(
                    self.pdf_files,
                    self.output_dir,
                    dpi=dpi,
                    progress_callback=callback
                )
                self.root.after(0, lambda: self._on_complete(results))
            except Exception as e:
                self.logger.error(str(e))
                self.root.after(0, lambda: self._on_error(str(e)))

        threading.Thread(target=thread_target, daemon=True).start()

    def _update_progress(self, page, total, overall):
        self.progress["value"] = overall * 100
        self.status_var.set(f"处理中... {int(overall * 100)}%")

    def _on_complete(self, results):
        self.progress["value"] = 100
        success = sum(1 for _, ok, _ in results if ok)
        failed = len(results) - success
        self._log(f"完成：成功 {success} 个，失败 {failed} 个")
        self.logger.info(f"转换完成: 成功{success} 失败{failed}")

        for pdf, ok, msg in results:
            if ok:
                self._log(f"✓ {Path(pdf).name}: {msg}")
            else:
                self._log(f"✗ {Path(pdf).name}: {msg}")
                self.logger.error(f"{pdf}: {msg}")

        self.convert_btn.config(state="normal", bg="#27ae60", text="开始转换")
        self.status_var.set("完成")
        messagebox.showinfo("完成", f"转换完成\n成功: {success} 失败: {failed}")

    def _on_error(self, err_msg):
        self._log(f"错误: {err_msg}")
        self.logger.error(err_msg)
        self.convert_btn.config(state="normal", bg="#27ae60", text="开始转换")
        self.status_var.set("转换失败")
        self.progress["value"] = 0
        messagebox.showerror("错误", err_msg)

    def run(self):
        self.root.mainloop()


def main():
    app = ConverterGUI()
    app.run()


if __name__ == "__main__":
    main()