#!/usr/bin/env python3
"""
FastMCP Server for Promptfoo Integration
Compatible with mcp dev command for inspection
"""

import subprocess
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("promptfoo-fastmcp-server")


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


@mcp.tool()
async def promptfoo_init(directory: str, provider: str = "openai") -> str:
    """Initialize promptfoo in a directory."""
    
    # Create directory if it doesn't exist
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Check if already initialized
    config_path = Path(directory) / "promptfooconfig.yaml"
    if config_path.exists():
        return f"✅ Promptfoo already initialized in {directory}"
    
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
            return f"🚀 Successfully initialized promptfoo in {directory}\n\nConfig created at: {config_path}\n\nOutput:\n{stdout}"
        else:
            return f"⚠️ Promptfoo init completed with warnings:\n{stderr}\n\nConfig still created at: {config_path}"
            
    except Exception as e:
        return f"❌ Error initializing promptfoo: {str(e)}"


@mcp.tool()
async def promptfoo_eval(directory: str, config: str = None) -> str:
    """Run promptfoo evaluation."""
    
    cmd = ["npx", "promptfoo", "eval"]
    if config:
        cmd.extend(["-c", config])
    
    stdout, stderr, code = await run_command(cmd, cwd=directory)
    
    if code == 0:
        return f"✅ Evaluation completed successfully!\n\n{stdout}"
    else:
        return f"❌ Evaluation failed:\n{stderr}\n\nOutput:\n{stdout}"


@mcp.tool()
async def promptfoo_view(directory: str, format: str = "table") -> str:
    """View evaluation results."""
    
    if format == "json":
        cmd = ["npx", "promptfoo", "view", "--format", "json"]
    elif format == "csv": 
        cmd = ["npx", "promptfoo", "view", "--format", "csv"]
    else:
        cmd = ["npx", "promptfoo", "view"]
    
    stdout, stderr, code = await run_command(cmd, cwd=directory)
    
    if code == 0:
        return f"📊 Evaluation Results ({format}):\n\n{stdout}"
    else:
        return f"❌ Could not view results:\n{stderr}"


@mcp.tool()
async def promptfoo_list(directory: str) -> str:
    """List promptfoo configurations and results."""
    
    try:
        path = Path(directory)
        files_found = []
        
        # Look for config files
        for pattern in ["promptfooconfig.*", "*.promptfoo.*"]:
            files_found.extend(path.glob(pattern))
        
        # Look for output directories
        output_dirs = [d for d in path.iterdir() if d.is_dir() and "output" in d.name.lower()]
        
        result = f"📁 Promptfoo files in {directory}:\n\n"
        
        if files_found:
            result += "📄 Configuration files:\n"
            for f in files_found:
                result += f"  - {f.name}\n"
        
        if output_dirs:
            result += "\n📊 Output directories:\n"
            for d in output_dirs:
                result += f"  - {d.name}/\n"
        
        if not files_found and not output_dirs:
            result += "❌ No promptfoo files found. Try running promptfoo_init first."
        
        return result
        
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"


if __name__ == "__main__":
    import sys
    import json
    import logging
    
    # Set up logging to suppress noise
    logging.basicConfig(level=logging.WARNING)
    
    # Run the server
    try:
        mcp.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)