#!/usr/bin/env python3
"""
Pre-commit linter to check Python syntax and common errors
"""
import sys
import ast
import subprocess
from pathlib import Path

def check_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except IndentationError as e:
        return False, f"IndentationError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_imports(filepath):
    """Check if all imports are valid"""
    try:
        result = subprocess.run(
            ['python3', '-m', 'py_compile', filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return False, result.stderr
        return True, None
    except Exception as e:
        return False, f"Import check failed: {str(e)}"

def get_staged_files():
    """Get list of staged Python files"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            cwd='/home/ubuntu/jabb-whatsapp-bot'
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f.endswith('.py') and f]
    except Exception as e:
        print(f"❌ Error getting staged files: {e}")
        return []

def main():
    """Main linter function"""
    print("🔍 Running pre-commit linter...")
    
    staged_files = get_staged_files()
    
    if not staged_files:
        print("✅ No Python files to check")
        return 0
    
    print(f"📝 Checking {len(staged_files)} file(s)...")
    
    errors = []
    
    for filepath in staged_files:
        full_path = Path('/home/ubuntu/jabb-whatsapp-bot') / filepath
        
        if not full_path.exists():
            continue
        
        print(f"  Checking {filepath}...")
        
        # Check syntax
        valid, error = check_python_syntax(full_path)
        if not valid:
            errors.append(f"❌ {filepath}: {error}")
            continue
        
        # Check imports
        valid, error = check_imports(full_path)
        if not valid:
            errors.append(f"❌ {filepath}: Import error\n{error}")
            continue
        
        print(f"  ✅ {filepath} OK")
    
    if errors:
        print("\n" + "="*70)
        print("🚨 LINTING ERRORS FOUND:")
        print("="*70)
        for error in errors:
            print(error)
        print("="*70)
        print("\n❌ Please fix the errors before committing.")
        return 1
    
    print("\n✅ All checks passed!")
    return 0

if __name__ == '__main__':
    sys.exit(main())

