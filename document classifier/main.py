#!/usr/bin/env python3
"""
ENHANCED DOCUMENT ANALYSIS SYSTEM
Automatically reads 3-5 .txt files from 'documents' folder,
summarizes, compares, detects discrepancies, and scores alignment.
"""

import os
import re

# ---------- AGENTS ----------

class SummarizerAgent:
    def summarize(self, text):
        """Simple summary: first 40 words"""
        words = text.split()
        return " ".join(words[:40]) + ("..." if len(words) > 40 else "")

class ComparatorAgent:
    def compare(self, documents):
        """Compute simple similarity between documents"""
        if not documents: return {"overall_similarity": 0}
        first = set(documents[0].split())
        sims = []
        for doc in documents[1:]:
            words = set(doc.split())
            overlap = len(first & words)
            total = len(first | words)
            sims.append((overlap / total * 100) if total > 0 else 0)
        overall = sum(sims)/len(sims) if sims else 100
        return {"overall_similarity": overall}

class DiscrepancyDetectorAgent:
    def detect(self, documents):
        """Detect contradictory refund policies"""
        issues = []
        refund_days = []
        for i, doc in enumerate(documents):
            match = re.search(r'(\d+)[- ]day refund', doc, re.IGNORECASE)
            if match: refund_days.append((i+1, int(match.group(1))))
        if len(refund_days) > 1 and len(set(day for _, day in refund_days)) > 1:
            issues.append({
                "message": f"Conflicting refund policies: {refund_days}",
                "severity": "high"
            })
        return issues

class ScoringAgent:
    def calculate(self, discrepancies, similarity):
        """Score alignment between 0-100"""
        score = similarity - 30 if discrepancies else similarity
        return max(0, min(100, int(score)))

    def get_interpretation(self, score):
        if score >= 80: return "Excellent alignment"
        elif score >= 60: return "Moderate alignment"
        else: return "Poor alignment"

# ---------- DISPLAY ----------

def show_documents(docs):
    print("\n📄 Documents Loaded:")
    for i, d in enumerate(docs,1): print(f"{i}. {d}\n")

def show_summaries(summaries):
    print("\n📝 Document Summaries:")
    for i, s in enumerate(summaries,1): print(f"{i}. {s}\n")

def show_comparison(result):
    print(f"\n📈 Overall Similarity: {result['overall_similarity']:.1f}%")

def show_discrepancies(discrepancies):
    print("\n🔍 Discrepancies Found:")
    if discrepancies:
        for d in discrepancies: print(f"- {d['message']} ({d['severity'].upper()})")
    else:
        print("None")

def show_score(score, interpretation):
    print(f"\n🧮 Alignment Score: {score}/100")
    print(f"Status: {interpretation}")

def show_summary_table(docs, summaries, comparison, discrepancies, score, interpretation):
    print("\n" + "="*50)
    print("FINAL ANALYSIS SUMMARY")
    print("="*50)
    print(f"Documents Analyzed: {len(docs)}")
    for i, s in enumerate(summaries,1):
        print(f"{i}. Summary: {s}")
    print(f"\nOverall Similarity: {comparison['overall_similarity']:.1f}%")
    print(f"Discrepancies Detected: {len(discrepancies)}")
    for d in discrepancies:
        print(f"- {d['message']} ({d['severity'].upper()})")
    print(f"Alignment Score: {score}/100")
    print(f"Status: {interpretation}")
    print("="*50)

# ---------- MAIN PROGRAM ----------

def main():
    folder = "documents"

    # Create folder if missing
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 '{folder}' folder created. Add 3-5 .txt files and rerun.")
        return

    # Load documents
    docs = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".txt"):
            with open(os.path.join(folder,f), "r", encoding="utf-8") as file:
                docs.append(file.read().strip())

    if len(docs) < 3:
        print(f"⚠️ Only {len(docs)} document(s) found. Please add at least 3 .txt files.")
        return
    elif len(docs) > 5:
        print(f"⚠️ {len(docs)} documents found. Only analyzing first 5 documents.")
        docs = docs[:5]

    # Initialize agents
    summarizer = SummarizerAgent()
    comparator = ComparatorAgent()
    detector = DiscrepancyDetectorAgent()
    scorer = ScoringAgent()

    # Analysis
    show_documents(docs)
    summaries = [summarizer.summarize(d) for d in docs]
    show_summaries(summaries)

    comparison = comparator.compare(docs)
    show_comparison(comparison)

    discrepancies = detector.detect(docs)
    show_discrepancies(discrepancies)

    score = scorer.calculate(discrepancies, comparison['overall_similarity'])
    interpretation = scorer.get_interpretation(score)
    show_score(score, interpretation)

    show_summary_table(docs, summaries, comparison, discrepancies, score, interpretation)

    # Save results
    try:
        with open("analysis_results.txt","w", encoding="utf-8") as f:
            f.write("DOCUMENT ANALYSIS RESULTS\n")
            f.write("="*50+"\n\n")
            f.write(f"Documents Analyzed: {len(docs)}\n\n")
            for i,s in enumerate(summaries,1): f.write(f"{i}. Summary: {s}\n")
            f.write(f"\nOverall Similarity: {comparison['overall_similarity']:.1f}%\n")
            f.write("\nDiscrepancies Detected:\n")
            if discrepancies:
                for d in discrepancies: f.write(f"- {d['message']} ({d['severity'].upper()})\n")
            else:
                f.write("None\n")
            f.write(f"\nAlignment Score: {score}/100\n")
            f.write(f"Status: {interpretation}\n")
        print("💾 Results saved to 'analysis_results.txt'")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")

if __name__ == "__main__":
    main()
