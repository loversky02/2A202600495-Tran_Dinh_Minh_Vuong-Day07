"""
Bonus: Test ChromaDB persistence to disk

This demonstrates how to persist vector store data to disk,
so it survives application restarts.
"""
from pathlib import Path
from src.store import EmbeddingStore
from src.models import Document

# Define persist directory
PERSIST_DIR = "./chroma_db"

print("=" * 80)
print("CHROMADB PERSISTENCE TEST")
print("=" * 80)

# Step 1: Create store with persistence
print("\n1. Creating EmbeddingStore with persistence...")
print(f"   Persist directory: {PERSIST_DIR}")

store1 = EmbeddingStore(
    collection_name="vinuni_admission",
    persist_directory=PERSIST_DIR
)

# Step 2: Add some documents
print("\n2. Adding documents to store...")
docs = [
    Document(
        id="doc1",
        content="VinUni offers scholarships ranging from 50% to 100% of tuition fees.",
        metadata={"category": "financial", "type": "scholarship"}
    ),
    Document(
        id="doc2",
        content="The tuition fee is approximately 530 million VND per year for most programs.",
        metadata={"category": "financial", "type": "tuition"}
    ),
    Document(
        id="doc3",
        content="IELTS 6.5 or equivalent is required for admission to VinUni.",
        metadata={"category": "requirements", "type": "english"}
    ),
]

store1.add_documents(docs)
print(f"   Added {len(docs)} documents")
print(f"   Collection size: {store1.get_collection_size()}")

# Step 3: Search to verify
print("\n3. Testing search...")
query = "How much is the tuition fee?"
results = store1.search(query, top_k=2)
print(f"   Query: '{query}'")
print(f"   Top result: {results[0]['content'][:80]}...")

# Step 4: Simulate application restart by creating new store instance
print("\n4. Simulating application restart...")
print("   Creating new EmbeddingStore instance with same persist_directory...")

store2 = EmbeddingStore(
    collection_name="vinuni_admission",
    persist_directory=PERSIST_DIR
)

print(f"   Collection size after restart: {store2.get_collection_size()}")

# Step 5: Verify data persisted
print("\n5. Verifying data persistence...")
results2 = store2.search(query, top_k=2)
print(f"   Query: '{query}'")
print(f"   Top result: {results2[0]['content'][:80]}...")

if results[0]['content'] == results2[0]['content']:
    print("\n   ✅ SUCCESS: Data persisted correctly!")
else:
    print("\n   ❌ FAILED: Data not persisted")

# Step 6: Test metadata filtering
print("\n6. Testing metadata filtering with persisted data...")
filtered_results = store2.search_with_filter(
    query="VinUni information",
    top_k=3,
    metadata_filter={"category": "financial"}
)
print(f"   Filter: category='financial'")
print(f"   Results: {len(filtered_results)} documents")
for i, result in enumerate(filtered_results, 1):
    print(f"   [{i}] {result['content'][:60]}...")

print("\n" + "=" * 80)
print("PERSISTENCE BENEFITS:")
print("- Data survives application restarts")
print("- No need to re-index documents every time")
print("- Faster startup for large document collections")
print("- Suitable for production deployments")
print("\nPersist directory:", Path(PERSIST_DIR).absolute())
print("=" * 80)

# Cleanup instructions
print("\nTo clean up: delete the './chroma_db' directory")
print("Command: rm -rf ./chroma_db  (Linux/Mac)")
print("Command: rmdir /s /q .\\chroma_db  (Windows)")
