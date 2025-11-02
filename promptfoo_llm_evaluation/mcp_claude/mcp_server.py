#!/usr/bin/env python3
"""
MCP Server for Promptfoo Integration
Simple Python-based MCP server that provides tools for promptfoo evaluation
"""

import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Any

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# Create server instance
server = Server("promptfoo-mcp-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for promptfoo integration."""
    return [
        types.Tool(
            name="promptfoo_init",
            description="Initialize a new promptfoo project in the specified directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path where promptfoo should be initialized"
                    },
                    "provider": {
                        "type": "string", 
                        "description": "AI provider to configure (e.g., 'openai', 'anthropic')",
                        "default": "openai"
                    }
                },
                "required": ["directory"]
            }
        ),
        types.Tool(
            name="promptfoo_eval",
            description="Run promptfoo evaluation with the current configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory containing promptfoo configuration"
                    },
                    "config": {
                        "type": "string",
                        "description": "Path to specific config file (optional)"
                    }
                },
                "required": ["directory"]
            }
        ),
        types.Tool(
            name="promptfoo_view",
            description="View promptfoo evaluation results",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory containing evaluation results"
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format: 'table', 'json', or 'csv'",
                        "enum": ["table", "json", "csv"],
                        "default": "table"
                    }
                },
                "required": ["directory"]
            }
        ),
        types.Tool(
            name="promptfoo_list",
            description="List available promptfoo configurations and results",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to search for promptfoo files"
                    }
                },
                "required": ["directory"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle tool calls for promptfoo operations."""
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "promptfoo_init":
            return await init_promptfoo(arguments)
        elif name == "promptfoo_eval":
            return await run_evaluation(arguments)
        elif name == "promptfoo_view":
            return await view_results(arguments)
        elif name == "promptfoo_list":
            return await list_configs(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def run_command(cmd: list[str], cwd: str = None) -> tuple[str, str, int]:
    """Run a shell command and return stdout, stderr, and return code."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode(), process.returncode
    except Exception as e:
        return "", str(e), 1


async def init_promptfoo(args: dict) -> list[types.TextContent]:
    """Initialize promptfoo in a directory."""
    directory = args.get("directory", ".")
    provider = args.get("provider", "openai")
    
    # Create directory if it doesn't exist
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Check if already initialized
    config_path = Path(directory) / "promptfooconfig.yaml"
    if config_path.exists():
        return [types.TextContent(
            type="text",
            text=f"✅ Promptfoo already initialized in {directory}"
        )]
    
    # Create basic configuration
    config_content = f"""# Promptfoo Configuration
description: "AI evaluation setup"

providers:
  - {provider}:gpt-4

prompts:
  - "You are a helpful assistant. {{{{question}}}}"

tests:
  - vars:
      question: "What is the capital of France?"
    assert:
      - type: contains
        value: "Paris"
      - type: contains-not
        value: "London"

outputPath: "./output"
"""
    
    try:
        # Write config file
        with open(config_path, "w") as f:
            f.write(config_content)
        
        # Run promptfoo init
        stdout, stderr, code = await run_command(
            ["npx", "promptfoo", "init", "--no-interactive"], 
            cwd=directory
        )
        
        if code == 0:
            return [types.TextContent(
                type="text",
                text=f"🚀 Successfully initialized promptfoo in {directory}\\n\\nConfig created at: {config_path}\\n\\nOutput:\\n{stdout}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"⚠️ Promptfoo init completed with warnings:\\n{stderr}\\n\\nConfig still created at: {config_path}"
            )]
            
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error initializing promptfoo: {str(e)}"
        )]


async def run_evaluation(args: dict) -> list[types.TextContent]:
    """Run promptfoo evaluation."""
    directory = args.get("directory", ".")
    config_file = args.get("config")
    
    cmd = ["npx", "promptfoo", "eval"]
    if config_file:
        cmd.extend(["-c", config_file])
    
    stdout, stderr, code = await run_command(cmd, cwd=directory)
    
    if code == 0:
        return [types.TextContent(
            type="text",
            text=f"✅ Evaluation completed successfully!\\n\\n{stdout}"
        )]
    else:
        return [types.TextContent(
            type="text",
            text=f"❌ Evaluation failed:\\n{stderr}\\n\\nOutput:\\n{stdout}"
        )]


async def view_results(args: dict) -> list[types.TextContent]:
    """View evaluation results."""
    directory = args.get("directory", ".")
    format_type = args.get("format", "table")
    
    if format_type == "json":
        cmd = ["npx", "promptfoo", "view", "--format", "json"]
    elif format_type == "csv": 
        cmd = ["npx", "promptfoo", "view", "--format", "csv"]
    else:
        cmd = ["npx", "promptfoo", "view"]
    
    stdout, stderr, code = await run_command(cmd, cwd=directory)
    
    if code == 0:
        return [types.TextContent(
            type="text",
            text=f"📊 Evaluation Results ({format_type}):\\n\\n{stdout}"
        )]
    else:
        return [types.TextContent(
            type="text",
            text=f"❌ Could not view results:\\n{stderr}"
        )]


async def list_configs(args: dict) -> list[types.TextContent]:
    """List promptfoo configurations and results."""
    directory = args.get("directory", ".")
    
    try:
        path = Path(directory)
        files_found = []
        
        # Look for config files
        for pattern in ["promptfooconfig.*", "*.promptfoo.*"]:
            files_found.extend(path.glob(pattern))
        
        # Look for output directories
        output_dirs = [d for d in path.iterdir() if d.is_dir() and "output" in d.name.lower()]
        
        result = f"📁 Promptfoo files in {directory}:\\n\\n"
        
        if files_found:
            result += "📄 Configuration files:\\n"
            for f in files_found:
                result += f"  - {f.name}\\n"
        
        if output_dirs:
            result += "\\n📊 Output directories:\\n"
            for d in output_dirs:
                result += f"  - {d.name}/\\n"
        
        if not files_found and not output_dirs:
            result += "❌ No promptfoo files found. Try running promptfoo_init first."
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error listing files: {str(e)}"
        )]


async def main():
    """Main entry point for the MCP server."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="promptfoo-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())