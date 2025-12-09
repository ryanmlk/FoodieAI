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
import os, json, argparse, re, io
import boto3
import faiss
from sentence_transformers import SentenceTransformer
import faiss

### Helper functions

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


def apply_filters(
    results,
    max_minutes=None,
    diet=None,
    meal=None,
    exclude_allergen=None,
    exclude_ingredients=None,
    include_ingredients=None,
    require_ingredients=None,
    max_ingredients=None,
    max_calories=None,
    min_calories=None,
    max_sugar_pdv=None,
    max_sodium_pdv=None,
    min_protein_pdv=None,
    max_steps=None,
    min_servings=None,
    max_servings=None,
    cuisine=None,
    tag=None
):
    wanted_diet = (diet or "").lower().strip()
    wanted_meal = (meal or "").lower().strip()
    wanted_cuisine = (cuisine or "").lower().strip()
    wanted_tag = (tag or "").lower().strip()
    excl_allergen = (exclude_allergen or "").lower().strip()

    def csv_to_list(value: str):
        if not value:
            return []
        return [w.strip().lower() for w in value.split(",") if w.strip()]

    excl_ingredients_list = csv_to_list(exclude_ingredients)
    include_ingredients_list = csv_to_list(include_ingredients)
    require_ingredients_list = csv_to_list(require_ingredients)

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
        cuisine_val = (r.get("cuisine") or "").lower()
        tags = [str(t).lower() for t in (r.get("tags") or [])]
        servings = r.get("servings")
        steps = r.get("steps") or []

        nutrition = r.get("nutrition") or {}
        calories = nutrition.get("calories")
        sugar_pdv_val = nutrition.get("sugar_pdv")
        sodium_pdv_val = nutrition.get("sodium_pdv")
        protein_pdv_val = nutrition.get("protein_pdv")

        # Filters
        if (max_minutes is not None) and isinstance(mins, (int, float)) and (mins > max_minutes):
            continue
        if wanted_diet and not has_substr(diets, wanted_diet):
            continue
        if wanted_meal and not has_substr(meals, wanted_meal):
            continue
        if excl_allergen and has_substr(allergens, excl_allergen):
            continue
        if excl_ingredients_list and not none_contains(ingredients, excl_ingredients_list):
            continue

        if include_ingredients_list:
            has_any = any(
                query_ing in str(ing).lower()
                for query_ing in include_ingredients_list
                for ing in ingredients
            )
            if not has_any:
                continue

        if require_ingredients_list:
            has_all = True
            for query_ing in require_ingredients_list:
                if not any(query_ing in str(ing).lower() for ing in ingredients):
                    has_all = False
                    break
            if not has_all:
                continue

        if max_ingredients is not None:
            if len(ingredients) > max_ingredients:
                continue

        if max_calories is not None and calories is not None:
            if calories > max_calories:
                continue

        if min_calories is not None and calories is not None:
            if calories < min_calories:
                continue

        if max_sugar_pdv is not None and sugar_pdv_val is not None:
            if sugar_pdv_val > max_sugar_pdv:
                continue

        if max_sodium_pdv is not None and sodium_pdv_val is not None:
            if sodium_pdv_val > max_sodium_pdv:
                continue

        if min_protein_pdv is not None and protein_pdv_val is not None:
            if protein_pdv_val < min_protein_pdv:
                continue

        # Complexity (number of steps) and serving filter (min and max serving values)

        if max_steps is not None:
            num_steps = len(steps) if steps is not None else None
            if num_steps is not None and num_steps > max_steps:
                continue

        if min_servings is not None and servings is not None:
            if servings < min_servings:
                continue

        if max_servings is not None and servings is not None:
            if servings > max_servings:
                continue

        # Cuisine and Tags

        if wanted_cuisine:
            if wanted_cuisine not in cuisine_val:
                continue

        if wanted_tag:
            if wanted_tag not in tags:
                continue

        out.append(r)
    return out

s3 = boto3.client("s3")

s3 = boto3.client("s3")

def download_index_from_s3(bucket: str, prefix: str, local_dir: str):
    """
    Download index artifacts from S3 ONLY if they don't already exist locally.
    Required files: recipes_chunks.index, texts.jsonl, metas.jsonl, manifest.json
    """
    os.makedirs(local_dir, exist_ok=True)
    files = ["recipes_chunks.index", "texts.jsonl", "metas.jsonl", "manifest.json"]
    for name in files:
        key = f"{prefix.rstrip('/')}/{name}"
        local_path = os.path.join(local_dir, name)
        if os.path.exists(local_path):
            continue
        s3.download_file(bucket, key, local_path)

def download_recipes_from_s3(bucket: str, prefix: str, local_path: str):
    """
    Download recipes.jsonl from S3 ONLY if it doesn't already exist locally.
    """
    dir_name = os.path.dirname(local_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    key = f"{prefix.rstrip('/')}/recipes.jsonl"
    if os.path.exists(local_path):
        return
    s3.download_file(bucket, key, local_path)

def ensure_index_artifacts(args):
    """
    Ensure that the FAISS index and its sidecar files exist locally.
    If any are missing and an S3 bucket is configured, download them.
    Otherwise, raise a clear error.
    """
    required = ["recipes_chunks.index", "texts.jsonl", "metas.jsonl", "manifest.json"]
    missing = [
        name for name in required
        if not os.path.exists(os.path.join(args.index_dir, name))
    ]

    if not missing:
        return

    if not args.s3_bucket:
        raise SystemExit(
            f"Missing files {missing} in {args.index_dir} and no S3 bucket configured."
        )

    download_index_from_s3(args.s3_bucket, args.s3_prefix, args.index_dir)

    # Re-check after download
    still_missing = [
        name for name in required
        if not os.path.exists(os.path.join(args.index_dir, name))
    ]
    if still_missing:
        raise SystemExit(
            f"After S3 download, still missing {still_missing} in {args.index_dir}."
        )

def ensure_recipes_file(args):
    """
    Ensure recipes.jsonl exists locally when --show-steps is requested.
    If missing and an S3 bucket is configured, download it.
    """
    if not args.show_steps:
        return

    if os.path.exists(args.recipes_jsonl):
        return
    
    if not args.s3_bucket:
        raise SystemExit(
            f"recipes.jsonl not found at {args.recipes_jsonl} and no S3 bucket configured."
        )

    download_recipes_from_s3(args.s3_bucket, args.s3_recipes_prefix, args.recipes_jsonl)

    if not os.path.exists(args.recipes_jsonl):
        raise SystemExit(
            f"After S3 download, recipes.jsonl still not found at {args.recipes_jsonl}."
        )


def main():
    ap = argparse.ArgumentParser(description="Query a FAISS index of recipe chunks")
    ap.add_argument("--index-dir", default="index_artifacts", help="Directory with recipes_chunks.index + sidecars")
    ap.add_argument("--query", required=True, help="Search query")
    ap.add_argument("--top-k", type=int, default=10, help="Number of recipes to return after dedupe")

    ap.add_argument("--filter-max-minutes", type=int, default=None, help="e.g., 30")
    ap.add_argument("--filter-diet", type=str, default=None, help="e.g., vegan (substring match allowed)")
    ap.add_argument("--filter-meal", type=str, default=None, help="e.g., dinner / lunch / breakfast")
    ap.add_argument("--exclude-allergen", type=str, default=None, help="e.g., nuts")
    ap.add_argument("--exclude-ingredients", type=str, default=None, help="comma-separated e.g. 'chicken, beef'")
    ap.add_argument("--show-steps", action="store_true", 
                    help="After retrieving, load recipes.jsonl and print full step-by-step instructions")
    ap.add_argument("--recipes-jsonl", default="rag_jsonl/recipes.jsonl", 
                    help="Path to recipes.jsonl (used with --show-steps)")
    ap.add_argument("--include-ingredients", type=str, default=None,
                    help="Comma-separated ingredients; keep recipes that contain ANY of them")
    ap.add_argument("--require-ingredients", type=str, default=None,
                    help="Comma-separated ingredients; keep recipes that contain ALL of them")
    ap.add_argument("--filter-max-ingredients", type=int, default=None,
                    help="Max number of ingredients allowed (simplicity filter)")
    ap.add_argument("--filter-max-calories", type=float, default=None,
                    help="Max calories per serving")
    ap.add_argument("--filter-min-calories", type=float, default=None,
                    help="Min calories per serving")
    ap.add_argument("--filter-max-sugar-pdv", type=float, default=None,
                    help="Max %%DV sugar")
    ap.add_argument("--filter-max-sodium-pdv", type=float, default=None,
                    help="Max %%DV sodium")
    ap.add_argument("--filter-min-protein-pdv", type=float, default=None,
                    help="Min %%DV protein")
    ap.add_argument("--filter-max-steps", type=int, default=None,
                    help="Max number of steps")
    ap.add_argument("--filter-min-servings", type=int, default=None,
                    help="Min servings")
    ap.add_argument("--filter-max-servings", type=int, default=None,
                    help="Max servings")
    ap.add_argument("--filter-cuisine", type=str, default=None,
                    help="Required cuisine (substring match, e.g. 'italian')")
    ap.add_argument("--filter-tag", type=str, default=None,
                    help="Required tag (e.g. 'kid-friendly', 'bbq')")
    
    # S3 related arguments
    ap.add_argument("--s3-bucket", type=str, default="foodieai-data",
                help="S3 bucket name to download index files from")
    ap.add_argument("--s3-prefix", type=str, default="index_artifacts",
                help="Prefix inside the S3 bucket for index files")
    ap.add_argument("--s3-recipes-prefix", type=str, default="rag_jsonl",
                help="S3 prefix where recipes.jsonl is stored")

    args = ap.parse_args()

    ensure_index_artifacts(args)

    ensure_recipes_file(args)

    man_path = os.path.join(args.index_dir, "manifest.json")
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

    # Loading index + sidecars
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

    # Embedding the query
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
        m["text"] = texts[i]
        raw.append(m)

    # Applying filters
    filt = apply_filters(
        raw,
        max_minutes=args.filter_max_minutes,
        diet=args.filter_diet,
        meal=args.filter_meal,
        exclude_allergen=args.exclude_allergen,
        exclude_ingredients=args.exclude_ingredients,
        include_ingredients=args.include_ingredients,
        require_ingredients=args.require_ingredients,
        max_ingredients=args.filter_max_ingredients,
        max_calories=args.filter_max_calories,
        min_calories=args.filter_min_calories,
        max_sugar_pdv=args.filter_max_sugar_pdv,
        max_sodium_pdv=args.filter_max_sodium_pdv,
        min_protein_pdv=args.filter_min_protein_pdv,
        max_steps=args.filter_max_steps,
        min_servings=args.filter_min_servings,
        max_servings=args.filter_max_servings,
        cuisine=args.filter_cuisine,
        tag=args.filter_tag
    )

    # Dedupe by doc_id, keeping highest score
    best = {}
    for r in filt:
        k = r.get("doc_id")
        if k not in best or r["score"] > best[k]["score"]:
            best[k] = r

    results = sorted(best.values(), key=lambda x: x["score"], reverse=True)[:args.top_k]

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
                    # store if found
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

        # print the steps
        if args.show_steps:
            steps = id_to_steps.get(str(r.get("doc_id")))
            if steps:
                print("    Steps:")
                for si, s in enumerate(steps, 1):
                    print(f"      {si}. {s}")
            else:
                print("(No structured steps found for this recipe)")
            print()

if __name__ == "__main__":
    main()
