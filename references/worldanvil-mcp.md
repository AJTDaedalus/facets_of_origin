# World Anvil MCP Reference

## Key Facts

- The worldanvil-mcp server does **NOT** require an app key (`WA_APP_KEY`). It only needs an auth token via the proxy.
- **Cloudflare bot protection** blocks direct API calls and swagger URLs. Always use the MCP proxy — never attempt direct HTTP requests to the WA API.
- When WA API capabilities are uncertain, **test the endpoint** before claiming it's not possible. The user has pushed back on incorrect assumptions about WA API limitations multiple times.

## Common Pitfalls

| Problem | Cause | Fix |
|---|---|---|
| 401 errors | Wrong or missing auth token | Verify token in MCP config, not app key |
| Connection refused | WSL node path wrong | Use full path to node binary (check `which node` in WSL) |
| "App key required" error | Outdated MCP server version | Update to latest; app key is NOT needed |
| Cloudflare 403 | Direct API call | Route through MCP proxy instead |
| "Endpoint not supported" | Untested assumption | Try the call before rejecting — category assignment, article updates, etc. all work |

## Verification Steps

Before starting WA work in any session:
1. Confirm MCP server is listed and connected (check tool availability)
2. Test with a simple read operation (e.g., list articles)
3. If connection fails, check node path and auth token before re-debugging from scratch

## Working With Articles

- Article creation and updates go through MCP tools, not direct REST
- Category assignment IS supported via the API — do not assume otherwise
- When syncing local docs to WA, diff content before pushing to avoid overwriting newer WA edits
