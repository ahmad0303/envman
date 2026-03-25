"""
Core business logic for EnvMan
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from .storage import Storage
from .crypto import Crypto


class EnvManager:
    """Main environment manager class"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize environment manager"""
        if config_dir is None:
            config_dir = Path.home() / ".envman"
        
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = config_dir / "envman.db"
        self.storage = Storage(self.db_path)
        self._crypto = None
    
    def _get_crypto(self) -> Crypto:
        """Get or create crypto instance"""
        if self._crypto is None:
            password = self.storage.get_config("master_password_hash")
            if not password:
                raise ValueError("EnvMan not initialized. Run 'envman init' first.")
            self._crypto = Crypto(password)
        return self._crypto
    
    def init(self, master_password: str):
        """Initialize EnvMan with master password"""
        # Store password hash for future use
        self.storage.set_config("master_password_hash", master_password)
        self._crypto = Crypto(master_password)
        print("✓ EnvMan initialized successfully!")
    
    def add_environment(self, name: str, description: str = ""):
        """Add a new environment"""
        try:
            env_id = self.storage.create_environment(name, description)
            print(f"✓ Environment '{name}' created successfully!")
            return env_id
        except Exception as e:
            raise ValueError(f"Failed to create environment: {e}")
    
    def list_environments(self) -> List[Dict]:
        """List all environments"""
        return self.storage.list_environments()
    
    def load_from_file(self, environment_name: str, filepath: Path):
        """Load variables from .env file into environment"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        crypto = self._get_crypto()
        count = 0
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    encrypted_value = crypto.encrypt(value)
                    self.storage.set_variable(env['id'], key, encrypted_value)
                    count += 1
        
        print(f"✓ Loaded {count} variables into '{environment_name}'")
    
    def export_to_file(self, environment_name: str, filepath: Path):
        """Export environment variables to .env file"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        crypto = self._get_crypto()
        variables = self.storage.get_variables(env['id'])
        
        with open(filepath, 'w') as f:
            f.write(f"# Environment: {environment_name}\n")
            f.write(f"# Exported at: {env['updated_at']}\n\n")
            
            for key, encrypted_value in sorted(variables.items()):
                value = crypto.decrypt(encrypted_value)
                f.write(f"{key}={value}\n")
        
        print(f"✓ Exported {len(variables)} variables to {filepath}")
    
    def use_environment(self, environment_name: str):
        """Switch to an environment (export to .env)"""
        current_dir = Path.cwd()
        env_file = current_dir / ".env"
        self.export_to_file(environment_name, env_file)
        print(f"✓ Now using '{environment_name}' environment")
    
    def set_variable(self, environment_name: str, key: str, value: str):
        """Set a single variable in an environment"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        crypto = self._get_crypto()
        encrypted_value = crypto.encrypt(value)
        self.storage.set_variable(env['id'], key, encrypted_value)
        print(f"✓ Set {key} in '{environment_name}'")
    
    def get_variables(self, environment_name: str) -> Dict[str, str]:
        """Get all variables from an environment (decrypted)"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        crypto = self._get_crypto()
        encrypted_vars = self.storage.get_variables(env['id'])
        
        return {
            key: crypto.decrypt(value)
            for key, value in encrypted_vars.items()
        }
    
    def backup_environment(self, environment_name: str):
        """Create a backup of an environment"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        variables = self.storage.get_variables(env['id'])
        backup_data = {
            'environment': environment_name,
            'variables': variables
        }
        
        backup_id = self.storage.create_backup(env['id'], backup_data)
        print(f"✓ Backup created (ID: {backup_id})")
        return backup_id
    
    def diff_environments(self, env1_name: str, env2_name: str) -> Dict:
        """Compare two environments and show differences"""
        vars1 = self.get_variables(env1_name)
        vars2 = self.get_variables(env2_name)
        
        all_keys = set(vars1.keys()) | set(vars2.keys())
        
        differences = {
            'only_in_first': {},
            'only_in_second': {},
            'different_values': {},
            'same': {}
        }
        
        for key in all_keys:
            if key not in vars1:
                differences['only_in_second'][key] = vars2[key]
            elif key not in vars2:
                differences['only_in_first'][key] = vars1[key]
            elif vars1[key] != vars2[key]:
                differences['different_values'][key] = {
                    'first': vars1[key],
                    'second': vars2[key]
                }
            else:
                differences['same'][key] = vars1[key]
        
        return differences
    
    def export_for_sharing(self, environment_name: str, output_path: Path):
        """Export environment in encrypted format for sharing"""
        env = self.storage.get_environment(environment_name)
        if not env:
            raise ValueError(f"Environment '{environment_name}' not found")
        
        variables = self.storage.get_variables(env['id'])
        
        export_data = {
            'environment': environment_name,
            'description': env.get('description', ''),
            'variables': variables,
            'version': '1.0'
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Environment exported to {output_path}")
        print(f"  Share this file with your team (already encrypted)")
    
    def import_from_share(self, input_path: Path, environment_name: Optional[str] = None):
        """Import shared environment"""
        with open(input_path, 'r') as f:
            import_data = json.load(f)
        
        env_name = environment_name or import_data['environment']
        
        # Create or get environment
        env = self.storage.get_environment(env_name)
        if not env:
            env_id = self.add_environment(env_name, import_data.get('description', ''))
            env = self.storage.get_environment(env_name)
        
        # Import variables (already encrypted)
        for key, encrypted_value in import_data['variables'].items():
            self.storage.set_variable(env['id'], key, encrypted_value)
        
        print(f"✓ Imported {len(import_data['variables'])} variables into '{env_name}'")
    
    def close(self):
        """Close storage connection"""
        self.storage.close()
