# Security Keys Directory

This directory is used to store security-related keys and certificates for the AI Plastic Recycling system. 

## Expected Contents

1. `ssl/` - SSL/TLS certificates for secure communication
   - `server.crt` - Server certificate
   - `server.key` - Server private key
   - `ca.crt` - Certificate Authority certificate

2. `jwt/` - JWT signing keys
   - `private.pem` - Private key for JWT signing
   - `public.pem` - Public key for JWT verification

3. `robot/` - Robot communication certificates
   - `robot_client.crt` - Robot client certificate
   - `robot_client.key` - Robot client private key

## Security Notice

⚠️ **IMPORTANT**: Never commit any keys or certificates to version control!
- All files in this directory (except this README and .gitignore) are ignored by git
- Store production keys securely and distribute them through secure channels
- Use environment variables or secure secret management systems in production

## Key Generation

For development purposes, you can generate self-signed certificates using:

```bash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/server.key -out ssl/server.crt

# Generate JWT keys
openssl genrsa -out jwt/private.pem 2048
openssl rsa -in jwt/private.pem -pubout -out jwt/public.pem

# Generate robot certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout robot/robot_client.key -out robot/robot_client.crt
``` 