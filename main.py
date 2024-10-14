import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from pdf_to_text import extract_text_from_entire_pdf  ## Custom file for PDF text extraction
from msword_to_text import extract_text_from_word  ## Custom file for Word text extraction
from transformers import pipeline
import os
import sys


class QAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF və Word sual-cavab proqramı")

        # Get the directory of the running script/executable to handle icon location change
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # Load the icon dynamically
        icon_path = os.path.join(application_path, 'qa_icon.ico')
        self.root.iconbitmap(icon_path)

        self.file_path = None
        self.file_text = None

        # File selection
        self.select_file_button = tk.Button(root, text="PDF və ya Word fayl seçin", command=self.select_file)
        self.select_file_button.pack(pady=5)

        self.file_label = tk.Label(root, text="Fayl seçilməyib")
        self.file_label.pack(pady=5)

        # Question entry
        self.question_label = tk.Label(root, text="Fayl tərkibi ilə bağlı sualınızı daxil edin:")
        self.question_label.pack(pady=5)

        self.question_entry = tk.Entry(root, width=80)
        self.question_entry.pack(pady=5)

        # Submit button
        self.submit_button = tk.Button(root, text="Sualı göndər", command=self.get_answer)
        self.submit_button.pack(pady=5)

        # Answer display
        self.answer_label = tk.Label(root, text="Cavab:")
        self.answer_label.pack(pady=5)

        self.answer_text = tk.Text(root, height=10, width=80)
        self.answer_text.pack(pady=5)

        # Load QA model from local dir
        model_path = os.path.join(application_path, 'qa_model')
        self.qa_model = pipeline("question-answering", model=model_path)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.doc;*.docx")])
        if self.file_path:
            self.file_label.config(text=f"Fayl: {self.file_path}")

            # Extract text based on file type
            try:
                if self.file_path.lower().endswith(".pdf"):
                    self.file_text = extract_text_from_entire_pdf(self.file_path)
                elif self.file_path.lower().endswith((".doc", ".docx")):
                    self.file_text = extract_text_from_word(self.file_path)
                else:
                    self.file_label.config(text="Dəstəklənməyən fayl formatı")
                    self.file_text = None
            except Exception as e:
                messagebox.showerror("Error", f"Faylın məzmununu çıxarmaq mümkün olmadı: {str(e)}")
                self.file_text = None
        else:
            self.file_label.config(text="Fayl seçilməyib")
            self.file_text = None

    def get_answer(self):
        if not self.file_text:
            messagebox.showerror("Error", "Zəhmət olmasa birinci fayl seçin.")
            return
        question = self.question_entry.get()
        if not question:
            messagebox.showerror("Error", "Zəhmət olmasa sualı daxil edin.")
            return
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert(tk.END, "İşlənir...")

        # Run the answer processing in a separate thread
        threading.Thread(target=self.process_answer, args=(question,)).start()

    def process_answer(self, question):
        context = self.file_text

        result = self.qa_model(question=question, context=context, max_answer_len=100)

        answer = result['answer']
        score = result['score']

        # Update the GUI in the main thread
        self.root.after(0, self.update_answer_text, answer, score)

    def update_answer_text(self, answer, score):
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert(tk.END, f"{answer} (Score: {score})")


# ensures that the GUI is triggered only if main.py executed directly
if __name__ == "__main__":
    root = tk.Tk()
    app = QAApp(root)
    root.mainloop()
