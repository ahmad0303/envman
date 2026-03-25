#!/usr/bin/env python3
"""
Test suite for EnvMan - Run this to verify everything works
"""
import os
import sys
import tempfile
from pathlib import Path
from envman.core import EnvManager
from envman.crypto import Crypto


def test_encryption():
    """Test encryption and decryption"""
    print("Testing encryption...", end=" ")
    
    crypto = Crypto("test-password-123")
    
    # Test basic encryption/decryption
    original = "my-secret-database-url"
    encrypted = crypto.encrypt(original)
    decrypted = crypto.decrypt(encrypted)
    
    assert original == decrypted, "Encryption/decryption failed!"
    assert encrypted != original, "Not actually encrypted!"
    
    # Test that same value encrypts differently (due to random salt/nonce)
    encrypted2 = crypto.encrypt(original)
    assert encrypted != encrypted2, "Encryption not using random salt/nonce!"
    
    # But both decrypt to same value
    assert crypto.decrypt(encrypted2) == original
    
    print("✓")


def test_storage():
    """Test database operations"""
    print("Testing storage...", end=" ")
    
    from envman.storage import Storage
    
    # Use cross-platform temp directory
    test_dir = Path(tempfile.gettempdir()) / "envman-test"
    test_dir.mkdir(exist_ok=True)
    db_path = test_dir / "test.db"
    
    # Clean up if exists
    if db_path.exists():
        db_path.unlink()
    
    storage = Storage(db_path)
    
    # Test creating environment
    env_id = storage.create_environment("test-env", "Test description")
    assert env_id > 0, "Failed to create environment!"
    
    # Test getting environment
    env = storage.get_environment("test-env")
    assert env is not None, "Failed to retrieve environment!"
    assert env['name'] == "test-env"
    
    # Test setting/getting variables
    storage.set_variable(env_id, "TEST_KEY", "encrypted_value_123")
    vars = storage.get_variables(env_id)
    assert vars['TEST_KEY'] == "encrypted_value_123"
    
    # Test backups
    backup_id = storage.create_backup(env_id, {"key": "value"})
    assert backup_id > 0, "Failed to create backup!"
    
    storage.close()
    print("✓")


def test_core():
    """Test core business logic"""
    print("Testing core logic...", end=" ")
    
    # Use cross-platform temp directory
    test_dir = Path(tempfile.gettempdir()) / "envman-test-core"
    test_dir.mkdir(exist_ok=True)
    
    manager = EnvManager(config_dir=test_dir)
    
    # Initialize
    manager.init("test-password-456")
    
    # Add environment
    manager.add_environment("dev", "Development")
    
    # Set variables
    manager.set_variable("dev", "DB_URL", "postgres://localhost/db")
    manager.set_variable("dev", "API_KEY", "secret-key-123")
    
    # Get variables
    vars = manager.get_variables("dev")
    assert vars['DB_URL'] == "postgres://localhost/db"
    assert vars['API_KEY'] == "secret-key-123"
    
    # Test export
    export_path = test_dir / "test.env"
    manager.export_to_file("dev", export_path)
    assert export_path.exists(), "Export file not created!"
    
    # Test load
    manager.add_environment("dev2", "Development 2")
    manager.load_from_file("dev2", export_path)
    vars2 = manager.get_variables("dev2")
    assert vars2['DB_URL'] == vars['DB_URL']
    
    # Test diff
    manager.set_variable("dev2", "NEW_KEY", "new-value")
    diff = manager.diff_environments("dev", "dev2")
    assert "NEW_KEY" in diff['only_in_second']
    
    # Test backup
    backup_id = manager.backup_environment("dev")
    assert backup_id > 0
    
    # Test sharing
    share_path = test_dir / "share.json"
    manager.export_for_sharing("dev", share_path)
    assert share_path.exists()
    
    # Test import
    manager.add_environment("imported", "Imported")
    manager.import_from_share(share_path, "imported")
    imported_vars = manager.get_variables("imported")
    assert imported_vars['DB_URL'] == vars['DB_URL']
    
    manager.close()
    print("✓")


def test_cli():
    """Test CLI commands (basic smoke test)"""
    print("Testing CLI...", end=" ")
    
    # Just test that commands exist and can be imported
    from envman.cli import cli
    assert cli is not None
    
    print("✓")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print(" EnvMan Test Suite")
    print("="*50 + "\n")
    
    try:
        test_encryption()
        test_storage()
        test_core()
        test_cli()
        
        print("\n" + "="*50)
        print(" All tests passed!")
        print("="*50 + "\n")
        
        print("EnvMan is ready to use! Try:")
        print("  envman init")
        print("  envman add production")
        print("  envman --help")
        
        return 0
        
    except AssertionError as e:
        print(f"\n Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())