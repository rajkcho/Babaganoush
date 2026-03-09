#!/usr/bin/env python3
"""
Push files to GitHub using the Contents API
"""

import requests
import base64
import json
import os
import subprocess

# GitHub repo details
OWNER = 'rajkcho'
REPO = 'Babaganoush'
BRANCH = 'main'

# Get list of changed/new files from git
def get_files_to_push():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        capture_output=True,
        text=True,
        cwd='/home/openclaw/.openclaw/workspace/figgybank'
    )
    return result.stdout.strip().split('\n')

def get_file_sha(filepath, token):
    """Get the SHA of an existing file (returns None if file doesn't exist)"""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{filepath}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None

def push_file(filepath, token, commit_message):
    """Push a single file to GitHub"""
    full_path = f'/home/openclaw/.openclaw/workspace/figgybank/{filepath}'
    
    if not os.path.exists(full_path):
        print(f"  ⚠️  {filepath} does not exist, skipping")
        return False
    
    # Read file content
    with open(full_path, 'rb') as f:
        content = f.read()
    
    # Base64 encode
    content_b64 = base64.b64encode(content).decode('utf-8')
    
    # Get existing SHA if file exists
    sha = get_file_sha(filepath, token)
    
    # Prepare API request
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{filepath}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'message': commit_message,
        'content': content_b64,
        'branch': BRANCH
    }
    
    if sha:
        data['sha'] = sha
        action = 'Updated'
    else:
        action = 'Created'
    
    # Make request
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"  ✅ {action}: {filepath}")
        return True
    else:
        print(f"  ❌ Failed: {filepath}")
        print(f"     Status: {response.status_code}")
        print(f"     Error: {response.json().get('message', 'Unknown error')}")
        return False

def main():
    print("🚀 Pushing files to GitHub via API...")
    print(f"   Repo: {OWNER}/{REPO}")
    print()
    
    # Check for GitHub token
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ No GITHUB_TOKEN found in environment")
        print("   Please provide a GitHub personal access token")
        print("   You can create one at: https://github.com/settings/tokens")
        print()
        print("   Or you can:")
        print("   1. Clone this repo locally")
        print("   2. Pull the changes with: git pull")
        print("   3. Push with: git push")
        return
    
    # Get files to push
    files = get_files_to_push()
    
    if not files or files == ['']:
        print("⚠️  No files staged for commit")
        print("   Run: git add <files> first")
        return
    
    print(f"📦 Found {len(files)} file(s) to push:\n")
    
    commit_message = "Add SEO-optimized calculator pages and updated sitemap"
    
    success_count = 0
    for filepath in files:
        if filepath and filepath.strip():
            if push_file(filepath, token, commit_message):
                success_count += 1
    
    print()
    print(f"✅ Successfully pushed {success_count}/{len(files)} files")
    
    if success_count == len(files):
        print("🎉 All files pushed successfully!")
        print(f"   View at: https://github.com/{OWNER}/{REPO}")
        print(f"   Live site: https://figgybank.ca/")
    else:
        print("⚠️  Some files failed to push. Check errors above.")

if __name__ == '__main__':
    main()
