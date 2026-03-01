#!/usr/bin/env python3
"""
Inspect the actual google-generativeai SDK signature
"""
import inspect
import google.genai as genai
from google.genai import types

print("=" * 70)
print("GEMINI SDK SIGNATURE INSPECTION")
print("=" * 70)

# Check what's available
client = genai.Client(api_key="test")

print("\n1. Methods available on client:")
print(f"   - models: {hasattr(client, 'models')}")
print(f"   - generate_content: {hasattr(client.models, 'generate_content')}")

print("\n2. Inspecting client.models.generate_content signature:")
sig = inspect.signature(client.models.generate_content)
print(f"   Parameters: {list(sig.parameters.keys())}")
for param_name, param in sig.parameters.items():
    print(f"     - {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'Any'}")

print("\n3. Checking types.Tool:")
print(f"   - types.Tool exists: {hasattr(types, 'Tool')}")
if hasattr(types, 'Tool'):
    print(f"   - Signature: {inspect.signature(types.Tool)}")

print("\n4. Checking for function_declarations:")
print(f"   - types.FunctionDeclaration exists: {hasattr(types, 'FunctionDeclaration')}")

print("\n5. Checking types.Tool function_declarations:")
try:
    tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="test",
                description="Test",
                parameters=types.Schema(type_="OBJECT", properties={})
            )
        ]
    )
    print(f"   - types.Tool with function_declarations works: True")
    print(f"   - Tool object: {tool}")
except Exception as e:
    print(f"   - types.Tool with function_declarations error: {e}")

print("\n6. Checking system_instruction parameter:")
print(f"   - 'system_instruction' in parameters: {'system_instruction' in sig.parameters}")

print("\n" + "=" * 70)
