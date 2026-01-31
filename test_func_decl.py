#!/usr/bin/env python3
"""
Test function declarations
"""
from google.genai import types

print("Testing FunctionDeclaration...")

try:
    func = types.FunctionDeclaration(
        name="test_func",
        description="A test function",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "name": types.Schema(type=types.Type.STRING, description="Name"),
                "platform": types.Schema(type=types.Type.STRING, description="Platform")
            },
            required=["name", "platform"]
        )
    )
    print("✓ FunctionDeclaration created successfully")
    print(f"  Name: {func.name}")
    print(f"  Description: {func.description}")
    print(f"  Parameters: {func.parameters}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nAvailable Type values: {[e.name for e in types.Type]}")
