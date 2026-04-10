# ChromaDB Tutorial - Hiểu Từ Đầu

## 🤔 ChromaDB Là Gì?

ChromaDB là một **vector database** (cơ sở dữ liệu vector) - nơi lưu trữ và tìm kiếm các vector embeddings.

### Tương Tự Đơn Giản:

Hãy tưởng tượng:
- **Database thông thường (SQL):** Lưu text, số, ngày tháng → Tìm kiếm chính xác (WHERE name = "John")
- **Vector Database (ChromaDB):** Lưu vectors (danh sách số) → Tìm kiếm tương tự (tìm câu giống nghĩa)

**Ví dụ:**
```
Text: "VinUni offers scholarships"
↓ (embedding)
Vector: [0.23, -0.45, 0.67, 0.12, ...] (384 số)
```

ChromaDB lưu các vectors này và giúp tìm vectors "gần nhau" (nghĩa tương tự).

---

## 📚 Các Khái Niệm Cơ Bản

### 1. Client (Máy Khách)

Client là "cổng vào" để làm việc với ChromaDB. Có 2 loại:

```python
import chromadb

# Loại 1: In-Memory Client (lưu trong RAM)
client = chromadb.Client()
# ✓ Nhanh
# ✗ Mất data khi tắt chương trình

# Loại 2: Persistent Client (lưu vào ổ cứng)
client = chromadb.PersistentClient(path="./my_database")
# ✓ Giữ data khi tắt chương trình
# ✗ Chậm hơn một chút (phải đọc/ghi file)
```

**Tương tự:** Client giống như "cửa hàng" - bạn phải vào cửa hàng mới mua được đồ.

### 2. Collection (Bộ Sưu Tập)

Collection là "ngăn kệ" trong cửa hàng - nơi lưu các documents.

```python
# Tạo hoặc lấy collection
collection = client.get_or_create_collection(name="my_documents")
# Giống như: "Cho tôi ngăn kệ tên 'my_documents', nếu chưa có thì tạo mới"
```

**Tương tự:** 
- Client = Cửa hàng
- Collection = Ngăn kệ trong cửa hàng
- Documents = Sản phẩm trên ngăn kệ

### 3. Document (Tài Liệu)

Mỗi document có 3 phần:

```python
collection.add(
    ids=["doc1"],                    # ID duy nhất (như mã sản phẩm)
    documents=["VinUni is great"],   # Nội dung text
    embeddings=[[0.1, 0.2, 0.3]],   # Vector (tự động tính hoặc tự cung cấp)
    metadatas=[{"type": "review"}]   # Thông tin thêm (tùy chọn)
)
```

---

## 🔍 Cách ChromaDB Hoạt Động

### Bước 1: Thêm Documents

```python
import chromadb

# 1. Mở cửa hàng
client = chromadb.Client()

# 2. Lấy ngăn kệ
collection = client.get_or_create_collection("vinuni_docs")

# 3. Thêm sản phẩm (documents)
collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "VinUni offers scholarships to students.",
        "The tuition fee is 530 million VND.",
        "IELTS 6.5 is required for admission."
    ]
)

print(f"Đã thêm {collection.count()} documents")
# Output: Đã thêm 3 documents
```

**Điều gì xảy ra bên trong?**
1. ChromaDB tự động chuyển text → vector (embedding)
2. Lưu vector vào collection
3. Giờ có thể tìm kiếm!

### Bước 2: Tìm Kiếm (Query)

```python
# Tìm documents giống với câu hỏi
results = collection.query(
    query_texts=["How much is the tuition?"],  # Câu hỏi
    n_results=2                                 # Lấy 2 kết quả gần nhất
)

print("Kết quả tìm kiếm:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")

# Output:
# 1. The tuition fee is 530 million VND.
# 2. VinUni offers scholarships to students.
```

**Điều gì xảy ra bên trong?**
1. ChromaDB chuyển câu hỏi → vector
2. So sánh vector câu hỏi với tất cả vectors trong collection
3. Trả về documents có vectors "gần nhất" (nghĩa tương tự)

---

## 🎯 Ví Dụ Thực Tế: Từng Bước

### Ví Dụ 1: In-Memory (Đơn Giản Nhất)

```python
import chromadb

# Bước 1: Tạo client (in-memory)
print("Bước 1: Tạo client...")
client = chromadb.Client()
print("✓ Client đã sẵn sàng (in-memory mode)")

# Bước 2: Tạo collection
print("\nBước 2: Tạo collection...")
collection = client.get_or_create_collection("test")
print(f"✓ Collection 'test' đã sẵn sàng")

# Bước 3: Thêm documents
print("\nBước 3: Thêm documents...")
collection.add(
    ids=["1", "2", "3"],
    documents=[
        "Tôi thích học Python",
        "Python là ngôn ngữ lập trình",
        "Hôm nay trời đẹp"
    ]
)
print(f"✓ Đã thêm {collection.count()} documents")

# Bước 4: Tìm kiếm
print("\nBước 4: Tìm kiếm...")
results = collection.query(
    query_texts=["Ngôn ngữ lập trình là gì?"],
    n_results=2
)
print("Kết quả:")
for i, doc in enumerate(results['documents'][0], 1):
    print(f"  {i}. {doc}")

# Output:
# Kết quả:
#   1. Python là ngôn ngữ lập trình
#   2. Tôi thích học Python
```

**Giải thích:**
- Document 1 và 2 về Python → gần với câu hỏi về "ngôn ngữ lập trình"
- Document 3 về thời tiết → xa với câu hỏi → không xuất hiện

### Ví Dụ 2: Persistent (Lưu Vào Ổ Cứng)

```python
import chromadb

# Lần chạy đầu tiên
print("=== LẦN CHẠY ĐẦU TIÊN ===")
client = chromadb.PersistentClient(path="./my_db")
collection = client.get_or_create_collection("my_docs")

collection.add(
    ids=["1"],
    documents=["VinUni is in Hanoi"]
)
print(f"Đã lưu {collection.count()} documents vào ổ cứng")
print("Thư mục './my_db' đã được tạo")

# Giả sử tắt chương trình và chạy lại...
print("\n=== CHẠY LẠI SAU KHI TẮT ===")
client2 = chromadb.PersistentClient(path="./my_db")
collection2 = client2.get_or_create_collection("my_docs")

print(f"Vẫn còn {collection2.count()} documents!")
# Output: Vẫn còn 1 documents!

results = collection2.query(
    query_texts=["Where is VinUni?"],
    n_results=1
)
print(f"Kết quả: {results['documents'][0][0]}")
# Output: Kết quả: VinUni is in Hanoi
```

**Điểm khác biệt:**
- In-memory: Tắt chương trình → mất data
- Persistent: Tắt chương trình → data vẫn còn trong `./my_db`

---

## 🔧 Trong Code Của Chúng Ta

### Trước Khi Thêm Persistence

```python
class EmbeddingStore:
    def __init__(self, collection_name: str = "documents"):
        # Chỉ có in-memory
        client = chromadb.Client()
        self._collection = client.get_or_create_collection(name=collection_name)
```

**Vấn đề:** Mỗi lần chạy lại phải index lại tất cả documents → chậm!

### Sau Khi Thêm Persistence

```python
class EmbeddingStore:
    def __init__(
        self, 
        collection_name: str = "documents",
        persist_directory: str | None = None  # ← Thêm parameter này
    ):
        # Nếu có persist_directory → dùng PersistentClient
        if persist_directory:
            client = chromadb.PersistentClient(path=persist_directory)
        else:
            client = chromadb.Client()  # Mặc định vẫn là in-memory
        
        self._collection = client.get_or_create_collection(name=collection_name)
```

**Lợi ích:**
- Backward compatible: Code cũ vẫn chạy (in-memory)
- Có thể chọn persistent khi cần

---

## 📊 So Sánh Trực Quan

### In-Memory Mode

```
Lần 1:
┌─────────────┐
│   Client    │ (RAM)
│  ┌────────┐ │
│  │ doc1   │ │
│  │ doc2   │ │
│  └────────┘ │
└─────────────┘

Tắt chương trình...

Lần 2:
┌─────────────┐
│   Client    │ (RAM)
│  ┌────────┐ │
│  │ EMPTY! │ │ ← Mất hết!
│  └────────┘ │
└─────────────┘
```

### Persistent Mode

```
Lần 1:
┌─────────────┐      ┌──────────────┐
│   Client    │ ───→ │  ./my_db/    │ (Ổ cứng)
│  ┌────────┐ │      │  ┌────────┐  │
│  │ doc1   │ │      │  │ doc1   │  │
│  │ doc2   │ │      │  │ doc2   │  │
│  └────────┘ │      │  └────────┘  │
└─────────────┘      └──────────────┘

Tắt chương trình...

Lần 2:
┌─────────────┐      ┌──────────────┐
│   Client    │ ←─── │  ./my_db/    │ (Đọc từ ổ cứng)
│  ┌────────┐ │      │  ┌────────┐  │
│  │ doc1   │ │      │  │ doc1   │  │
│  │ doc2   │ │      │  │ doc2   │  │
│  └────────┘ │      │  └────────┘  │
└─────────────┘      └──────────────┘
                     ↑ Vẫn còn!
```

---

## 🎓 Tóm Tắt Đơn Giản

### ChromaDB Là Gì?
- Nơi lưu trữ vectors (embeddings)
- Giúp tìm kiếm "nghĩa tương tự" thay vì "chính xác"

### Các Thành Phần:
1. **Client:** Cổng vào (in-memory hoặc persistent)
2. **Collection:** Ngăn kệ chứa documents
3. **Document:** Text + Vector + Metadata

### Workflow:
```
Text → Embedding → ChromaDB → Query → Similar Documents
```

### In-Memory vs Persistent:
- **In-Memory:** Nhanh, mất data khi tắt, tốt cho testing
- **Persistent:** Chậm hơn chút, giữ data, tốt cho production

### Code Của Chúng Ta:
```python
# Testing (in-memory)
store = EmbeddingStore(collection_name="test")

# Production (persistent)
store = EmbeddingStore(
    collection_name="vinuni",
    persist_directory="./chroma_db"
)
```

---

## 🧪 Thử Nghiệm Ngay

Chạy file này để hiểu rõ hơn:

```bash
# Ví dụ đơn giản
python -c "
import chromadb
client = chromadb.Client()
collection = client.get_or_create_collection('test')
collection.add(ids=['1'], documents=['Hello World'])
print(f'Đã lưu {collection.count()} documents')
results = collection.query(query_texts=['Hi'], n_results=1)
print(f'Kết quả: {results[\"documents\"][0][0]}')
"

# Demo persistence
python demo_persistence_comparison.py

# Test đầy đủ
python test_chromadb_persistence.py
```

---

## ❓ Câu Hỏi Thường Gặp

**Q: Tại sao cần ChromaDB? Dùng list không được sao?**
A: List chỉ lưu được vài trăm documents. ChromaDB tối ưu cho hàng triệu documents, tìm kiếm nhanh hơn nhiều.

**Q: Embedding được tính ở đâu?**
A: Trong code của chúng ta, embedding được tính bởi `_mock_embed` hoặc `sentence-transformers`, rồi truyền vào ChromaDB.

**Q: Persistent mode lưu ở đâu?**
A: Trong thư mục bạn chỉ định (ví dụ: `./chroma_db`). Có thể xóa thư mục này để reset database.

**Q: Có thể dùng ChromaDB cho production không?**
A: Có! Với persistent mode, ChromaDB phù hợp cho production. Nhiều công ty đang dùng.

---

## 📚 Tài Liệu Tham Khảo

- ChromaDB Docs: https://docs.trychroma.com/
- Getting Started: https://docs.trychroma.com/getting-started
- Persistence: https://docs.trychroma.com/usage-guide#persistence

---

**Hy vọng giờ bạn đã hiểu ChromaDB rõ hơn! 🎉**

Nếu còn thắc mắc, hãy chạy các demo scripts và xem kết quả từng bước.
