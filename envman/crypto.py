"""
Encryption and decryption utilities using AES-256-GCM
"""
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypto:
    """Handle encryption and decryption of environment variables"""
    
    def __init__(self, master_password: str):
        """Initialize with master password"""
        self.master_password = master_password
    
    def _derive_key(self, salt: bytes) -> bytes:
        """Derive encryption key from master password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(self.master_password.encode())
    
    def encrypt(self, data: str) -> str:
        """Encrypt data and return base64 encoded string"""
        # Generate random salt and nonce
        salt = os.urandom(16)
        nonce = os.urandom(12)
        
        # Derive key from password
        key = self._derive_key(salt)
        
        # Encrypt data
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data.encode(), None)
        
        # Combine salt + nonce + ciphertext and encode
        encrypted = salt + nonce + ciphertext
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt base64 encoded encrypted data"""
        # Decode from base64
        encrypted = base64.b64decode(encrypted_data.encode())
        
        # Extract salt, nonce, and ciphertext
        salt = encrypted[:16]
        nonce = encrypted[16:28]
        ciphertext = encrypted[28:]
        
        # Derive key from password
        key = self._derive_key(salt)
        
        # Decrypt data
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode()
