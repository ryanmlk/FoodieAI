#!/usr/bin/env python3
"""
convert_to_rag_jsonl.py
-----------------------
Read a recipes CSV and emit two JSONL files with a robust RAG schema:

Outputs (into --out dir):
- recipes.jsonl  : one JSON object per recipe (id, title, text, metadata{...})
- chunks.jsonl   : one JSON object per chunk (chunk_id, doc_id, recipe_title, chunk_index, text, metadata{...})

Usage:
  python convert_to_rag_jsonl.py --csv path/to/updated_combined_data_categories_embedded.csv --out rag_jsonl --chunk-tokens 400 --overlap 80
"""

import os, ast, json, uuid, argparse
from typing import Any, Dict, List, Optional
import pandas as pd

def as_list(value) -> List[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    s = str(value).strip()
    if not s:
        return []
    # Try to parse as Python list literal first:
    try:
        obj = ast.literal_eval(s)
        if isinstance(obj, list):
            return [str(x).strip() for x in obj if str(x).strip()]
    except Exception:
        pass
    # Fallback: comma-separated
    return [p.strip() for p in s.split(",") if p.strip()]

def to_float(value) -> Optional[float]:
    try:
        x = float(value)
        return x
    except Exception:
        return None

def normalize_row(row: Dict[str, Any], row_index: int) -> Dict[str, Any]:
    # id & title
    rid = row.get("id")
    rid = str(rid).strip() if rid is not None else ""
    if not rid:
        rid = str(uuid.uuid4())
    title = str(row.get("name", "")).strip() or "(Unnamed Recipe)"
    # numbers
    minutes = row.get("minutes")
    try:
        minutes = int(minutes) if minutes == minutes else None  # NaN check
    except Exception:
        minutes = None
    servings = row.get("servings")
    try:
        servings = int(servings) if servings == servings else None
    except Exception:
        servings = None
    serving_size = str(row.get("serving_size", "")).strip() or None

    # lists
    ingredients = as_list(row.get("ingredients_raw_str"))
    steps = as_list(row.get("steps"))
    tags = as_list(row.get("tags"))
    diets = as_list(row.get("diets"))
    allergens = as_list(row.get("allergens"))
    meals = as_list(row.get("meals"))
    cuisine = str(row.get("cuisine", "")).strip() or None

    # nutrition
    nutrition = {
        "calories": to_float(row.get("calories")),
        "total_fat_pdv": to_float(row.get("total_fat_pdv")),
        "sugar_pdv": to_float(row.get("sugar_pdv")),
        "sodium_pdv": to_float(row.get("sodium_pdv")),
        "protein_pdv": to_float(row.get("protein_pdv")),
        "saturated_fat_pdv": to_float(row.get("saturated_fat_pdv")),
        "carbohydrates_pdv": to_float(row.get("carbohydrates_pdv")),
    }

    # diet flags (simple heuristics)
    def contains(lst, key):
        k = key.lower()
        return any(k in str(x).lower() for x in lst)
    diet_flags = {
        "is_vegan": contains(diets, "vegan"),
        "is_vegetarian": contains(diets, "vegetarian"),
        "is_gluten_free": contains(diets, "gluten") or contains(tags, "gluten-free"),
        "is_dairy_free": contains(diets, "dairy-free") or not contains(allergens, "dairy"),
    }

    combined_text = str(row.get("combined_text") or "").strip()
    if not combined_text:
        ing = ", ".join(ingredients)
        steps_block = " ".join([f"Step {i+1}. {s}" for i, s in enumerate(steps)]) if steps else ""
        meta_bits = [cuisine] + diets + tags
        meta_line = ", ".join([m for m in meta_bits if m])
        combined_text = (f"{title}\n"
                         f"Ingredients: { ing }\n"
                         f"{ steps_block }\n"
                         f"Meta: { meta_line }").strip()

    # top-level text we will embed
    text = combined_text

    # metadata object
    metadata = {
        "minutes": minutes,
        "servings": servings,
        "serving_size": serving_size,
        "ingredients": ingredients,
        "steps": steps,
        "tags": tags,
        "diets": diets,
        "allergens": allergens,
        "meals": meals,
        "cuisine": cuisine,
        "nutrition": nutrition,
        "diet_flags": diet_flags,
        "source": {
            "dataset": "updated_combined_data_categories_embedded.csv",
            "row_index": row_index
        }
    }

    return {
        "id": rid,
        "title": title,
        "text": text,
        "metadata": metadata
    }

def chunk_text(text: str, max_tokens: int = 400, overlap: int = 80):
    words = text.split()
    if not words:
        return [text]
    chunks = []
    i = 0
    stride = max_tokens - overlap if max_tokens > overlap else max_tokens
    while i < len(words):
        chunks.append(" ".join(words[i:i+max_tokens]))
        i += stride
    return chunks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to the recipes CSV")
    ap.add_argument("--out", default="rag_jsonl", help="Output directory")
    ap.add_argument("--chunk-tokens", type=int, default=400)
    ap.add_argument("--overlap", type=int, default=80)
    ap.add_argument("--limit", type=int, default=0, help="Optional row limit for quick tests")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    df = pd.read_csv(args.csv)
    if args.limit and args.limit > 0:
        df = df.head(args.limit)

    recipes_path = os.path.join(args.out, "recipes.jsonl")
    chunks_path = os.path.join(args.out, "chunks.jsonl")

    with open(recipes_path, "w", encoding="utf-8") as f_recipes, \
         open(chunks_path, "w", encoding="utf-8") as f_chunks:
        for i, row in enumerate(df.to_dict(orient="records")):
            doc = normalize_row(row, row_index=i)
            f_recipes.write(json.dumps(doc, ensure_ascii=False) + "\n")

            # chunk and emit chunk records
            chunks = chunk_text(doc["text"], max_tokens=args.chunk_tokens, overlap=args.overlap)
            for idx, ch in enumerate(chunks):
                chunk_obj = {
                    "chunk_id": f"{doc['id']}:{idx}",
                    "doc_id": doc["id"],
                    "recipe_title": doc["title"],
                    "chunk_index": idx,
                    "text": ch,
                    "metadata": {
                        "minutes": doc["metadata"]["minutes"],
                        "diets": doc["metadata"]["diets"],
                        "allergens": doc["metadata"]["allergens"],
                        "cuisine": doc["metadata"]["cuisine"],
                        "meals": doc["metadata"]["meals"],            # ← add this
                        "ingredients": doc["metadata"]["ingredients"]  # ← and this
                    }
                }
                f_chunks.write(json.dumps(chunk_obj, ensure_ascii=False) + "\n")

    print("[ok] Wrote:")
    print("  -", os.path.abspath(recipes_path))
    print("  -", os.path.abspath(chunks_path))

if __name__ == "__main__":
    main()
