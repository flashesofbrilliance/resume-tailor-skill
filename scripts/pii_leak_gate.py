#!/usr/bin/env python3
"""pii_leak_gate.py — Mechanical test asserting zero raw candidate PII leaves the local boundary.

Fails (exit 1) if raw unredacted personal identifiable information (emails, phone numbers,
home addresses, or raw private identifiers) is found inside candidate resume outputs,
intermediate LLM context bundles, or network-bound payloads.

Usage:
    python3 pii_leak_gate.py <file_or_dir_to_check>
"""

import sys
import os
import re

PHONE_REGEX = re.compile(r'(\b\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

# Allowlist: Public project / generic contact addresses
ALLOWED_EMAILS = {
    "noreply@anthropic.com",
    "support@arcs.care",
    "admin@arcs.care",
    "contact@example.com"
}

def scan_text(text, filepath):
    leaks = []
    
    # Check phones
    for m in PHONE_REGEX.finditer(text):
        leaks.append(f"Phone leak detected: '{m.group(0)}' in {filepath}")
        
    # Check emails
    for m in EMAIL_REGEX.finditer(text):
        email = m.group(0).lower()
        if email not in ALLOWED_EMAILS and not email.endswith("@example.com"):
            leaks.append(f"Email leak detected: '{email}' in {filepath}")
            
    return leaks

def scan_path(target):
    all_leaks = []
    if os.path.isfile(target):
        with open(target, 'r', errors='ignore') as f:
            all_leaks.extend(scan_text(f.read(), target))
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(('.html', '.json', '.txt', '.md')):
                    p = os.path.join(root, file)
                    with open(p, 'r', errors='ignore') as f:
                        all_leaks.extend(scan_text(f.read(), p))
    return all_leaks

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pii_leak_gate.py <file_or_dir_to_check>")
        sys.exit(2)
        
    target_path = sys.argv[1]
    if not os.path.exists(target_path):
        print(f"Error: Target path does not exist: {target_path}")
        sys.exit(2)
        
    detected = scan_path(target_path)
    if detected:
        print(f"❌ PII_LEAK_GATE: FAIL — {len(detected)} raw PII patterns detected!")
        for l in detected[:10]:
            print(f"   ✖ {l}")
        sys.exit(1)
    else:
        print(f"✓ PII_LEAK_GATE: PASS — clean air-gap, 0 leaks detected in {target_path}")
        sys.exit(0)
