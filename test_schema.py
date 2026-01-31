#!/usr/bin/env python3
"""
Test the correct Schema syntax
"""
from google.genai import types
import inspect

print("Schema signature:")
print(inspect.signature(types.Schema))

print("\nTrying different Schema creations...")

try:
    # Try with type parameter
    s1 = types.Schema(type="OBJECT", properties={})
    print("✓ types.Schema(type='OBJECT', properties={}) works")
except Exception as e:
    print(f"✗ types.Schema(type='OBJECT', ...): {e}")

try:
    # Try with type_ parameter
    s2 = types.Schema(type_="OBJECT", properties={})
    print("✓ types.Schema(type_='OBJECT', properties={}) works")
except Exception as e:
    print(f"✗ types.Schema(type_='OBJECT', ...): {e}")

# Print available fields
print(f"\nSchema fields: {types.Schema.model_fields.keys()}")
