"""
Interactive ChromaDB Demo - Học Từng Bước

Chạy script này và làm theo hướng dẫn để hiểu ChromaDB
"""
import chromadb
from pathlib import Path

def pause(message="Nhấn Enter để tiếp tục..."):
    """Dừng lại để người dùng đọc"""
    input(f"\n{message}")

def clear_screen():
    """Xóa màn hình (optional)"""
    print("\n" * 2)

print("=" * 80)
print("CHROMADB INTERACTIVE DEMO - HỌC TỪNG BƯỚC")
print("=" * 80)
print("\nChào mừng! Demo này sẽ giúp bạn hiểu ChromaDB từng bước.")
print("Mỗi bước sẽ giải thích và cho bạn thấy kết quả.")
pause()

# ============================================================================
# PHẦN 1: IN-MEMORY MODE
# ============================================================================
clear_screen()
print("=" * 80)
print("PHẦN 1: IN-MEMORY MODE (Lưu trong RAM)")
print("=" * 80)

print("\n📝 Giải thích:")
print("In-memory mode lưu data trong RAM (bộ nhớ tạm).")
print("Khi tắt chương trình, data sẽ mất.")
print("Tốt cho: Testing, thử nghiệm nhanh")
pause()

print("\n🔧 Bước 1: Tạo Client (in-memory)")
print("Code: client = chromadb.Client()")
client = chromadb.Client()
print("✓ Client đã được tạo (in-memory mode)")
pause()

print("\n🔧 Bước 2: Tạo Collection")
print("Code: collection = client.get_or_create_collection('demo')")
print("Collection giống như 'ngăn kệ' để chứa documents")
collection = client.get_or_create_collection("demo")
print(f"✓ Collection 'demo' đã được tạo")
print(f"  Số documents hiện tại: {collection.count()}")
pause()

print("\n🔧 Bước 3: Thêm Documents")
print("Code: collection.add(ids=[...], documents=[...])")
print("\nThêm 3 documents về VinUni:")
docs = [
    "VinUni offers scholarships to students.",
    "The tuition fee is 530 million VND per year.",
    "IELTS 6.5 is required for admission."
]
for i, doc in enumerate(docs, 1):
    print(f"  {i}. {doc}")

collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=docs
)
print(f"\n✓ Đã thêm {collection.count()} documents")
print("\n💡 Điều gì xảy ra bên trong?")
print("  - ChromaDB tự động chuyển text → vector (embedding)")
print("  - Lưu vector vào collection")
print("  - Giờ có thể tìm kiếm!")
pause()

print("\n🔧 Bước 4: Tìm Kiếm (Query)")
print("Code: collection.query(query_texts=['...'], n_results=2)")
query = "How much is the tuition?"
print(f"\nCâu hỏi: '{query}'")
print("Tìm 2 documents gần nhất...")

results = collection.query(
    query_texts=[query],
    n_results=2
)

print("\n✓ Kết quả:")
for i, doc in enumerate(results['documents'][0], 1):
    distance = results['distances'][0][i-1]
    print(f"  {i}. {doc}")
    print(f"     (Distance: {distance:.4f} - càng nhỏ càng giống)")

print("\n💡 Tại sao kết quả này?")
print("  - Document về tuition fee có nghĩa gần nhất với câu hỏi")
print("  - ChromaDB so sánh vectors để tìm documents tương tự")
pause()

print("\n🔧 Bước 5: Thử Query Khác")
query2 = "English requirements"
print(f"Câu hỏi: '{query2}'")
results2 = collection.query(query_texts=[query2], n_results=1)
print(f"\n✓ Kết quả: {results2['documents'][0][0]}")
print("\n💡 Document về IELTS được trả về vì liên quan đến English!")
pause()

print("\n⚠️  Vấn Đề Của In-Memory Mode:")
print("Nếu tắt chương trình và chạy lại, tất cả data sẽ MẤT!")
print("Phải thêm lại 3 documents từ đầu.")
print("\n→ Giải pháp: PERSISTENT MODE")
pause()

# ============================================================================
# PHẦN 2: PERSISTENT MODE
# ============================================================================
clear_screen()
print("=" * 80)
print("PHẦN 2: PERSISTENT MODE (Lưu vào ổ cứng)")
print("=" * 80)

print("\n📝 Giải thích:")
print("Persistent mode lưu data vào ổ cứng (hard disk).")
print("Khi tắt chương trình, data vẫn còn.")
print("Tốt cho: Production, ứng dụng thực tế")
pause()

persist_dir = "./demo_chromadb"
print(f"\n🔧 Bước 1: Tạo Persistent Client")
print(f"Code: client = chromadb.PersistentClient(path='{persist_dir}')")
client_persist = chromadb.PersistentClient(path=persist_dir)
print(f"✓ Persistent client đã được tạo")
print(f"  Data sẽ được lưu vào: {Path(persist_dir).absolute()}")
pause()

print("\n🔧 Bước 2: Tạo Collection")
collection_persist = client_persist.get_or_create_collection("vinuni_docs")
print(f"✓ Collection 'vinuni_docs' đã được tạo")
print(f"  Số documents hiện tại: {collection_persist.count()}")
pause()

print("\n🔧 Bước 3: Thêm Documents")
print("Thêm documents về VinUni admission...")
collection_persist.add(
    ids=["v1", "v2", "v3"],
    documents=[
        "VinUni is located in Hanoi, Vietnam.",
        "VinUni partners with Cornell University.",
        "VinUni offers 15 undergraduate majors."
    ],
    metadatas=[
        {"type": "location"},
        {"type": "partnership"},
        {"type": "programs"}
    ]
)
print(f"✓ Đã thêm {collection_persist.count()} documents")
print(f"✓ Data đã được lưu vào ổ cứng tại: {persist_dir}")
pause()

print("\n🔧 Bước 4: Tìm Kiếm")
query3 = "Where is VinUni?"
print(f"Câu hỏi: '{query3}'")
results3 = collection_persist.query(query_texts=[query3], n_results=1)
print(f"✓ Kết quả: {results3['documents'][0][0]}")
pause()

print("\n🔧 Bước 5: Giả Lập Restart (Tạo Client Mới)")
print("Giả sử chương trình bị tắt và chạy lại...")
print("Tạo client mới với cùng persist_directory...")
client_persist2 = chromadb.PersistentClient(path=persist_dir)
collection_persist2 = client_persist2.get_or_create_collection("vinuni_docs")
print(f"\n✓ Client mới đã được tạo")
print(f"  Số documents: {collection_persist2.count()}")
print("\n🎉 Data vẫn còn! Không bị mất!")
pause()

print("\n🔧 Bước 6: Verify Data Vẫn Còn")
print("Thử query lại với client mới...")
results4 = collection_persist2.query(query_texts=[query3], n_results=1)
print(f"✓ Kết quả: {results4['documents'][0][0]}")
print("\n✅ SUCCESS! Data đã được persist thành công!")
pause()

# ============================================================================
# PHẦN 3: METADATA FILTERING
# ============================================================================
clear_screen()
print("=" * 80)
print("PHẦN 3: METADATA FILTERING (Lọc Theo Metadata)")
print("=" * 80)

print("\n📝 Giải thích:")
print("Metadata là thông tin thêm về document (type, category, date, etc.)")
print("Có thể lọc documents theo metadata trước khi search.")
pause()

print("\n🔧 Ví Dụ: Lọc Theo Type")
print("Documents hiện có:")
all_results = collection_persist2.query(
    query_texts=["VinUni"],
    n_results=10
)
for i, (doc, meta) in enumerate(zip(all_results['documents'][0], all_results['metadatas'][0]), 1):
    print(f"  {i}. {doc}")
    print(f"     Metadata: {meta}")
pause()

print("\n🔧 Query Với Filter")
print("Chỉ tìm documents có type='partnership'")
filtered_results = collection_persist2.query(
    query_texts=["VinUni information"],
    n_results=10,
    where={"type": "partnership"}  # ← Filter này!
)
print(f"\n✓ Kết quả (chỉ partnership):")
for doc in filtered_results['documents'][0]:
    print(f"  - {doc}")
pause()

# ============================================================================
# PHẦN 4: SO SÁNH
# ============================================================================
clear_screen()
print("=" * 80)
print("PHẦN 4: SO SÁNH IN-MEMORY vs PERSISTENT")
print("=" * 80)

print("\n📊 In-Memory Mode:")
print("  ✓ Nhanh (không có disk I/O)")
print("  ✓ Đơn giản (không cần chỉ định path)")
print("  ✓ Tốt cho testing")
print("  ✗ Mất data khi restart")
print("  ✗ Không phù hợp production")

print("\n📊 Persistent Mode:")
print("  ✓ Data không bị mất")
print("  ✓ Không cần re-index")
print("  ✓ Phù hợp production")
print("  ✗ Chậm hơn chút (disk I/O)")
print("  ✗ Cần quản lý thư mục lưu trữ")

print("\n💡 Khi Nào Dùng Gì?")
print("  - Testing/Development: In-Memory")
print("  - Production/Real App: Persistent")
pause()

# ============================================================================
# KẾT THÚC
# ============================================================================
clear_screen()
print("=" * 80)
print("🎉 HOÀN THÀNH DEMO!")
print("=" * 80)

print("\n📚 Bạn Đã Học:")
print("  1. ChromaDB là gì và hoạt động như thế nào")
print("  2. In-memory mode (lưu trong RAM)")
print("  3. Persistent mode (lưu vào ổ cứng)")
print("  4. Cách thêm documents và query")
print("  5. Metadata filtering")
print("  6. Khi nào dùng mode nào")

print("\n🔧 Trong Code Của Chúng Ta:")
print("  # In-memory (default)")
print("  store = EmbeddingStore(collection_name='test')")
print("\n  # Persistent")
print("  store = EmbeddingStore(")
print("      collection_name='vinuni',")
print("      persist_directory='./chroma_db'")
print("  )")

print("\n📁 Files Để Tham Khảo:")
print("  - CHROMADB_TUTORIAL.md: Hướng dẫn chi tiết")
print("  - demo_persistence_comparison.py: So sánh 2 modes")
print("  - test_chromadb_persistence.py: Test đầy đủ")

print("\n🧹 Cleanup:")
print(f"  Xóa thư mục demo: rm -rf {persist_dir}")
print("  (Hoặc xóa thủ công)")

print("\n" + "=" * 80)
print("Cảm ơn bạn đã tham gia demo! 🚀")
print("=" * 80)
