import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from agents import SummarizerAgent, ComparatorAgent, DiscrepancyDetectorAgent, ScoringAgent

class DocumentAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Analysis System")
        self.root.geometry("900x650")
        self.root.configure(bg="#f4f6f8")

        self.documents = []

        # ---------- HEADER ----------
        header = tk.Label(
            root,
            text="📄 Document Analysis System",
            font=("Helvetica", 20, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)

        # ---------- BUTTON FRAME ----------
        btn_frame = tk.Frame(root, bg="#f4f6f8")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="📂 Select Documents (3–5)",
            command=self.load_files,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="▶ Analyze",
            command=self.analyze,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)

        # ---------- OUTPUT AREA ----------
        output_frame = tk.Frame(root, bg="#f4f6f8")
        output_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="white",
            fg="#2c3e50",
            insertbackground="black"
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        self.output.insert(tk.END, "👉 Please select 3–5 text documents to begin analysis.\n")

    # ---------- LOAD FILES ----------
    def load_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Text Files",
            filetypes=[("Text Files", "*.txt")]
        )

        if len(file_paths) < 3 or len(file_paths) > 5:
            messagebox.showerror("Selection Error", "Please select between 3 and 5 text files.")
            return

        self.documents = []
        for path in file_paths:
            with open(path, "r", encoding="utf-8") as f:
                self.documents.append(f.read())

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"✅ {len(self.documents)} documents loaded successfully.\n\n")

    # ---------- ANALYZE ----------
    def analyze(self):
        if not self.documents:
            messagebox.showwarning("No Documents", "Please load documents first.")
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

        self.output.insert(tk.END, "📝 DOCUMENT SUMMARIES\n", "title")
        self.output.insert(tk.END, "-" * 60 + "\n")
        for i, s in enumerate(summaries, 1):
            self.output.insert(tk.END, f"{i}. {s}\n\n")

        self.output.insert(tk.END, f"📈 OVERALL SIMILARITY: {comparison['overall_similarity']:.1f}%\n\n")

        self.output.insert(tk.END, "🔍 DISCREPANCIES\n")
        self.output.insert(tk.END, "-" * 60 + "\n")
        if discrepancies:
            for d in discrepancies:
                self.output.insert(tk.END, f"- {d['message']} ({d['severity'].upper()})\n")
        else:
            self.output.insert(tk.END, "None\n")

        self.output.insert(tk.END, "\n🧮 ALIGNMENT SCORE\n")
        self.output.insert(tk.END, "-" * 60 + "\n")
        self.output.insert(tk.END, f"Score: {score}/100\n")
        self.output.insert(tk.END, f"Status: {interpretation}\n")

        # Styling text tags
        self.output.tag_config("title", font=("Helvetica", 12, "bold"))

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentAnalysisGUI(root)
    root.mainloop()
