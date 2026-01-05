# agents.py
"""
Agents for Document Analysis System
Includes Summarizer, Comparator, Discrepancy Detector, and Scoring Agent
"""

import re

class SummarizerAgent:
    """Summarizes a document"""
    def summarize(self, text):
        words = text.split()
        summary = " ".join(words[:30])
        if len(words) > 30:
            summary += "..."
        return summary

class ComparatorAgent:
    """Compares documents for similarity"""
    def compare(self, documents):
        if not documents:
            return {"overall_similarity": 0}
        
        first_words = set(documents[0].split())
        similarities = []
        
        for doc in documents[1:]:
            doc_words = set(doc.split())
            overlap = len(first_words & doc_words)
            total = len(first_words | doc_words)
            similarity = (overlap / total) * 100 if total > 0 else 0
            similarities.append(similarity)
        
        overall_similarity = sum(similarities) / len(similarities) if similarities else 100
        return {"overall_similarity": overall_similarity}

class DiscrepancyDetectorAgent:
    """Detects contradictions in documents"""
    def detect(self, documents):
        discrepancies = []
        refund_days = []
        for i, doc in enumerate(documents):
            match = re.search(r'(\d+)[- ]day refund', doc, re.IGNORECASE)
            if match:
                refund_days.append((i+1, int(match.group(1))))
        
        if len(refund_days) > 1:
            days_set = set(day for _, day in refund_days)
            if len(days_set) > 1:
                discrepancies.append({
                    "message": f"Conflicting refund policies found: {refund_days}",
                    "severity": "high"
                })
        return discrepancies

class ScoringAgent:
    """Calculates alignment score"""
    def calculate(self, discrepancies, similarity):
        score = similarity
        if discrepancies:
            score -= 30
        return max(0, min(100, int(score)))

    def get_interpretation(self, score):
        if score >= 80:
            return "Excellent alignment"
        elif score >= 60:
            return "Moderate alignment"
        else:
            return "Poor alignment"
