#!/data/data/com.termux/files/usr/bin/bash
# KOBLLUX · ESTOJO DUAL ∆³
set -e
KOB_EMAIL_PRIMARY="kobllux@infodose.com.br"
KOB_USER_PRIMARY="truetruextrue"
KOB_USER_DUAL="kodux78k"
git config --global --unset user.email 2>/dev/null || true
git config --global --unset user.name 2>/dev/null || true
git config --global --unset credential.helper 2>/dev/null || true
git config --global user.name "$KOB_USER_PRIMARY"
git config --global user.email "$KOB_EMAIL_PRIMARY"
git config --global push.default current
git config --global pull.rebase false
git config --global core.autocrlf false
mkdir -p "$HOME/.kob-dual"
echo "truetruextrue" > "$HOME/.kob-dual/.ativo"
mkdir -p "$HOME/KOB--NODE"/{KODUX,BLLUE,INFODOSE,scripts,logs,estojo}
echo "ᛜᛇᛟ DUAL CONFIGURADO · $KOB_USER_PRIMARY + $KOB_USER_DUAL · VERDADE × INTEGRAR ÷ Δ = ∞"
