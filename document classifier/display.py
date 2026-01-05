# display.py
"""
Results display for Document Analysis System
"""

class ResultsDisplay:
    def show_documents(self, documents):
        print("\n📄 Documents:")
        for i, doc in enumerate(documents, 1):
            print(f"{i}. {doc}\n")

    def show_summaries(self, summaries):
        print("\n📝 Summaries:")
        for i, summary in enumerate(summaries, 1):
            print(f"{i}. {summary}\n")

    def show_comparison(self, comparison):
        print(f"\n📈 Overall Similarity: {comparison['overall_similarity']:.1f}%")

    def show_discrepancies(self, discrepancies):
        print("\n🔍 Discrepancies Found:")
        if discrepancies:
            for disc in discrepancies:
                print(f"- {disc['message']} ({disc['severity'].upper()})")
        else:
            print("None")

    def show_score(self, score, interpretation):
        print(f"\n🧮 Alignment Score: {score}/100")
        print(f"Status: {interpretation}")

    def show_summary_table(self, results):
        print("\n" + "="*40)
        print("FINAL RESULTS SUMMARY")
        print("="*40)
        print(f"Documents analyzed: {len(results['documents'])}")
        print(f"Alignment Score: {results['score']}/100")
        print(f"Discrepancies: {len(results['discrepancies'])}")
        print(f"Overall Similarity: {results['comparison']['overall_similarity']:.1f}%")
        print("="*40)
