CREATE TABLE IF NOT EXISTS public.sdlc_workspaces (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 owner_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
 title text NOT NULL CHECK (length(title) BETWEEN 1 AND 80),
 requirement text NOT NULL CHECK (length(requirement) BETWEEN 1 AND 8000),
 source_hash text NOT NULL,
 automation_run_id uuid,
 created_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.sdlc_workspaces ENABLE ROW LEVEL SECURITY;
CREATE POLICY sdlc_workspace_select ON public.sdlc_workspaces FOR SELECT TO authenticated USING ((select auth.uid())=owner_id);
CREATE POLICY sdlc_workspace_update ON public.sdlc_workspaces FOR UPDATE TO authenticated USING ((select auth.uid())=owner_id) WITH CHECK ((select auth.uid())=owner_id);
REVOKE INSERT, UPDATE, DELETE ON public.sdlc_workspaces FROM anon, authenticated;
GRANT SELECT ON public.sdlc_workspaces TO authenticated;
GRANT UPDATE(automation_run_id) ON public.sdlc_workspaces TO authenticated;
CREATE INDEX IF NOT EXISTS sdlc_workspaces_owner ON public.sdlc_workspaces(owner_id,created_at DESC);
INSERT INTO storage.buckets(id,name,public) VALUES
 ('sandbox-gateway-artifacts','sandbox-gateway-artifacts',false),
 ('automation-platform-artifacts','automation-platform-artifacts',false)
ON CONFLICT(id) DO NOTHING;
