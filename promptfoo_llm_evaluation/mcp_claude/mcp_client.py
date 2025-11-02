#!/usr/bin/env python3
"""
MCP Client for testing the Promptfoo MCP Server
Simple test client to verify server functionality

Usage Examples:
    # Basic testing (default)
    python3 mcp_client.py
    
    # Interactive mode
    python3 mcp_client.py --interactive
    
    # Class-based client demo
    python3 mcp_client.py --class
    
    # Show help
    python3 mcp_client.py --help

Requirements:
    - mcp package (pip install mcp)
    - promptfoo CLI tool (npm install -g promptfoo)
    - Running mcp_server.py in the same directory
"""

import asyncio
import json
import sys
from contextlib import AsyncExitStack
from typing import Optional, List, Dict, Any
from mcp import ClientSession, StdioServerParameters, stdio_client


async def test_server():
    """Test the MCP server functionality."""
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=None
    )
    
    async with AsyncExitStack() as exit_stack:
        # Connect to server
        streams = await exit_stack.enter_async_context(stdio_client(server_params))
        session = await exit_stack.enter_async_context(ClientSession(*streams))
        
        # Initialize the session
        await session.initialize()
        
        print("🚀 Connected to MCP Promptfoo Server!")
        print("=" * 50)
        
        # List available tools
        print("📋 Available Tools:")
        tools = await session.list_tools()
        for tool in tools.tools:
            print(f"  • {tool.name}: {tool.description}")
        
        print("\n" + "=" * 50)
        
        # Test promptfoo_list tool
        print("🔍 Testing promptfoo_list tool...")
        try:
            result = await session.call_tool("promptfoo_list", {
                "directory": "."
            })
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 50)
        
        # Test promptfoo_init tool  
        print("🚀 Testing promptfoo_init tool...")
        try:
            result = await session.call_tool("promptfoo_init", {
                "directory": "./test_project",
                "provider": "openai"
            })
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 50)
        print("Client test completed!")


async def interactive_client():
    """Interactive client for manual testing."""
    
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=None
    )
    
    async with AsyncExitStack() as exit_stack:
        streams = await exit_stack.enter_async_context(stdio_client(server_params))
        session = await exit_stack.enter_async_context(ClientSession(*streams))
        
        await session.initialize()
        
        print("🤖 Interactive MCP Promptfoo Client")
        print("Type 'help' for available commands, 'quit' to exit")
        print("=" * 50)
        
        # List tools once
        tools = await session.list_tools()
        available_tools = [tool.name for tool in tools.tools]
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command.lower() == 'help':
                    print("\n📋 Available commands:")
                    print("  • help - Show this help")
                    print("  • tools - List available tools")
                    print("  • quit - Exit the client")
                    print("\n🔧 Available MCP tools:")
                    for tool in tools.tools:
                        print(f"  • {tool.name} - {tool.description}")
                    print("\n💡 Usage: <tool_name> <json_args>")
                    print('   Example: promptfoo_list {"directory": "."}')
                
                elif command.lower() == 'tools':
                    print("\n🔧 Available tools:")
                    for tool in tools.tools:
                        print(f"  • {tool.name}: {tool.description}")
                
                elif ' ' in command:
                    # Parse tool call
                    parts = command.split(' ', 1)
                    tool_name = parts[0]
                    args_str = parts[1]
                    
                    if tool_name in available_tools:
                        try:
                            args = json.loads(args_str)
                            print(f"🔄 Calling {tool_name}...")
                            result = await session.call_tool(tool_name, args)
                            print("\n📄 Result:")
                            for content in result.content:
                                if hasattr(content, 'text'):
                                    print(content.text)
                        except json.JSONDecodeError:
                            print("❌ Invalid JSON arguments")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    else:
                        print(f"❌ Unknown tool: {tool_name}")
                
                else:
                    print("❌ Invalid command. Type 'help' for usage.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


class MCPPromptfooClient:
    """Enhanced MCP client class for better code organization."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack: Optional[AsyncExitStack] = None
        self.tools: Optional[List[Any]] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def connect(self) -> None:
        """Connect to the MCP server."""
        server_params = StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
            env=None
        )
        
        self.exit_stack = AsyncExitStack()
        streams = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(*streams))
        await self.session.initialize()
        
        # Cache available tools
        tools_result = await self.session.list_tools()
        self.tools = tools_result.tools
    
    async def close(self) -> None:
        """Close the connection."""
        if self.exit_stack:
            await self.exit_stack.aclose()
    
    async def list_tools(self) -> None:
        """List available tools."""
        if not self.tools:
            print("❌ No tools available or not connected")
            return
            
        print("📋 Available Tools:")
        for tool in self.tools:
            print(f"  • {tool.name}: {tool.description}")
    
    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Call a specific tool with arguments."""
        if not self.session:
            raise RuntimeError("Not connected to server")
            
        result = await self.session.call_tool(tool_name, args)
        output = ""
        for content in result.content:
            if hasattr(content, 'text'):
                output += content.text
        return output
    
    async def test_all_tools(self) -> None:
        """Test all available tools with sample data."""
        print("🧪 Testing all tools...")
        
        if not self.tools:
            print("❌ No tools available")
            return
        
        test_cases = [
            ("promptfoo_list", {"directory": "."}, "� Testing promptfoo_list..."),
            ("promptfoo_init", {"directory": "test_project"}, "🚀 Testing promptfoo_init..."),
            ("promptfoo_view", {}, "👀 Testing promptfoo_view..."),
            ("promptfoo_eval", {"config_path": "promptfooconfig.yaml"}, "⚡ Testing promptfoo_eval...")
        ]
        
        for tool_name, args, description in test_cases:
            print(f"\n{description}")
            try:
                result = await self.call_tool(tool_name, args)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nAll tests completed!")


async def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Promptfoo Client")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--class", "-c", action="store_true", dest="use_class",
                       help="Use the MCPPromptfooClient class")
    
    args = parser.parse_args()
    
    try:
        if args.use_class:
            # Demo using the client class
            async with MCPPromptfooClient() as client:
                await client.list_tools()
                print("\n" + "=" * 50)
                await client.test_all_tools()
        elif args.interactive:
            await interactive_client()
        else:
            await test_server()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())