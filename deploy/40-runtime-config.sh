#!/bin/sh
set -eu
config=$(jq -n --arg url "${PUBLIC_SUPABASE_URL:-}" --arg key "${PUBLIC_SUPABASE_ANON_KEY:-}" '{supabaseUrl:$url,supabaseAnonKey:$key}')
printf 'window.APP_CONFIG = %s;\n' "$config" > /usr/share/nginx/html/config.js
