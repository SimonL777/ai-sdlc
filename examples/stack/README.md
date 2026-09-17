# Four-repository NAS deployment

Implementation is at the code-written stage. Runtime validation is intentionally deferred; do not interpret this document as proof of a deployed stack.

## Layout

Keep the four repositories as siblings:

```text
workspace/
  sandbox-gateway/
  model-gateway/
  automation-platform/
  ai-sdlc/examples/stack/
```

Requirements: a Linux Docker host/NAS with Docker Compose v2, Python 3 for setup/smoke scripts, outbound access to image/package registries and Supabase, and enough available RAM for three JVMs plus one browser container (start with roughly 3 GiB available, then measure).

## Supabase setup

Use a dedicated development Supabase project. Do not point first-run migrations at existing business projects.

1. Apply `ai-sdlc/supabase/migrations/202609180001_workspaces.sql` through your normal Supabase SQL workflow. It creates the user-owned workspace table and two private artifact buckets.
2. Each Java service applies Flyway migrations to its own schema: `sandbox_gateway`, `model_gateway`, `automation_platform`. Configure a database role with the needed schema/migration permissions. The deployment sample uses one operator-managed database connection for simplicity; production can split roles. JDBC does not automatically impersonate `auth.uid()`.
3. Use a TLS PostgreSQL JDBC endpoint appropriate to your NAS network. Supabase direct connection or a suitable session pooler is preferable for the small persistent Java pools. Verify IPv4/IPv6 reachability. If you choose transaction pooling, check prepared-statement compatibility before use.
4. Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in private `.env`; the service-role key remains in Java containers, never browser config.
5. Optional Supabase user login: deploy `ai-sdlc-workspaces` Edge Function, set `PUBLIC` frontend settings via `.env`'s `SUPABASE_URL` and `SUPABASE_ANON_KEY`, and configure `SUPABASE_JWT_ISSUER` and `SUPABASE_JWKS_URL` for an asymmetric-signing Supabase project. The Edge Function verifies the user through Auth and uses the user's JWT for RLS. Legacy HS256 projects need a compatible authentication adapter; do not disable Java verification.

Operator-token mode can run the full material → workflow → Docker → report path without Edge deployment. In that mode material is persisted in the automation service's database task; the optional separate Workspace table is used only with Supabase user login. This is an explicit mode distinction.

## Configure and start

```bash
cd ai-sdlc/examples/stack
python3 setup_env.py
# Edit .env privately: database, Supabase, Docker socket group and provider settings.
python3 check_config.py
sh start.sh
```

The generator finds the Docker socket group when run on the Docker host. Otherwise set `DOCKER_GID` on the NAS. The Sandbox service needs that group to access the socket; the temporary Runner never receives the socket, host mounts or cloud credentials.

The web listener defaults to `127.0.0.1:8098`. For a private LAN demo set `BIND_ADDRESS=0.0.0.0` and place access behind your LAN/VPN or authenticated TLS reverse proxy. Avoid publishing the Docker daemon or Java service ports. Log into the workbench with the private `API_TOKEN` generated in `.env`.

`MODEL_MODE=mock` is the default and is visibly synthetic. To verify a real provider set `MODEL_MODE=upstream`, an HTTPS `MODEL_BASE_URL` ending in the provider's API prefix (for example `/v1`), `MODEL_API_KEY` and `MODEL_NAME`. Do not commit real values.

To enable Git snapshots, set an operator-owned allowlist such as `GIT_REPOSITORIES_JSON={"sample":"https://github.com/OWNER/PUBLIC_REPOSITORY.git"}`. Requests may choose a registered key and safe ref; they cannot supply arbitrary repository URLs, credentials or shell commands.

## Runtime acceptance — run only when ready to debug

```bash
python3 smoke.py
python3 smoke.py --negative
```

Positive smoke checks durable run status, idempotent replay, a real Docker/Playwright result, matching Java/Runner compiler hashes, and actual container cleanup. Negative smoke uses an intentionally false assertion. The JSON proof includes IDs and provider mode but no secrets. A mock-model pass is infrastructure proof, not real-LLM quality proof.

## Explicit local-development alternative

`python3 setup_env.py --local` opts into H2 and local artifact volumes. It is for development/contract checks and does not validate PostgreSQL, Supabase RLS/Storage or NAS connectivity. The production target remains Supabase. No silent fallback occurs.

## Operation and limits

- Use `docker compose logs --tail 100 SERVICE` and the protected task APIs to investigate failures; never paste `.env` into issues.
- A single scheduled worker per service polls durable tasks. Thread/lease/state fencing prevents stale completion; process restart marks expired uncertain work `LOST` rather than silently repeating side effects. This is not a distributed exactly-once service.
- Cancellation is cooperative at task boundaries. Git operations have finite process deadlines; a currently blocked Git command may finish or time out before the worker notices cancellation.
- Container cleanup has a separate status and reconciliation pass. Cleanup failure does not rewrite an already persisted business outcome.
- The example Runner executes only a constrained synthetic Todo workflow with network disabled. It does not execute arbitrary caller-supplied source code.
- Docker access gives the trusted Sandbox controller powerful host privileges. This release is for private trusted deployments, not a hardened public hostile-code service.
- No K8s, Redis, Kafka, separate Data Pool or internal-company connectors are required.

Stop services with `docker compose down`. Do not add `--volumes` unless intentionally deleting local development data. Supabase data is not deleted by Compose.
