#!/usr/bin/env python3
"""
build_faiss_index.py
--------------------
Build a FAISS index from chunks.jsonl produced by convert_to_rag_jsonl.py

Inputs:
  --chunks path/to/chunks.jsonl
  --out    directory to store index + sidecar files (default: index_artifacts)

Outputs in --out:
  - recipes_chunks.index     (FAISS index)
  - texts.jsonl              (line i = text for vector i)
  - metas.jsonl              (line i = metadata for vector i; includes chunk_id/doc_id/recipe_title/...)
  - manifest.json            (embed model, dim, count)

Usage:
  python build_faiss_index.py --chunks rag_jsonl/chunks.jsonl --out index_artifacts
"""
import os, json, argparse
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def read_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True, help="Path to chunks.jsonl")
    ap.add_argument("--out", default="index_artifacts", help="Output directory")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    texts, metas = [], []
    for rec in read_jsonl(args.chunks):
        texts.append(rec["text"])
        metas.append({
            "chunk_id": rec.get("chunk_id"),
            "doc_id": rec.get("doc_id"),
            "recipe_title": rec.get("recipe_title"),
            "chunk_index": rec.get("chunk_index"),
            "minutes": rec.get("metadata", {}).get("minutes"),
            "diets": rec.get("metadata", {}).get("diets"),
            "allergens": rec.get("metadata", {}).get("allergens"),
            "cuisine": rec.get("metadata", {}).get("cuisine"),
            "meals": rec.get("metadata", {}).get("meals"),
            "ingredients": rec.get("metadata", {}).get("ingredients"),
        })

    if not texts:
        raise SystemExit("No records found in chunks.jsonl")

    # Embed
    model = SentenceTransformer(EMBED_MODEL)
    vecs = model.encode(texts, batch_size=128, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True)
    dim = vecs.shape[1]

    # Build FAISS (cosine via inner product on normalized vectors)
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)

    # Persist index
    index_path = os.path.join(args.out, "recipes_chunks.index")
    faiss.write_index(index, index_path)

    # Sidecars
    texts_path = os.path.join(args.out, "texts.jsonl")
    metas_path = os.path.join(args.out, "metas.jsonl")
    with open(texts_path, "w", encoding="utf-8") as ft:
        for t in texts:
            ft.write(json.dumps({"text": t}, ensure_ascii=False) + "\n")
    with open(metas_path, "w", encoding="utf-8") as fm:
        for m in metas:
            fm.write(json.dumps(m, ensure_ascii=False) + "\n")

    # Manifest
    manifest = {
        "embed_model": EMBED_MODEL,
        "dim": int(dim),
        "count": int(len(texts)),
        "index_path": os.path.abspath(index_path),
        "texts_path": os.path.abspath(texts_path),
        "metas_path": os.path.abspath(metas_path),
    }
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("[ok] Built FAISS index")
    print(" -", index_path)
    print(" -", texts_path)
    print(" -", metas_path)

if __name__ == "__main__":
    main()
