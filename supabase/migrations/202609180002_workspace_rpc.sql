-- Lightweight default API: no management API token or Edge deployment is required.
-- The existing Edge Function remains an optional transport with the same ownership rules.
CREATE OR REPLACE FUNCTION public.sdlc_create_workspace(p_title text,p_requirement text)
RETURNS SETOF public.sdlc_workspaces
LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE caller uuid := auth.uid();
BEGIN
 IF caller IS NULL THEN RAISE EXCEPTION 'authentication required' USING ERRCODE='42501'; END IF;
 IF p_title IS NULL OR char_length(btrim(p_title))=0 OR char_length(p_title)>80
    OR p_requirement IS NULL OR char_length(btrim(p_requirement))=0 OR char_length(p_requirement)>8000
 THEN RAISE EXCEPTION 'invalid material' USING ERRCODE='22023'; END IF;
 RETURN QUERY INSERT INTO public.sdlc_workspaces(owner_id,title,requirement,source_hash)
 VALUES(caller,p_title,p_requirement,pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(p_requirement,'UTF8')),'hex'))
 RETURNING *;
END;
$$;
REVOKE ALL ON FUNCTION public.sdlc_create_workspace(text,text) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.sdlc_create_workspace(text,text) TO authenticated;
