# Cloudflare Tunnel Setup Guide

This guide explains how to expose your local Scene Generator API to the internet securely using Cloudflare Tunnel.

## Why Cloudflare Tunnel?

Cloudflare Tunnel creates a secure, encrypted tunnel between your local machine and Cloudflare's edge network without requiring you to open ports on your firewall or set up complex network configurations.

## Prerequisites

1. A Cloudflare account (free tier is sufficient)
2. The `cloudflared` CLI tool installed on your machine

## Installation

### macOS

Install using Homebrew:
```bash
brew install cloudflared
```

### Windows

Download the installer from:
https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install/windows/

### Linux

Download the appropriate package for your distribution from:
https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install/linux/

## Setup Process

### 1. Authenticate with Cloudflare

```bash
cloudflared login
```

This command will open a browser window asking you to log in to your Cloudflare account and authorize the cloudflared application.

### 2. Start a Quick Tunnel (Temporary)

For testing or temporary use:

```bash
cloudflared tunnel --url http://localhost:8000
```

This will output a URL like `https://your-tunnel-id.trycloudflare.com` that you can use to access your API.

### 3. Create a Named Tunnel (Persistent, Optional)

For a more permanent solution:

```bash
# Create a tunnel
cloudflared tunnel create scene-generator

# Configure the tunnel (replace UUID with your tunnel ID)
cloudflared tunnel route dns <UUID> scene-generator.yourdomain.com

# Create a config file
cat > ~/.cloudflared/config.yml << EOF
tunnel: <UUID>
credentials-file: /Users/username/.cloudflared/<UUID>.json
ingress:
  - hostname: scene-generator.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
EOF

# Run the tunnel
cloudflared tunnel run
```

## Updating the OpenAPI Specification

Once you have your tunnel URL, update the `servers.url` field in your `openapi.yaml` file:

```yaml
servers:
  - url: https://your-tunnel-id.trycloudflare.com
```

## Checking Tunnel Status

```bash
# For named tunnels
cloudflared tunnel list

# For active tunnels
cloudflared tunnel info
```

## Stopping the Tunnel

For a quick tunnel, press `Ctrl+C` in the terminal where it's running.

For a named tunnel running in the background:

```bash
cloudflared tunnel stop <tunnel-name-or-id>
```

## Troubleshooting

### Connection Issues

If you're having trouble connecting to your tunnel:

1. Check that your API is running locally and accessible at http://localhost:8000
2. Verify that cloudflared is running without errors
3. Check your firewall settings to ensure cloudflared can establish outbound connections

### Certificate Errors

If you see certificate errors:

```bash
cloudflared certificate install
```

### Permissions Issues

On Linux/macOS, if you encounter permissions issues:

```bash
sudo chmod +x /usr/local/bin/cloudflared
```

## Additional Resources

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cloudflare Zero Trust Dashboard](https://dash.teams.cloudflare.com/) 