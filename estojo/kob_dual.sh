#!/data/data/com.termux/files/usr/bin/bash
# KOBLLUX · KOB DUAL SWITCHER ∆³
KOB_DUAL_STATE="$HOME/.kob-dual/.ativo"
KOB_USER_PRIMARY="truetruextrue"; KOB_EMAIL_PRIMARY="kobllux@infodose.com.br"
KOB_USER_DUAL="kodux78k"; KOB_EMAIL_DUAL="kodux78k@infodose.com.br"
CMD="${1:-status}"
ativar_primario() { git config --global user.name "$KOB_USER_PRIMARY"; git config --global user.email "$KOB_EMAIL_PRIMARY"; echo "$KOB_USER_PRIMARY" > "$KOB_DUAL_STATE"; echo "ᚲᛞ [truetruextrue] ATIVO"; }
ativar_dual() { git config --global user.name "$KOB_USER_DUAL"; git config --global user.email "$KOB_EMAIL_DUAL"; echo "$KOB_USER_DUAL" > "$KOB_DUAL_STATE"; echo "ᛒᛚ [kodux78k] DUAL SOBRE"; }
case "$CMD" in
    truetruextrue|principal|kodux) ativar_primario ;;
    kodux78k|dual|sobre|SOBRE) ativar_dual ;;
    status|s) echo "ᛜᛇᛟ $(git config --global user.name 2>/dev/null) <$(git config --global user.email 2>/dev/null)" ;;
    toggle|t) [ "$(cat "$KOB_DUAL_STATE" 2>/dev/null)" = "$KOB_USER_PRIMARY" ] && ativar_dual || ativar_primario ;;
    *) echo "Uso: $0 [truetruextrue|sobre|status|toggle]" ;;
esac
