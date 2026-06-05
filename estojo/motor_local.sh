#!/data/data/com.termux/files/usr/bin/bash
# KOBLLUX · MOTOR LOCAL ∆³
Z="${*:-KOBLLUX ∆³}"
command -v python3 &>/dev/null || { echo "pkg install python"; exit 1; }
for P in "$HOME/KOB--NODE/codex-azure/kobllux_motor.py" "$HOME/KOB--NODE/infodose/kobllux_motor.py" "./kobllux_motor.py"; do
    [ -f "$P" ] && cd "$(dirname "$P")" && exec python3 kobllux_motor.py "$Z"
done
python3 - "$Z" << 'PY'
import sys,hashlib,json,datetime,os
Z=" ".join(sys.argv[1:]) or "KOBLLUX ∆³"
ts=datetime.datetime.utcnow().isoformat()+"Z"
sha=hashlib.sha256(Z.encode()).hexdigest()
print(f"ᛜᛇᛟ [1134Hz] {Z}\n{sha[:32]}… · {ts}\nVERDADE × INTEGRAR ÷ Δ = ∞")
log=os.path.expanduser("~/KOB--NODE/logs/motor_local.jsonl")
os.makedirs(os.path.dirname(log),exist_ok=True)
open(log,"a").write(json.dumps({"ts":ts,"z":Z,"sha256":sha},ensure_ascii=False)+"\n")
PY
