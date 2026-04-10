"""
Bonus: Compare in-memory vs persistent ChromaDB

This demonstrates the difference between:
1. In-memory mode (default) - data lost on restart
2. Persistent mode - data saved to disk
"""
from src.store import EmbeddingStore
from src.models import Document

print("=" * 80)
print("IN-MEMORY vs PERSISTENT CHROMADB COMPARISON")
print("=" * 80)

# Sample documents
docs = [
    Document("d1", "VinUni is located in Hanoi, Vietnam.", {"type": "location"}),
    Document("d2", "VinUni partners with Cornell University.", {"type": "partnership"}),
    Document("d3", "VinUni offers 15 undergraduate majors.", {"type": "programs"}),
]

# Test 1: In-memory mode (default)
print("\n" + "=" * 80)
print("TEST 1: IN-MEMORY MODE (Default)")
print("=" * 80)

print("\nCreating store without persist_directory...")
store_memory = EmbeddingStore(collection_name="test_memory")
store_memory.add_documents(docs)
print(f"Added {len(docs)} documents")
print(f"Collection size: {store_memory.get_collection_size()}")

print("\nSimulating restart (creating new instance)...")
store_memory2 = EmbeddingStore(collection_name="test_memory")
print(f"Collection size after restart: {store_memory2.get_collection_size()}")
print("❌ Data lost! In-memory mode doesn't persist.")

# Test 2: Persistent mode
print("\n" + "=" * 80)
print("TEST 2: PERSISTENT MODE")
print("=" * 80)

print("\nCreating store WITH persist_directory...")
store_persist = EmbeddingStore(
    collection_name="test_persist",
    persist_directory="./demo_chroma_db"
)
store_persist.add_documents(docs)
print(f"Added {len(docs)} documents")
print(f"Collection size: {store_persist.get_collection_size()}")

print("\nSimulating restart (creating new instance)...")
store_persist2 = EmbeddingStore(
    collection_name="test_persist",
    persist_directory="./demo_chroma_db"
)
print(f"Collection size after restart: {store_persist2.get_collection_size()}")
print("✅ Data persisted! Persistent mode saves to disk.")

# Test search on persisted data
print("\nTesting search on persisted data...")
results = store_persist2.search("Where is VinUni?", top_k=1)
print(f"Query: 'Where is VinUni?'")
print(f"Result: {results[0]['content']}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nIn-Memory Mode (default):")
print("  ✓ Faster (no disk I/O)")
print("  ✓ Good for testing")
print("  ✗ Data lost on restart")
print("  ✗ Not suitable for production")

print("\nPersistent Mode (persist_directory='./path'):")
print("  ✓ Data survives restarts")
print("  ✓ Suitable for production")
print("  ✓ No need to re-index")
print("  ✗ Slightly slower (disk I/O)")

print("\n" + "=" * 80)
print("USAGE:")
print("=" * 80)
print("\n# In-memory (default)")
print("store = EmbeddingStore(collection_name='my_docs')")
print("\n# Persistent")
print("store = EmbeddingStore(")
print("    collection_name='my_docs',")
print("    persist_directory='./chroma_db'")
print(")")

print("\n" + "=" * 80)
print("Cleanup: rm -rf ./demo_chroma_db")
print("=" * 80)
