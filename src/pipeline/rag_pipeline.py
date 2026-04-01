import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from groq import Groq
from src.retrieval.retriever import SchemeRetriever
from config import GROQ_API_KEY, GROQ_MODEL

class RAGPipeline:
    def __init__(self):
        print("🚀 Initializing RAG Pipeline...")
        self.retriever = SchemeRetriever()
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
        print("✅ RAG Pipeline ready!\n")

    def build_prompt(self, query, chunks):
        """Build prompt with retrieved context."""

        context = ""
        for i, chunk in enumerate(chunks):
            context += f"\n--- Scheme {i+1}: {chunk['scheme_name']} ---\n"
            context += chunk["text"]
            context += "\n"

        prompt = f"""You are a helpful assistant that answers questions about Indian Government schemes, scholarships, and welfare programs.

Use ONLY the context provided below to answer the question. If the answer is not found in the context, say "I don't have enough information about this in my knowledge base."

Always mention:
- The scheme name
- Eligibility criteria (if asked or relevant)
- Key benefits
- Documents required (if asked)

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

        return prompt

    def ask(self, query):
        """Main method — retrieve relevant chunks and generate answer."""

        print(f"🔍 Searching for: {query}")

        # Step 1: Retrieve relevant chunks
        chunks = self.retriever.retrieve(query, n_results=5)
        print(f"📦 Retrieved {len(chunks)} relevant chunks")

        # Step 2: Build prompt
        prompt = self.build_prompt(query, chunks)

        # Step 3: Call Groq LLM
        print("🤖 Generating answer with Groq...")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert on Indian Government schemes and welfare programs. Answer clearly and helpfully in simple language."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )

        answer = response.choices[0].message.content
        sources = list(set([c["scheme_name"] for c in chunks]))

        return {
            "question": query,
            "answer": answer,
            "sources": sources
        }


if __name__ == "__main__":
    rag = RAGPipeline()

    # Test queries
    test_queries = [
        "What schemes are available for farmers?",
        "What scholarships are available for SC ST students?",
        "What documents are required for PM-KISAN?"
    ]

    for query in test_queries:
        result = rag.ask(query)
        print(f"\n{'='*60}")
        print(f"❓ Question: {result['question']}")
        print(f"\n💬 Answer:\n{result['answer']}")
        print(f"\n📚 Sources: {', '.join(result['sources'])}")
        print('='*60)