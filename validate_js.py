#!/usr/bin/env python3.11
"""
JavaScript Validation Script
Checks for common JavaScript errors in HTML templates before committing.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

def extract_javascript_from_html(html_content):
    """Extract all JavaScript code blocks from HTML."""
    # Find all <script> blocks
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, html_content, re.DOTALL)
    return scripts

def check_duplicate_declarations(js_code):
    """Check for duplicate variable declarations in global scope only."""
    errors = []
    
    # Track global variable declarations (not inside functions)
    global_declarations = defaultdict(list)
    
    # Find all let/const/var declarations
    patterns = [
        (r'\blet\s+(\w+)', 'let'),
        (r'\bconst\s+(\w+)', 'const'),
        (r'\bvar\s+(\w+)', 'var')
    ]
    
    # Track brace depth to identify global scope
    lines = js_code.split('\n')
    brace_depth = 0
    
    for line_num, line in enumerate(lines, 1):
        # Update brace depth
        brace_depth += line.count('{') - line.count('}')
        
        # Only check declarations at global scope (brace_depth <= 0 before the line)
        # We check before incrementing because the declaration line itself might have braces
        line_depth = brace_depth - line.count('{') + line.count('}')
        
        if line_depth <= 0:  # Global scope
            for pattern, decl_type in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    var_name = match.group(1)
                    global_declarations[var_name].append((line_num, decl_type, line.strip()))
    
    # Check for duplicates
    for var_name, occurrences in global_declarations.items():
        if len(occurrences) > 1:
            errors.append({
                'type': 'duplicate_declaration',
                'variable': var_name,
                'occurrences': occurrences,
                'message': f"Variable '{var_name}' is declared {len(occurrences)} times in global scope"
            })
    
    return errors

def check_syntax_errors(js_code):
    """Check for common JavaScript syntax errors."""
    errors = []
    
    # Check for unmatched braces
    brace_count = js_code.count('{') - js_code.count('}')
    if brace_count != 0:
        errors.append({
            'type': 'unmatched_braces',
            'message': f"Unmatched braces: {abs(brace_count)} {'opening' if brace_count > 0 else 'closing'} braces"
        })
    
    # Check for unmatched parentheses
    paren_count = js_code.count('(') - js_code.count(')')
    if paren_count != 0:
        errors.append({
            'type': 'unmatched_parentheses',
            'message': f"Unmatched parentheses: {abs(paren_count)} {'opening' if paren_count > 0 else 'closing'} parentheses"
        })
    
    # Check for unmatched brackets
    bracket_count = js_code.count('[') - js_code.count(']')
    if bracket_count != 0:
        errors.append({
            'type': 'unmatched_brackets',
            'message': f"Unmatched brackets: {abs(bracket_count)} {'opening' if bracket_count > 0 else 'closing'} brackets"
        })
    
    return errors

def validate_html_file(file_path):
    """Validate JavaScript in an HTML file."""
    print(f"\n🔍 Validating: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    scripts = extract_javascript_from_html(html_content)
    
    if not scripts:
        print("   ℹ️  No JavaScript found")
        return True
    
    print(f"   📝 Found {len(scripts)} script block(s)")
    
    all_errors = []
    
    for i, script in enumerate(scripts, 1):
        # Check for duplicate declarations
        dup_errors = check_duplicate_declarations(script)
        if dup_errors:
            all_errors.extend([(i, err) for err in dup_errors])
        
        # Check for syntax errors
        syntax_errors = check_syntax_errors(script)
        if syntax_errors:
            all_errors.extend([(i, err) for err in syntax_errors])
    
    if all_errors:
        print(f"\n   ❌ Found {len(all_errors)} error(s):\n")
        for block_num, error in all_errors:
            print(f"   Script Block {block_num}:")
            print(f"   Type: {error['type']}")
            print(f"   {error['message']}")
            
            if 'occurrences' in error:
                for line_num, decl_type, line_text in error['occurrences']:
                    print(f"      Line {line_num}: {decl_type} {error['variable']}")
                    print(f"         {line_text}")
            print()
        
        return False
    else:
        print("   ✅ No errors found")
        return True

def main():
    """Main validation function."""
    print("🔍 JavaScript Validation Script")
    print("=" * 60)
    
    # Find all HTML files in templates directory
    templates_dir = Path(__file__).parent.parent / 'templates'
    
    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        sys.exit(1)
    
    html_files = list(templates_dir.glob('*.html'))
    
    if not html_files:
        print("ℹ️  No HTML files found")
        sys.exit(0)
    
    print(f"📁 Found {len(html_files)} HTML file(s)")
    
    all_valid = True
    
    for html_file in html_files:
        if not validate_html_file(html_file):
            all_valid = False
    
    print("\n" + "=" * 60)
    
    if all_valid:
        print("✅ All files passed validation")
        sys.exit(0)
    else:
        print("❌ Validation failed - please fix the errors above")
        sys.exit(1)

if __name__ == '__main__':
    main()
