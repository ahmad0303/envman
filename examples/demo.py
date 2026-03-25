#!/usr/bin/env python3
"""
Example demonstrating EnvMan usage
"""
import tempfile
from pathlib import Path
from envman.core import EnvManager

def demo():
    """Demo of EnvMan features"""
    print(" EnvMan Demo\n")
    
    # Initialize with test directory (cross-platform temp)
    test_dir = Path(tempfile.gettempdir()) / "envman-demo"
    test_dir.mkdir(exist_ok=True)
    
    manager = EnvManager(config_dir=test_dir)
    
    # 1. Initialize
    print("1. Initializing...")
    manager.init("demo-password-123")
    
    # 2. Add environments
    print("\n2. Creating environments...")
    manager.add_environment("development", "Dev environment")
    manager.add_environment("production", "Prod environment")
    
    # 3. Set some variables
    print("\n3. Setting variables...")
    manager.set_variable("development", "DATABASE_URL", "postgres://localhost/dev")
    manager.set_variable("development", "API_KEY", "dev-key-12345")
    manager.set_variable("development", "DEBUG", "true")
    
    manager.set_variable("production", "DATABASE_URL", "postgres://prod-server/db")
    manager.set_variable("production", "API_KEY", "prod-key-67890")
    manager.set_variable("production", "DEBUG", "false")
    
    # 4. List environments
    print("\n4. Listing environments...")
    envs = manager.list_environments()
    for env in envs:
        print(f"   - {env['name']}: {env['description']}")
    
    # 5. Show variables
    print("\n5. Development variables:")
    dev_vars = manager.get_variables("development")
    for key, value in dev_vars.items():
        print(f"   {key} = {value}")
    
    # 6. Diff environments
    print("\n6. Comparing environments...")
    diff = manager.diff_environments("development", "production")
    print(f"   Different values: {len(diff['different_values'])} variables")
    
    # 7. Export
    print("\n7. Exporting to .env file...")
    export_path = test_dir / "exported.env"
    manager.export_to_file("development", export_path)
    print(f"   Exported to: {export_path}")
    
    # 8. Share
    print("\n8. Creating shareable export...")
    share_path = test_dir / "share.json"
    manager.export_for_sharing("development", share_path)
    print(f"   Share file: {share_path}")
    
    # 9. Backup
    print("\n9. Creating backup...")
    backup_id = manager.backup_environment("development")
    print(f"   Backup ID: {backup_id}")
    
    print("\n Demo complete!")
    print(f"\nFiles created in: {test_dir}")
    
    manager.close()


if __name__ == "__main__":
    demo()