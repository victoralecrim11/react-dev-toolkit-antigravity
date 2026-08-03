#!/usr/bin/env bash
# Atualiza o React Dev Hub no Antigravity.
#
# Rode depois de um push para trazer a versao nova do plugin.
# Nao instala o plugin do zero -- para isso, veja o README.
#
# O Antigravity nao recarrega plugins em sessao aberta: reinicie o app
# ou reabra o workspace depois de atualizar.
#
# Uso:
#   ./scripts/atualizar-plugin.sh
#   ./scripts/atualizar-plugin.sh --limpar-cache

set -uo pipefail

PLUGIN="${PLUGIN:-plugin-react-dev-toolkit}"
LIMPAR_CACHE=0
falhas=()

for arg in "$@"; do
  case "$arg" in
    --limpar-cache) LIMPAR_CACHE=1 ;;
    -h|--help) sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argumento desconhecido: $arg" >&2; exit 2 ;;
  esac
done

titulo() { printf '\n\033[36m== %s\033[0m\n' "$1"; }
aviso()  { printf '\033[33m  %s\033[0m\n' "$1"; }
ok()     { printf '\033[32m  %s\033[0m\n' "$1"; }
existe() { command -v "$1" >/dev/null 2>&1; }

plugins_dir="$HOME/.gemini/config/plugins"

titulo 'Antigravity'
if existe agy; then
  if [ "$LIMPAR_CACHE" -eq 1 ]; then
    plugin_path="$plugins_dir/$PLUGIN"
    if [ -d "$plugin_path" ]; then
      rm -rf "$plugin_path"
      aviso "plugin removido: $plugin_path"
    fi
    cli_path="$HOME/.gemini/antigravity-cli/plugins"
    if [ -d "$cli_path/$PLUGIN" ]; then
      rm -rf "$cli_path/$PLUGIN"
      aviso "plugin CLI removido: $cli_path/$PLUGIN"
    fi
  fi
  agy plugin update "$PLUGIN" \
    || falhas+=('agy plugin update')
  ok 'feito. Reinicie o Antigravity para carregar os arquivos novos.'
else
  aviso "CLI 'agy' nao encontrada no PATH -- pulando."
  aviso "Para atualizar manualmente: copie a pasta do plugin para $plugins_dir/$PLUGIN"
fi

echo
if [ "${#falhas[@]}" -gt 0 ]; then
  printf '\033[31mFalhou: %s\033[0m\n' "${falhas[*]}"
  exit 1
fi
ok 'Atualizacao concluida.'
