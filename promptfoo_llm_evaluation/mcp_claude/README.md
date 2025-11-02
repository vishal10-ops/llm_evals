# MCP Promptfoo Server

A simple Python-based MCP (Model Context Protocol) server that integrates Claude Desktop with promptfoo evaluation tools.

## Features

- **promptfoo_init**: Initialize new promptfoo projects
- **promptfoo_eval**: Run evaluations 
- **promptfoo_view**: View evaluation results
- **promptfoo_list**: List configurations and results

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the server:**
   ```bash
   python mcp_client.py
   ```

3. **Run with MCP dev tools:**
   ```bash
   mcp dev mcp_server.py
   ```

4. **Interactive client:**
   ```bash
   python mcp_client.py --interactive
   ```

## Claude Desktop Configuration

Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "promptfoo": {
      "command": "python",
      "args": ["/path/to/mcp_claude/mcp_server.py"],
      "env": {}
    }
  }
}
```

## Usage Examples

```bash
# Initialize promptfoo in a directory
promptfoo_init {"directory": "./my_project", "provider": "openai"}

# Run evaluation
promptfoo_eval {"directory": "./my_project"}

# View results
promptfoo_view {"directory": "./my_project", "format": "table"}

# List configs
promptfoo_list {"directory": "./my_project"}
```

## Requirements

- Python 3.8+
- Node.js (for promptfoo)
- MCP Python SDK