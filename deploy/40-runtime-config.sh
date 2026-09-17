#!/bin/sh
set -eu
config=$(jq -n --arg url "${PUBLIC_SUPABASE_URL:-}" --arg key "${PUBLIC_SUPABASE_ANON_KEY:-}" --arg transport "${PUBLIC_WORKSPACE_TRANSPORT:-rpc}" '{supabaseUrl:$url,supabaseAnonKey:$key,workspaceTransport:$transport}')
printf 'window.APP_CONFIG = %s;\n' "$config" > /usr/share/nginx/html/config.js
