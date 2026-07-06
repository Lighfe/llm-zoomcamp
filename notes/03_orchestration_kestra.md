# Setup
- I created the different API_KEYS as suggested but saved them in codespace secrets
- Using setup-secrets.sh to have secrets available for kestra (base64)
- Kestra uses a postgres database which it uses to storing tis data
# structure
- systemMessage
- prompt
- provider
- tools
- memory

## Agent Tools Available in Kestra

| Tool | Purpose | Example Use |
|------|---------|-------------|
| `TavilyWebSearch` | Search the web for current information | Market research, news monitoring |
| `GoogleCustomWebSearch` | Search with Google Custom Search API | Google search |
| `CodeExecution` | Run code safely via Judge0 | Math calculations, data validation |
| `KestraTask` | Execute any Kestra task | Run tasks based on 1000+ Kestra plugins |
| `KestraFlow` | Trigger other Kestra flows | Call other flows for modularity |
| `StreamableHttpMcpClient` | Use MCP servers via HTTP/SSE | Connect to remote MCP servers |
| `DockerMcpClient` | Use MCP servers in Docker | MCP servers spun up on-demand via Docker |
| `StdioMcpClient` | Use MCP servers via stdio | Integration with external systems |
| `AIAgent` | Use another agent as a tool | Multi-agent systems, specialized sub-agents 


# When to Use AI Agents

- Use AI Agents when the exact sequence of steps isn't known in advance, decisions depend on dynamic changing information, or you need to adapt to unexpected conditions.
- Use traditional workflows when steps are deterministic and repeatable, compliance requires exact auditable processes, or cost and latency must be minimized.