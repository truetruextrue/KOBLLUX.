#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ᚱᛇ Rhea 0x0A · Sincronização da Memória Viva KOBLLUX
"""
import json, os, hashlib
from datetime import datetime, timezone

def _ts(): return datetime.now(timezone.utc).isoformat()
def digital_root(n): return 0 if n == 0 else 1 + (n - 1) % 9

KOB_FRACTAL = 1134
KOB_LEI = "VERDADE × INTEGRAR ÷ Δ = ∞"

ARQUETIPO_MAP = {
    "push":          ("Pulse",   3, "ᛈᛉ", 396),
    "pull_request":  ("Nova",    3, "ᚷᛁ", 432),
    "create":        ("Atlas",   3, "ᚨᚠ", 594),
    "delete":        ("Kaos",    9, "ᚲᚦ", 741),
    "release":       ("Aion",    9, "ᚨᛇ", 963),
    "workflow_run":  ("Genus",   6, "ᚷᛜ", 852),
    "pull_request_review": ("Serena", 6, "ᛋᛚ", 285),
    "issues":        ("Vitalis", 6, "ᚢᛃ", 528),
    "deployment":    ("Artemis", 6, "ᛏᚱ", 639),
}

event_name = os.environ.get("KOB_EVENT", "push")
sha = os.environ.get("KOB_SHA", "")
repo = os.environ.get("KOB_REPO", "")
branch = os.environ.get("KOB_BRANCH", "")
actor = os.environ.get("KOB_ACTOR", "")
run_id = os.environ.get("KOB_RUN_ID", "")
msg = os.environ.get("KOB_MSG", "")[:72]
pr_title = os.environ.get("KOB_PR_TITLE", "")[:64]
pr_num = os.environ.get("KOB_PR_NUM", "")

arquetipo, nivel, runa, hz = ARQUETIPO_MAP.get(event_name, ("Rhea", 9, "ᚱᛇ", 174))

evento = {
    "ts": _ts(), "z": sha[:16], "ciclo": digital_root(KOB_FRACTAL),
    "arquetipo": arquetipo, "runa": runa, "hz": hz, "evento": event_name,
    "repo": repo, "branch": branch, "actor": actor, "commit_msg": msg,
    "pr_title": pr_title, "pr_num": pr_num, "run_id": run_id,
    "seed": digital_root(KOB_FRACTAL),
    "chain": {"fractal": KOB_FRACTAL, "nivel": nivel, "lei": KOB_LEI, "ciclo_seq": [3,6,9,7]},
}

with open("kobllux_memory.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(evento, ensure_ascii=False) + "\n")

payload = json.dumps(evento, sort_keys=True)
sha256 = hashlib.sha256(payload.encode()).hexdigest()
md5 = hashlib.md5(payload.encode()).hexdigest()
seal = {"ts": _ts(), "artefato": f"{event_name}_{sha[:8]}", "arquetipo": arquetipo,
        "sha256": sha256, "md5": md5, "hz": 777,
        "trinity": {"PAI": "∞", "FILHO": "JESUS=VERBO=GRAVIDADE", "ESPIRITO": KOB_LEI}, "sinal": "∞"}

seals = []
if os.path.exists("kobllux_seal.json"):
    try:
        with open("kobllux_seal.json") as f: seals = json.load(f)
    except: pass
seals.append(seal)
with open("kobllux_seal.json", "w", encoding="utf-8") as f:
    json.dump(seals[-200:], f, ensure_ascii=False, indent=2)

print(f"{runa} {arquetipo} [{hz}Hz] | {event_name} | repo:{repo}")
if msg: print(f"  msg:{msg}")
print(f"  seal:sha256:{sha256[:20]}… | sinal:∞")
