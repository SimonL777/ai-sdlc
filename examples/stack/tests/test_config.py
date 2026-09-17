import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('check_config',Path(__file__).resolve().parents[1]/'check_config.py')
config=importlib.util.module_from_spec(spec);spec.loader.exec_module(config)

def production():
 d={'API_TOKEN':'operator-'+'x'*32,'SANDBOX_SERVICE_TOKEN':'sandbox-'+'x'*32,'MODEL_SERVICE_TOKEN':'model-'+'x'*32,'AUTOMATION_SERVICE_TOKEN':'automation-'+'x'*32,'DOCKER_GID':'999','ARTIFACT_MODE':'supabase','MODEL_MODE':'mock','AI_SDLC_SUPABASE_URL':'https://studio-project.supabase.co'}
 for prefix in ['SANDBOX','MODEL','AUTOMATION']:
  d.update({prefix+'_DATABASE_URL':f'jdbc:postgresql://db.{prefix.lower()}.supabase.co:5432/postgres?sslmode=require',prefix+'_DATABASE_USER':'postgres',prefix+'_DATABASE_PASSWORD':'synthetic-test-value',prefix+'_SUPABASE_URL':f'https://{prefix.lower()}-project.supabase.co'})
 for prefix in ['SANDBOX','AUTOMATION']:d[prefix+'_SUPABASE_SERVICE_ROLE_KEY']=prefix+'-synthetic-secret'
 return d

class ConfigTests(unittest.TestCase):
 def test_four_independent_projects_are_valid_without_model_storage_key(self):self.assertEqual([],config.validate(production()))
 def test_shared_project_is_rejected(self):
  d=production();d['MODEL_SUPABASE_URL']=d['SANDBOX_SUPABASE_URL'];self.assertTrue(any('four distinct' in x for x in config.validate(d)))
 def test_shared_database_identity_is_rejected(self):
  d=production();d['MODEL_DATABASE_URL']=d['SANDBOX_DATABASE_URL'];self.assertTrue(any('database connection' in x for x in config.validate(d)))
 def test_private_values_never_appear_in_diagnostics(self):
  d=production();d['AUTOMATION_SUPABASE_SERVICE_ROLE_KEY']=d['SANDBOX_SUPABASE_SERVICE_ROLE_KEY'];errors=' '.join(config.validate(d));self.assertNotIn(d['SANDBOX_SUPABASE_SERVICE_ROLE_KEY'],errors);self.assertIn('service-role',errors)
 def test_explicit_local_mode_does_not_require_cloud_projects(self):
  d=production();d={k:v for k,v in d.items() if k in ['API_TOKEN','SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN','DOCKER_GID']};d['SPRING_PROFILES_ACTIVE']='local';d['ARTIFACT_MODE']='local';self.assertEqual([],config.validate(d))

class TwoProjectDemoTests(unittest.TestCase):
 def demo(self):
  d=production();d['SUPABASE_LAYOUT']='two-project-demo'
  d['MODEL_SUPABASE_URL']=d['SANDBOX_SUPABASE_URL']
  d['MODEL_DATABASE_URL']=d['SANDBOX_DATABASE_URL']
  d['AI_SDLC_SUPABASE_URL']=d['AUTOMATION_SUPABASE_URL']
  return d
 def test_resource_sharing_is_explicit_and_supported(self):self.assertEqual([],config.validate(self.demo()))
 def test_one_project_for_everything_is_rejected(self):
  d=self.demo();d['AI_SDLC_SUPABASE_URL']=d['AUTOMATION_SUPABASE_URL']=d['SANDBOX_SUPABASE_URL'];self.assertTrue(any('Two-project demo' in x for x in config.validate(d)))
 def test_demo_config_does_not_weaken_independent_default(self):
  d=self.demo();del d['SUPABASE_LAYOUT'];self.assertTrue(any('four distinct' in x for x in config.validate(d)))
 def test_wrong_group_mapping_is_rejected(self):
  d=self.demo();d['MODEL_SUPABASE_URL']=d['AUTOMATION_SUPABASE_URL'];self.assertTrue(any('Two-project demo' in x for x in config.validate(d)))
 def test_data_connection_cannot_cross_resource_groups(self):
  d=self.demo();d['AUTOMATION_DATABASE_URL']=d['SANDBOX_DATABASE_URL'];self.assertTrue(any('connection identity' in x for x in config.validate(d)))
 def test_unknown_layout_is_rejected(self):
  d=self.demo();d['SUPABASE_LAYOUT']='unrestricted';self.assertIn('Unknown SUPABASE_LAYOUT',config.validate(d))

if __name__=='__main__':unittest.main()
