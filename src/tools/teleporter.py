#!/usr/bin/env python3
"""Simple Teleporter helper for AkashaOS
This script reads a teleport manifest YAML and copies files from an incoming update directory
into the repository layout described by the manifest. It performs only local filesystem operations.
Usage examples:
  python3 src/tools/teleporter.py --manifest configs/teleport/teleport_manifest.yaml --incoming /path/to/extracted_update_dir --dry-run
The manifest format expected (example):
  files:
    - src: update/specs/core.yaml
      dest: configs/teleport/specs/core.yaml
"""
import argparse, yaml, os, shutil, sys

def load_manifest(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def apply_manifest(manifest, incoming_dir, repo_root='.', dry_run=True):
    files = manifest.get('files') or []
    results = []
    for entry in files:
        src = entry.get('src')
        dest = entry.get('dest')
        if not src or not dest:
            results.append((entry, 'skipped: missing src/dest'))
            continue
        src_path = os.path.join(incoming_dir, src)
        dest_path = os.path.join(repo_root, dest)
        if not os.path.exists(src_path):
            results.append((entry, f'missing source: {src_path}'))
            continue
        results.append((entry, 'would copy' if dry_run else 'copied'))
        if not dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
    return results

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', required=True, help='Path to teleport manifest YAML in the repo')
    p.add_argument('--incoming', required=True, help='Path to incoming extracted update directory (local)')
    p.add_argument('--repo-root', default='.', help='Repository root (where dest paths are relative to)')
    p.add_argument('--apply', action='store_true', help='Actually perform copies (default is dry-run)')
    args = p.parse_args()

    if not os.path.exists(args.manifest):
        print('Manifest not found:', args.manifest, file=sys.stderr); sys.exit(2)
    if not os.path.isdir(args.incoming):
        print('Incoming dir not found:', args.incoming, file=sys.stderr); sys.exit(3)

    manifest = load_manifest(args.manifest)
    results = apply_manifest(manifest, args.incoming, repo_root=args.repo_root, dry_run=not args.apply)
    for entry, status in results:
        print(status, entry)
    missing = [r for r in results if 'missing source' in r[1]]
    if missing:
        print('\nSome sources were missing. See messages above.', file=sys.stderr)
        sys.exit(4)

if __name__ == '__main__':
    main()
