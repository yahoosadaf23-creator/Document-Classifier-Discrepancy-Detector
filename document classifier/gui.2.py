import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from agents import SummarizerAgent, ComparatorAgent, DiscrepancyDetectorAgent, ScoringAgent

# ---------- LOGIN WINDOW ----------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Document Analysis System")
        self.root.geometry("450x350")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # Header
        tk.Label(
            root,
            text="🔐 Login",
            font=("Helvetica", 22, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=25)

        # Username
        tk.Label(root, text="Username", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 11)).pack(pady=(5,0))
        self.username = tk.Entry(root, width=30, font=("Arial", 12))
        self.username.pack(pady=5)

        # Password
        tk.Label(root, text="Password", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 11)).pack(pady=(10,0))
        self.password = tk.Entry(root, show="*", width=30, font=("Arial", 12))
        self.password.pack(pady=5)

        # Login Button with hover effect
        self.login_btn = tk.Button(
            root,
            text="Login",
            command=self.login,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=25,
            pady=8,
            relief=tk.FLAT,
            activebackground="#2ecc71",
            activeforeground="white"
        )
        self.login_btn.pack(pady=30)
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#2ecc71"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#27ae60"))

        # Footer
        tk.Label(
            root,
            text="© 2026 Document Analysis System",
            bg="#2c3e50",
            fg="#bdc3c7",
            font=("Arial", 9)
        ).pack(side=tk.BOTTOM, pady=10)

    def login(self):
        # Set correct credentials
        correct_username = "techsprint"
        correct_password = "12345"

        if self.username.get() == correct_username and self.password.get() == correct_password:
            self.root.destroy()
            open_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.username.delete(0, tk.END)
            self.password.delete(0, tk.END)

# ---------- MAIN APPLICATION ----------
class DocumentAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Analysis System")
        self.root.geometry("900x650")
        self.root.configure(bg="#f4f6f8")
        self.documents = []

        # Header
        tk.Label(
            root,
            text="📄 Document Analysis System",
            font=("Helvetica", 20, "bold"),
            bg="#34495e",
            fg="white",
            pady=15
        ).pack(fill=tk.X)

        # Buttons
        btn_frame = tk.Frame(root, bg="#f4f6f8")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="📂 Select Documents (3–5)",
            command=self.load_files,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="▶ Analyze",
            command=self.analyze,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)

        # Output area
        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="white",
            fg="#2c3e50"
        )
        self.output.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.output.insert(tk.END, "👉 Please select 3–5 text documents to begin analysis.\n")

    def load_files(self):
        files = filedialog.askopenfilenames(
            title="Select Text Files",
            filetypes=[("Text Files", "*.txt")]
        )
        if len(files) < 3 or len(files) > 5:
            messagebox.showerror("Error", "Please select 3 to 5 text files.")
            return

        self.documents = []
        for f in files:
            with open(f, "r", encoding="utf-8") as file:
                self.documents.append(file.read())

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"✅ {len(self.documents)} documents loaded successfully.\n\n")

    def analyze(self):
        if not self.documents:
            messagebox.showwarning("Warning", "Please load documents first.")
            return

        summarizer = SummarizerAgent()
        comparator = ComparatorAgent()
        detector = DiscrepancyDetectorAgent()
        scorer = ScoringAgent()

        summaries = [summarizer.summarize(d) for d in self.documents]
        comparison = comparator.compare(self.documents)
        discrepancies = detector.detect(self.documents)
        score = scorer.calculate(discrepancies, comparison["overall_similarity"])
        interpretation = scorer.get_interpretation(score)

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "📝 SUMMARIES\n" + "-"*60 + "\n")
        for i, s in enumerate(summaries, 1):
            self.output.insert(tk.END, f"{i}. {s}\n\n")

        self.output.insert(tk.END, f"📈 Overall Similarity: {comparison['overall_similarity']:.1f}%\n\n")
        self.output.insert(tk.END, "🔍 DISCREPANCIES\n" + "-"*60 + "\n")
        if discrepancies:
            for d in discrepancies:
                self.output.insert(tk.END, f"- {d['message']} ({d['severity'].upper()})\n")
        else:
            self.output.insert(tk.END, "None\n")

        self.output.insert(tk.END, "\n🧮 ALIGNMENT SCORE\n" + "-"*60 + "\n")
        self.output.insert(tk.END, f"Score: {score}/100\n")
        self.output.insert(tk.END, f"Status: {interpretation}\n")


# ---------- OPEN MAIN APP ----------
def open_main_app():
    root = tk.Tk()
    DocumentAnalysisGUI(root)
    root.mainloop()


# ---------- START ----------
if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
