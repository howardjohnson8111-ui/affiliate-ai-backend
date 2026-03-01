#!/usr/bin/env python3
"""Quick SDK verification script"""
import sys

print("=" * 70)
print("SDK VERIFICATION")
print("=" * 70)

print(f"\nPython executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import google.genai as genai
    print("✓ google.genai imported successfully")
except Exception as e:
    print(f"✗ Failed to import google.genai: {e}")
    sys.exit(1)

try:
    from google.genai import types
    print("✓ google.genai.types imported successfully")
except Exception as e:
    print(f"✗ Failed to import google.genai.types: {e}")
    sys.exit(1)

try:
    # Check key components
    assert hasattr(genai, 'Client'), "genai.Client not found"
    print("✓ genai.Client available")
    
    assert hasattr(types, 'Tool'), "types.Tool not found"
    print("✓ types.Tool available")
    
    assert hasattr(types, 'FunctionDeclaration'), "types.FunctionDeclaration not found"
    print("✓ types.FunctionDeclaration available")
    
    assert hasattr(types, 'Schema'), "types.Schema not found"
    print("✓ types.Schema available")
    
    assert hasattr(types, 'Content'), "types.Content not found"
    print("✓ types.Content available")
    
    assert hasattr(types, 'Part'), "types.Part not found"
    print("✓ types.Part available")
    
    assert hasattr(types, 'FunctionResponse'), "types.FunctionResponse not found"
    print("✓ types.FunctionResponse available")
    
except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("ALL SDK CHECKS PASSED - Ready to run ai_service.py")
print("=" * 70)
