#!/usr/bin/env python3
"""Inspect the exact SDK method signature for generate_content"""
import inspect
import google.genai as genai
from google.genai import types

print("=" * 70)
print("SDK METHOD SIGNATURE INSPECTION")
print("=" * 70)

# Get the client
client = genai.Client(api_key="dummy_key")

# Get the generate_content method
generate_method = client.models.generate_content

print("\n1. Full Method Signature:")
print("-" * 70)
sig = inspect.signature(generate_method)
print(f"generate_content{sig}")

print("\n2. Parameters:")
print("-" * 70)
for param_name, param in sig.parameters.items():
    print(f"  {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'Any'}")

print("\n3. Docstring:")
print("-" * 70)
print(generate_method.__doc__)

print("\n4. Check for types.Tool attributes:")
print("-" * 70)
print(f"  types.Tool exists: {hasattr(types, 'Tool')}")
print(f"  types.GenerateContentConfig exists: {hasattr(types, 'GenerateContentConfig')}")
print(f"  types.FunctionDeclaration exists: {hasattr(types, 'FunctionDeclaration')}")

if hasattr(types, 'Tool'):
    tool_sig = inspect.signature(types.Tool)
    print(f"\n  types.Tool signature: {tool_sig}")

print("\n" + "=" * 70)
