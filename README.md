# AI-SDLC

[![CI](https://github.com/SimonL777/ai-sdlc/actions/workflows/ci.yml/badge.svg)](https://github.com/SimonL777/ai-sdlc/actions/workflows/ci.yml)

[sandbox-gateway](https://github.com/SimonL777/sandbox-gateway) · [model-gateway](https://github.com/SimonL777/model-gateway) · [automation-platform](https://github.com/SimonL777/automation-platform) · [ai-sdlc](https://github.com/SimonL777/ai-sdlc)

A small React workbench that connects three independent Java services into a demonstrable delivery loop.

```text
Requirement / material
  → Model Gateway: structured Workflow
  → Automation Platform: validation + deterministic compilation
  → Sandbox Gateway: Docker / Playwright execution
  → report and provenance in the workbench
```

## Four repositories

Keep these as siblings for the integration example:

- `sandbox-gateway`: execution control and Docker resource lifecycle.
- `model-gateway`: model requests, provider credentials, SSE and audit.
- `automation-platform`: durable runs, Git snapshots, Workflow compiler and test delivery.
- `ai-sdlc`: user interface, Supabase Workspace RPC with optional Edge transport and integration deployment.

Each repository has its own build, API/configuration and migration lifecycle. The integrated deployment keeps them as siblings.

## Current implementation

- Requirement input, optional registered Git ref, asynchronous execution list, cancellation, report, artifact downloads and provenance.
- Model mode is visible. Mock generation is not presented as a real LLM evaluation.
- Private operator-token login and optional Supabase email login.
- The browser calls Java APIs through the NAS's same-origin reverse proxy; no cloud Edge Function must reach a private NAS IP.
- Independent project configuration supports four Supabase resources or an explicit two-project NAS demo. Schemas and buckets stay service-owned; AI-SDLC Auth provides a common verified identity. Its Workspace Edge API stores immutable material snapshots. Shared demo resources are logical separation, not four physical security boundaries.
- A four-service Docker Compose example plus an on-demand Playwright Runner image.

Validated on 2026-09-18: frontend tests (4), deployment configuration tests (11), production build, browser login-page rendering, real Supabase Workspace/Auth/Storage, and the authenticated Docker execution/report chain. Model generation is explicitly mock. Real-provider validation remains pending.

## Get the complete demo

```bash
mkdir ai-sdlc-demo && cd ai-sdlc-demo
git clone https://github.com/SimonL777/sandbox-gateway.git
git clone https://github.com/SimonL777/model-gateway.git
git clone https://github.com/SimonL777/automation-platform.git
git clone https://github.com/SimonL777/ai-sdlc.git
cd ai-sdlc/examples/stack
```

Continue with [the deployment guide](examples/stack/README.md). For the validated two-resource demo, use `setup_env.py --layout two-project-demo`; each repository also supports independent Supabase resources. Never copy private credentials into source files.

## Development

Node 22.12+:

```bash
npm ci
npm run dev
```

Start the three Java services separately on localhost 8081, 8082 and 8083. Vite proxies the API paths. Set public Supabase configuration in a local `public/config.js` if testing account login; never put a service-role key or provider key there. The image generates `config.js` from public-only environment variables at startup.

The operator token is entered at login and kept only in session storage. Supabase login uses the Supabase session; Java services must have issuer/JWKS/audience verification configured. Do not expose this workbench publicly without HTTPS and appropriate access controls.

## NAS deployment

See [examples/stack/README.md](examples/stack/README.md). This is the single integration recipe; each Java repository also builds and tests independently. Production configuration uses Supabase; H2/local artifacts require an explicit development profile.

## Supabase Workspace function

Apply both Workspace migrations in order: `202609180001_workspaces.sql` and `202609180002_workspace_rpc.sql`. The default `rpc` transport works through authenticated Supabase PostgREST and requires no management API token. To use the optional `edge` transport, deploy:

```bash
supabase functions deploy ai-sdlc-workspaces --project-ref YOUR_PROJECT_REF --no-verify-jwt
```

Set `AI_SDLC_WORKSPACE_TRANSPORT=edge` only after deploying the optional function. The function itself verifies the user with Supabase Auth. `--no-verify-jwt` does not make its application API anonymous. Material creation uses the server-side service role only after identity verification; user table grants cannot update the material. Run attachment uses the user's JWT and RLS. A run reference is metadata and never an authorization credential.

Operator mode persists the original requirement in the automation task. The separate Workspace table is used with Supabase account login; these modes are shown explicitly.

## Tests and acceptance

```bash
npm test
npm run build
```

NAS acceptance scripts:

```bash
cd examples/stack
python3 smoke.py
python3 smoke.py --negative
```

The smoke script checks the real task result, idempotency, compiler hash, Docker execution and container cleanup. It prints provider mode so synthetic and actual-model evidence remain distinct.

## Scope

A compact interview/open-source demonstration, not a full enterprise AI-SDLC suite. Complete AICR, defect detection, external Wiki/EC connectors, complex knowledge retrieval, Data Pool, K8s and message-broker infrastructure are outside v0.1. See each service's README for execution and security boundaries.

Apache-2.0. Only original implementation and synthetic data are included.
