# Four-repository NAS deployment

The two-project layout has been deployed and exercised on a Linux Docker host. Positive, deliberate failure, authenticated Workspace linkage, private Storage download and cleanup checks passed. Model generation remains mock; real-provider acceptance is separate. See the repository validation status for the exact scope.

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

## Independent projects and two-project NAS demo

Every repository keeps its own database configuration and migrations. The default `SUPABASE_LAYOUT=independent` supports four separate Supabase projects. The NAS demo may explicitly select `two-project-demo` when only two cloud projects are available:

| Project | Data and migrations | Private configuration |
|---|---|---|
| Sandbox Gateway | Flyway execution schema; `sandbox-gateway/supabase/migrations/202609180001_artifact_bucket.sql` creates its private bucket | `SANDBOX_DATABASE_*`, `SANDBOX_SUPABASE_URL`, `SANDBOX_SUPABASE_SERVICE_ROLE_KEY` |
| Model Gateway | Flyway request/audit schema; no artifact bucket or service-role key needed | `MODEL_DATABASE_*`, `MODEL_SUPABASE_URL` (deployment identity) |
| Automation Platform | Flyway workflow/run schema; `automation-platform/supabase/migrations/202609180001_artifact_bucket.sql` creates its private bucket | `AUTOMATION_DATABASE_*`, `AUTOMATION_SUPABASE_URL`, `AUTOMATION_SUPABASE_SERVICE_ROLE_KEY` |
| AI-SDLC | Apply both Workspace SQL migrations in filename order; default RPC is ready after SQL. Edge transport is optional | `AI_SDLC_SUPABASE_URL`, `AI_SDLC_SUPABASE_ANON_KEY`; its service-role key stays in its own Edge environment |

### Two-project demo mapping

- **Project A / infrastructure**: Sandbox Gateway (`sandbox_gateway` schema + its private bucket) and Model Gateway (`model_gateway` schema, no Storage key).
- **Project B / applications**: Automation Platform (`automation_platform` schema + its bucket) and AI-SDLC (`public.sdlc_workspaces`, Auth and its Edge Function).

Use `python3 setup_env.py --layout two-project-demo` for a new private configuration. Keep all four variable groups: repeat project A's endpoints for Sandbox/Model and project B's endpoints for Automation/AI-SDLC. Each repository still runs and migrates independently. Moving to four resources later only changes connection settings and requires a deliberate data migration; no source coupling is introduced.

Schemas and buckets provide logical organization in this demo. A shared database administrator or Supabase service-role key can have access across its physical project; this is not four independent privilege boundaries. Use separate database roles with scoped grants for stronger isolation if needed. Privileged keys are never put in the browser or shared between projects A and B.

Apply each service's Supabase SQL **only to its own project**. Java Flyway migrations run against that service's configured JDBC database. Use TLS and an appropriate direct/session-pooler endpoint reachable from the NAS. Database credentials are distinct from API/service-role keys. If choosing transaction pooling, check JDBC prepared-statement compatibility first.

The Compose file maps each prefix into the corresponding container's ordinary `DATABASE_URL` / `SUPABASE_URL` environment variables. No Java service receives another project's service-role key. The checker enforces four distinct resources in independent mode, or the explicit A/B grouping in two-project demo mode. Cross-group connection and service-role-key reuse is rejected.

**Identity can remain unified while data is isolated.** Optional user login is provided by the AI-SDLC project's Auth. Set `AI_SDLC_JWT_ISSUER` and `AI_SDLC_JWKS_URL` to that project's asymmetric JWT configuration; all Java APIs verify this issuer and enforce owner scope, while each service still reads/writes only its own database. Users do not need four separate accounts. Internal service tokens are distinct by receiver and can forward a verified owner ID. No JWT decoding or shared owner header bypasses authentication.

Operator-token mode runs the infrastructure path without Edge deployment. Its input material is persisted in the automation project's database. The separate AI-SDLC Workspace table is exercised only by the Supabase account-login path; verify that path separately before claiming all four cloud projects are integrated.

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

## Runtime acceptance

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

## Low-memory NAS / prebuilt-artifact path

Build each Java JAR with JDK 21/Maven and the workbench with `npm ci && npm run build` on the development machine. Transfer source plus `target/*-0.1.0.jar` and frontend `dist/` to the same sibling layout on the NAS. `Dockerfile.runtime` skips Maven/Node builds on the NAS. Then use:

```bash
docker compose -f compose.yml -f compose.nas.yml --parallel 1 build
docker compose -f compose.yml -f compose.nas.yml --profile build build runner-image
docker compose -f compose.yml -f compose.nas.yml up -d --wait
```

The override sets each Java container to 448 MiB, the workbench to 96 MiB, and the on-demand Runner to 512 MiB. JVM heap is bounded; execute one browser task at a time and observe the host's available memory/swap. These are demo limits, not a production capacity claim. Do not stop unrelated NAS applications to make room without a deliberate operator decision.

## v0.2 product consoles

The same ingress serves four separately built frontends: `/` (AI-SDLC), `/automation/`, `/models/`, `/sandbox/`. Platform switching reuses the same browser session. Each Java repository owns its `frontend/` project and UI Dockerfiles.

Apply the additive Flyway migrations by starting the new service images. These add case revisions and the artifact catalogue, preserving prior jobs. AI-SDLC capabilities are logical Studio tasks executed by the existing Java worker; no fourth JVM or cloud-to-NAS callback is required.

Initialize sample cases with the **载入演示用例** button or `WORKSPACE_TOKEN=... python3 seed-demo.py`. Add `--run` to create real execution records. Seeded input is labeled, and successful/failed runs are never fabricated.

Web tests emit private screenshots; API tests record status, path and bounded response bodies. Every output uses the existing Supabase Storage configuration. No extra S3 credentials or service is needed.
