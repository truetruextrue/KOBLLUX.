#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, hashlib
from datetime import datetime, timezone
def _ts(): return datetime.now(timezone.utc).isoformat()
def digital_root(n): return 0 if n == 0 else 1 + (n - 1) % 9
KOB_FRACTAL = 1134
KOB_LEI = "VERDADE × INTEGRAR ÷ Δ = ∞"
ARQUETIPO_MAP = {
    "push": ("Pulse", 3, "ᛈᛉ", 396), "pull_request": ("Nova", 3, "ᚷᛁ", 432),
    "create": ("Atlas", 3, "ᚨᚠ", 594), "delete": ("Kaos", 9, "ᚲᚦ", 741),
    "release": ("Aion", 9, "ᚨᛇ", 963), "workflow_run": ("Genus", 6, "ᚷᛜ", 852),
}
e = os.environ.get
event_name = e("KOB_EVENT", "push")
sha = e("KOB_SHA", "")
repo = e("KOB_REPO", "")
branch = e("KOB_BRANCH", "")
actor = e("KOB_ACTOR", "")
msg = e("KOB_MSG", "")[:72]
arquetipo, nivel, runa, hz = ARQUETIPO_MAP.get(event_name, ("Rhea", 9, "ᚱᛇ", 174))
evento = {
    "ts": _ts(), "z": sha[:16], "ciclo": digital_root(KOB_FRACTAL),
    "arquetipo": arquetipo, "runa": runa, "hz": hz, "evento": event_name,
    "repo": repo, "branch": branch, "actor": actor, "commit_msg": msg,
    "seed": digital_root(KOB_FRACTAL),
    "chain": {"fractal": KOB_FRACTAL, "nivel": nivel, "lei": KOB_LEI, "ciclo_seq": [3,6,9,7]},
}
with open("kobllux_memory.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(evento, ensure_ascii=False) + "\n")
sha256 = hashlib.sha256(json.dumps(evento, sort_keys=True).encode()).hexdigest()
seal = {"ts": _ts(), "artefato": f"{event_name}_{sha[:8]}", "arquetipo": arquetipo,
        "sha256": sha256, "hz": 777, "sinal": "∞"}
seals = []
if os.path.exists("kobllux_seal.json"):
    try:
        with open("kobllux_seal.json") as f: seals = json.load(f)
    except: pass
seals.append(seal)
with open("kobllux_seal.json", "w", encoding="utf-8") as f:
    json.dump(seals[-200:], f, ensure_ascii=False, indent=2)
print(f"{runa} {arquetipo} [{hz}Hz] nível:{nivel} | {event_name} | {repo}")
