import chromadb

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "incidents"

_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}) # matches our normalized embeddings
    return _collection

def upsert_incident_embedding(incident_id:int, embedding: list[float]) -> None:
    collection = get_collection()
    collection.upsert(ids=[str(incident_id)], embeddings=[embedding])

def get_embedding(incident_id:int) -> list[float] | None:
    collection = get_collection()
    result = collection.get(ids=[str(incident_id)], include=["embeddings"])
    if not result["ids"]:
        return None
    return result["embeddings"][0]

def query_similar(embedding:list[float], top_k: int, exclude_id: int) -> list[tuple[int,float]]:
    collection = get_collection()
    results = collection.query(
        query_embeddings = [embedding],
        n_results = top_k + 1
    )
    ids = results["ids"][0]
    distances = results["distances"][0]

    similar = []
    for id_str , distance in zip(ids, distances):
        if int(id_str) == exclude_id:
            continue
        similarity = 1 - distance
        similar.append((int(id_str), similarity))
        return similar[:top_k]