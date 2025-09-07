import time
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from src.db.models import repo_files, code_embeddings

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def generate_embeddings_for_repo(repo_id: int, db: Session):
    start_time = time.time()

    files = db.query(repo_files).filter(repo_files.c.repository_id == repo_id).all()

    results = []
    for f in files:
        if not getattr(f, "content", None):
            continue

        chunks = chunk_text(f.content, chunk_size=500, overlap=50)

        for i, chunk in enumerate(chunks):
            vector = model.encode(chunk).tolist()

            insert_stmt = code_embeddings.insert().values(
                repo_id=repo_id,
                file_id=f.id,
                file_path=f.path,
                chunk_id=f"chunk-{i}",
                content=chunk,
                embedding=vector,
                metadata={
                    "content_length": len(chunk),
                    "total_chunks": len(chunks),
                    "chunk_index": i,
                },
                created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            try:
                db.execute(insert_stmt)
            except Exception as e:
                db.rollback()
                print(f"Skipping {f.path} chunk {i}: {e}")
                continue

            results.append({
                "file_id": f.id,
                "chunk_index": i,
                "content_length": len(chunk),
                "embedding_dim": len(vector),
            })

    db.commit()
    elapsed = round(time.time() - start_time, 2)

    return {
        "repo_id": repo_id,
        "file_count": len(files),
        "embedded_chunks": len(results),
        "time_taken_sec": elapsed,
        "details": results[:3],
    }
