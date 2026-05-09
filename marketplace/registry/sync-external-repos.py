"""
MEMBRA External Repo Sync Script

This script syncs functions from external repos into the local marketplace.
It's used by GitHub Actions to keep external function references up to date.
"""

import json
import requests
from pathlib import Path
from typing import Dict, Any

class ExternalRepoSyncer:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / 'external' / 'repos.json'
        self.repos = self.load_repos()
    
    def load_repos(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: Could not load repos config from {self.config_path}")
            return {"repos": {}}
    
    def sync_all_repos(self):
        """Sync all functions from all configured external repos"""
        repos = self.repos.get('repos', {})
        
        for repo_name, repo_config in repos.items():
            if not repo_config.get('sync_enabled', False):
                print(f"Skipping {repo_name} (sync disabled)")
                continue
            
            print(f"Syncing {repo_name}...")
            
            for function_name in repo_config.get('functions', []):
                try:
                    self.sync_function(repo_name, function_name, repo_config)
                except Exception as error:
                    print(f"Failed to sync {function_name} from {repo_name}: {error}")
    
    def sync_function(self, repo_name: str, function_name: str, repo_config: Dict[str, Any]):
        """Sync a single function from an external repo"""
        api_base = repo_config.get('api_base')
        if not api_base:
            raise ValueError(f"No API base configured for {repo_name}")
        
        url = f"{api_base}/{function_name}/source"
        
        # Fetch function code
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            code = response.text
        except requests.RequestException as error:
            raise ValueError(f"Failed to fetch function from {url}: {error}")
        
        # Save to local marketplace/external
        local_path = Path(__file__).parent.parent / 'external' / repo_name / f"{function_name}.py"
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(local_path, 'w') as f:
            f.write(code)
        
        print(f"Synced {function_name} from {repo_name} -> {local_path}")
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get status of synced functions"""
        status = {
            "last_sync": None,
            "repos": {}
        }
        
        repos = self.repos.get('repos', {})
        
        for repo_name, repo_config in repos.items():
            repo_status = {
                "sync_enabled": repo_config.get('sync_enabled', False),
                "functions": {},
                "functions_synced": 0
            }
            
            for function_name in repo_config.get('functions', []):
                local_path = Path(__file__).parent.parent / 'external' / repo_name / f"{function_name}.py"
                repo_status["functions"][function_name] = {
                    "synced": local_path.exists(),
                    "path": str(local_path) if local_path.exists() else None
                }
                
                if local_path.exists():
                    repo_status["functions_synced"] += 1
            
            status["repos"][repo_name] = repo_status
        
        return status

if __name__ == "__main__":
    syncer = ExternalRepoSyncer()
    
    print("Starting external repo sync...")
    syncer.sync_all_repos()
    
    print("\nSync status:")
    status = syncer.get_sync_status()
    print(json.dumps(status, indent=2))
    
    print("\nSync complete!")
