# router_from_sheet.py
# Pipeline fonctionnel basé sur ton fichier tableau (CSV ou XLSX)

from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import re
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer


# --------------------------
# Data structures
# --------------------------

@dataclass
class SheetIndex:
    ids: List[str]  # liste d'ids (ex: "203.4403....txt")
    titles: List[str]  # titres extraits des textes
    texts: List[str]  # textes (sans le préfixe nom-de-fichier)
    urls: Dict[str, str]  # id -> chunk_url
    embs: np.ndarray  # (N, d) embeddings normalisés
    model_name: str  # modèle utilisé


# --------------------------
# Helpers
# --------------------------

def _extract_filename_prefix(s: str) -> Tuple[str, str]:
    """
    Dans 'chunk_name', on a 'FILENAME.txt ...reste du texte...'.
    Cette fonction renvoie (filename, text_sans_filename).
    """
    if not isinstance(s, str):
        return "", ""
    # filename = 1er token qui se termine par .txt
    m = re.match(r"\s*([^\s]+\.txt)\s*(.*)", s, flags=re.DOTALL)
    if not m:
        # fallback: pas de filename détecté
        return "", s.strip()
    filename, rest = m.group(1), m.group(2)
    return filename.strip(), rest.strip()


def _extract_title(text: str) -> str:
    """Titre = 1re ligne commençant par '#' si présente, sinon 1re ligne brute."""
    if not text:
        return ""
    for line in text.splitlines():
        l = line.strip()
        if l.startswith("#"):
            return l.lstrip("#").strip()
    # sinon début du texte (limité pour éviter les pavés)
    return text.splitlines()[0].strip()[:160]


def _ensure_2d(x: np.ndarray) -> np.ndarray:
    return x if x.ndim == 2 else x[None, :]


# --------------------------
# Loading
# --------------------------

def load_sheet(path: str) -> pd.DataFrame:
    """
    Charge un CSV ou un XLSX en détectant par extension.
    Doit contenir: chunk_url, chunk_id, chunk_name (et idéalement chunk_number).
    """
    if path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    # normalise les noms de colonnes (au cas où)
    df.columns = [c.strip() for c in df.columns]
    required = {"chunk_url", "chunk_id", "chunk_name","chunk_content"}
    missing = required - set(df.columns)
    print(df.values)
    if missing:
        raise ValueError(f"Colonnes manquantes dans {path}: {missing}")
    return df


def build_index_from_sheet(
        df: pd.DataFrame,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        device: Optional[str] = None,
) -> SheetIndex:
    """
    À partir du DataFrame, extrait ids/titres/textes/urls et crée les embeddings.
    - id = filename détecté dans chunk_name (ex: '203.4403....txt')
      (si non trouvé, fallback sur str(chunk_id)+'.txt')
    - titre = première ligne '# ...' ou 1re ligne brute
    """
    ids: List[str] = []
    titles: List[str] = []
    texts: List[str] = []
    urls: Dict[str, str] = {}

    for _, row in df.iterrows():
        url = str(row["chunk_url"]).strip()
        chunk_name = str(row["chunk_name"])
        fn, rest = _extract_filename_prefix(chunk_name)

        if not fn:
            # fallback robuste
            fn = f"{row['chunk_id']}.txt"

        text = rest if rest else chunk_name
        title = _extract_title(text)

        ids.append(fn)
        titles.append(title)
        texts.append(text)
        urls[fn] = url

    # embeddings sur TITRES (rapide, robuste pour routing d’intention)
    model = SentenceTransformer(model_name, device=device)
    embs = model.encode(titles, normalize_embeddings=True)
    embs = _ensure_2d(np.asarray(embs))

    return SheetIndex(
        ids=ids,
        titles=titles,
        texts=texts,
        urls=urls,
        embs=embs,
        model_name=model_name,
    )


# --------------------------
# Search
# --------------------------

def top_k_from_query(
        index: SheetIndex,
        query: str,
        k: int = 5,
        device: Optional[str] = None,
) -> List[Tuple[str, str, float, str]]:
    """
    Retourne une liste triée de tuples:
      (chunk_id, title, score, url)
    """
    model = SentenceTransformer(index.model_name, device=device)
    q = model.encode([query], normalize_embeddings=True)[0]  # (d,)
    sims = index.embs @ q  # cosinus
    order = np.argsort(-sims)[:k]

    results: List[Tuple[str, str, float, str]] = []
    for i in order:
        cid = index.ids[i]
        results.append((cid, index.titles[i], float(sims[i]), index.urls.get(cid, "")))
    return results


def chunk_text_by_id(index: SheetIndex, chunk_id: str) -> str:
    """Récupère le texte du chunk (par son id)."""
    try:
        i = index.ids.index(chunk_id)
        return index.texts[i]
    except ValueError:
        return ""


