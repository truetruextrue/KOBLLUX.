#!/data/data/com.termux/files/usr/bin/bash
# KOBLLUX · MOTOR LOCAL ∆³ · KOB--NODE
# utcnow() corrigido · path KOB--NODE confirmado
KOB_HOME="$HOME/KOB--NODE"
Z="${*:-KOBLLUX ∆³ motor local}"
command -v python3 &>/dev/null || { echo "[ERRO] pkg install python"; exit 1; }
for MOTOR_PATH in \
    "$KOB_HOME/codex-azure/kobllux_motor.py" \
    "$KOB_HOME/infodose/kobllux_motor.py" \
    "./kobllux_motor.py"; do
    [ -f "$MOTOR_PATH" ] && cd "$(dirname "$MOTOR_PATH")" && exec python3 kobllux_motor.py "$Z"
done
python3 - "$Z" << 'PYMOTOR'
import sys, hashlib, json, datetime, os
Z = " ".join(sys.argv[1:]) or "KOBLLUX ∆³"
ts = datetime.datetime.now(datetime.timezone.utc).isoformat()  # FIXED
sha = hashlib.sha256(Z.encode()).hexdigest()
md5 = hashlib.md5(Z.encode()).hexdigest()
blake = hashlib.blake2b(Z.encode()).hexdigest()
print(f"\nᛜᛇᛟ Kobllux 0x0F [1134Hz]\nZ: {Z}\nSHA256: {sha[:32]}…\nMD5: {md5[:16]}…\n{ts}\nVERDADE × INTEGRAR ÷ Δ = ∞")
log = os.path.expanduser("~/KOB--NODE/logs/motor_local.jsonl")
os.makedirs(os.path.dirname(log), exist_ok=True)
with open(log, "a") as f:
    f.write(json.dumps({"ts":ts,"z":Z,"sha256":sha,"md5":md5[:16]}, ensure_ascii=False)+"\n")
print(f"[log] {log}")
PYMOTOR
