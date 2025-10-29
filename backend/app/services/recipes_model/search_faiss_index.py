#!/usr/bin/env python3
"""
search_faiss_index.py — query the FAISS index built by build_faiss_index.py

Usage:
  python search_faiss_index.py --index-dir index_artifacts --query "vegan dinner under 30 minutes" --top-k 10
  # Optional filters:
  --filter-max-minutes 30
  --filter-diet vegan
  --filter-meal dinner
  --exclude-allergen nuts
  --exclude-ingredients "chicken, beef, pork, fish, shrimp, salmon, tuna, turkey"
"""
import os, json, argparse, re
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss

def read_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def auto_filters_from_query(q: str):
    ql = q.lower()
    filters = {}

    # time like: under 30 minutes / <30 minutes / 25 min / 20mins
    m = re.search(r"(?:under|less than|<)\s*(\d+)\s*(?:min|minutes?)", ql)
    if not m:
        m = re.search(r"\b(\d+)\s*(?:min|minutes?)\b", ql)
    if m:
        filters["filter_max_minutes"] = int(m.group(1))

    # common diet keywords
    for diet in ["vegan","vegetarian","gluten-free","gluten free","dairy-free","dairy free","keto","paleo"]:
        if diet in ql:
            filters["filter_diet"] = diet.replace(" ", "-")
            break

    # meal cues (optional, only if your metadata has meals)
    for meal in ["breakfast","brunch","lunch","dinner","snack","dessert"]:
        if meal in ql:
            filters["filter_meal"] = meal
            break

    return filters


def apply_filters(results, max_minutes=None, diet=None, meal=None, exclude_allergen=None, exclude_ingredients=None):
    wanted_diet = (diet or "").lower().strip()
    wanted_meal = (meal or "").lower().strip()
    excl_allergen = (exclude_allergen or "").lower().strip()

    excl_ingredients = []
    if exclude_ingredients:
        excl_ingredients = [w.strip().lower() for w in exclude_ingredients.split(",") if w.strip()]

    def has_substr(lst, needle):
        if not needle:
            return True
        if not lst:
            return False
        return any(needle in str(x).lower() for x in lst)

    def none_contains(lst, ban_list):
        txt = " ".join([str(x).lower() for x in (lst or [])])
        return all(b not in txt for b in ban_list)

    out = []
    for r in results:
        mins = r.get("minutes")
        diets = r.get("diets") or []
        allergens = r.get("allergens") or []
        meals = r.get("meals") or []
        ingredients = r.get("ingredients") or []

        if (max_minutes is not None) and (isinstance(mins, (int, float))) and (mins > max_minutes):
            continue
        if wanted_diet and not has_substr(diets, wanted_diet):
            continue
        if wanted_meal and not has_substr(meals, wanted_meal):
            continue
        if excl_allergen and has_substr(allergens, excl_allergen):
            continue
        if excl_ingredients and not none_contains(ingredients, excl_ingredients):
            continue

        out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser(description="Query a FAISS index of recipe chunks")
    ap.add_argument("--index-dir", default="index_artifacts", help="Directory with recipes_chunks.index + sidecars")
    ap.add_argument("--query", required=True, help="Search query")
    ap.add_argument("--top-k", type=int, default=10, help="Number of recipes to return after dedupe")
    ap.add_argument("--filter-max-minutes", type=int, default=None)
    ap.add_argument("--filter-diet", type=str, default=None, help="e.g., vegan (substring match allowed)")
    ap.add_argument("--filter-meal", type=str, default=None, help="e.g., dinner / lunch / breakfast")
    ap.add_argument("--exclude-allergen", type=str, default=None, help="e.g., nuts")
    ap.add_argument("--exclude-ingredients", type=str, default=None, help="comma-separated e.g. 'chicken, beef'")
    ap.add_argument("--show-steps", action="store_true", help="After retrieving, load recipes.jsonl and print full step-by-step instructions")
    ap.add_argument("--recipes-jsonl", default="rag_jsonl/recipes.jsonl", help="Path to recipes.jsonl (used with --show-steps)")

    args = ap.parse_args()

    # Load manifest (to get embed model used to build the index)
    man_path = os.path.join(args.index_dir, "manifest.json")
    if not os.path.exists(man_path):
        raise SystemExit(f"manifest.json not found in {args.index_dir}. Build the index first.")
    with open(man_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    auto = auto_filters_from_query(args.query)
    if "filter_max_minutes" in auto and args.filter_max_minutes is None:
        args.filter_max_minutes = auto["filter_max_minutes"]
    if "filter_diet" in auto and args.filter_diet is None:
        args.filter_diet = auto["filter_diet"]
    if "filter_meal" in auto and args.filter_meal is None:
        args.filter_meal = auto["filter_meal"]

    embed_model_name = manifest.get("embed_model", "sentence-transformers/all-MiniLM-L6-v2")

    # Load index + sidecars
    index_path = os.path.join(args.index_dir, "recipes_chunks.index")
    texts_path = os.path.join(args.index_dir, "texts.jsonl")
    metas_path = os.path.join(args.index_dir, "metas.jsonl")

    if not os.path.exists(index_path):
        raise SystemExit(f"FAISS index not found: {index_path}")
    if not os.path.exists(texts_path) or not os.path.exists(metas_path):
        raise SystemExit("Missing texts.jsonl or metas.jsonl. Rebuild the index.")

    index = faiss.read_index(index_path)
    texts = []
    for rec in read_jsonl(texts_path):
        # built as {"text": "..."} — accept either dict or raw string for robustness
        if isinstance(rec, dict) and "text" in rec:
            texts.append(rec["text"])
        elif isinstance(rec, str):
            texts.append(rec)
        else:
            texts.append(str(rec))

    metas = [rec for rec in read_jsonl(metas_path)]
    if len(texts) != len(metas):
        raise SystemExit("texts.jsonl and metas.jsonl length mismatch. Rebuild the index.")

    # Embed the query with the SAME model used at build time
    model = SentenceTransformer(embed_model_name)
    q = model.encode([args.query], convert_to_numpy=True, normalize_embeddings=True)
    scores, ids = index.search(q, args.top_k * 5)  # over-retrieve, then filter/dedupe
    ids, scores = ids[0], scores[0]

    raw = []
    for i, s in zip(ids, scores):
        if i < 0:
            continue
        m = dict(metas[i])
        m["score"] = float(s)
        m["text"] = texts[i]  # << fixed: texts[i] is already the string
        raw.append(m)

    # Apply filters
    filt = apply_filters(
        raw,
        max_minutes=args.filter_max_minutes,
        diet=args.filter_diet,
        meal=args.filter_meal,
        exclude_allergen=args.exclude_allergen,
        exclude_ingredients=args.exclude_ingredients,
    )

    # Dedupe by doc_id, keep highest score
    best = {}
    for r in filt:
        k = r.get("doc_id")
        if k not in best or r["score"] > best[k]["score"]:
            best[k] = r

    results = sorted(best.values(), key=lambda x: x["score"], reverse=True)[:args.top_k]
    # Optional: join back to full steps from recipes.jsonl
    id_to_steps = {}
    if args.show_steps and results:
        try:
            with open(args.recipes_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    # common doc_id locations
                    doc_id = str(
                        rec.get("id")
                        or rec.get("doc_id")
                        or (rec.get("metadata") or {}).get("doc_id")
                        or ""
                    )
                    steps = None
                    meta = rec.get("metadata") or {}
                    # try a few likely keys
                    if isinstance(meta.get("steps"), list):
                        steps = meta["steps"]
                    elif isinstance(rec.get("steps"), list):
                        steps = rec["steps"]
                    # store if we found something
                    if doc_id:
                        id_to_steps[doc_id] = steps
        except FileNotFoundError:
            print(f"[warn] recipes.jsonl not found at {args.recipes_jsonl}; cannot show full steps.")


    if not results:
        print("No results found.")
        return

    print(f"Top {len(results)} recipes for: \"{args.query}\"\n")
    for i, r in enumerate(results, 1):
        line = [
            f"Title: {r.get('recipe_title')}",
            f"Minutes: {r.get('minutes')}",
            f"Diets: {', '.join(r.get('diets') or [])}",
            f"Allergens: {', '.join(r.get('allergens') or [])}",
            f"Cuisine: {r.get('cuisine') or ''}",
            f"Score: {r.get('score'):.3f}",
        ]
        print(f"{i:>2}. " + " | ".join(line))

        snippet = (r.get("text") or "")[:260].replace("\n", " ")
        print(f"    {snippet}...\n")

        # printing the steps in a structured way
        if args.show_steps:
            steps = id_to_steps.get(str(r.get("doc_id")))
            if steps:
                print("    Steps:")
                for si, s in enumerate(steps, 1):
                    print(f"      {si}. {s}")
            else:
                print("    (No structured steps found for this recipe)")
            print()

if __name__ == "__main__":
    main()
