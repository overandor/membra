"""
MEMBRA Super Mono Repo - API Gateway

This gateway provides a unified interface for calling functions
from external repos as if they were local functions.
It enables the repo to self-reference as a marketplace where
code functions are the tradable assets.
"""

import json
from typing import Dict, Any, Optional
import requests
from pathlib import Path

class ExternalFunctionCall:
    def __init__(self, repo: str, function: str, params: Optional[Dict[str, Any]] = None):
        self.repo = repo
        self.function = function
        self.params = params or {}

class FunctionResult:
    def __init__(self, success: bool, data: Optional[Any] = None, error: Optional[str] = None, 
                 source: str = 'external', latency: Optional[float] = None):
        self.success = success
        self.data = data
        self.error = error
        self.source = source
        self.latency = latency

class APIGateway:
    def __init__(self):
        self.registry_path = Path(__file__).parent.parent / 'registry' / 'functions.json'
        self.cache: Dict[str, FunctionResult] = {}
        self.external_endpoints: Dict[str, str] = {}
        self.load_registry()
        self.initialize_endpoints()
    
    def load_registry(self) -> Dict[str, Any]:
        try:
            with open(self.registry_path, 'r') as f:
                self.registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.registry = self.initialize_registry()
    
    def initialize_registry(self) -> Dict[str, Any]:
        initial_registry = {
            "version": "1.0.0",
            "last_updated": "2026-05-09T00:00:00Z",
            "functions": {},
            "external_api_endpoints": {}
        }
        self.save_registry(initial_registry)
        return initial_registry
    
    def save_registry(self, registry: Dict[str, Any]):
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def initialize_endpoints(self):
        external_apis = self.registry.get('external_api_endpoints', {})
        for repo_name, config in external_apis.items():
            for endpoint_name, path in config.get('endpoints', {}).items():
                key = f"{repo_name}:{endpoint_name}"
                url = f"{config['base_url']}{path}"
                self.external_endpoints[key] = url
    
    def call_function(self, call: ExternalFunctionCall) -> FunctionResult:
        key = f"{call.repo}:{call.function}"
        
        try:
            if key in self.external_endpoints:
                return self.call_external_function(call)
            else:
                return self.call_local_function(call)
        except Exception as error:
            return FunctionResult(
                success=False,
                error=str(error),
                source='external',
                latency=0
            )
    
    def call_external_function(self, call: ExternalFunctionCall) -> FunctionResult:
        key = f"{call.repo}:{call.function}"
        url = self.external_endpoints.get(key)
        
        if not url:
            return FunctionResult(
                success=False,
                error=f"No endpoint found for {key}",
                source='external',
                latency=0
            )
        
        cache_key = f"{key}:{json.dumps(call.params)}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            return FunctionResult(
                success=cached.success,
                data=cached.data,
                error=cached.error,
                source='external',
                latency=0
            )
        
        try:
            response = requests.post(
                url,
                json=call.params,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            data = response.json()
            
            result = FunctionResult(
                success=response.ok,
                data=data,
                source='external',
                latency=response.elapsed.total_seconds()
            )
            
            if result.success:
                self.cache[cache_key] = result
            
            return result
        except Exception as error:
            return FunctionResult(
                success=False,
                error=str(error),
                source='external',
                latency=0
            )
    
    def call_local_function(self, call: ExternalFunctionCall) -> FunctionResult:
        function_name = call.function
        params = call.params or {}
        
        try:
            # Import and execute local function
            module_path = f"marketplace.functions.{function_name}"
            module = __import__(module_path, fromlist=[function_name])
            result = getattr(module, function_name)(params)
            
            return FunctionResult(
                success=True,
                data=result,
                source='local',
                latency=0
            )
        except ImportError:
            return FunctionResult(
                success=False,
                error=f"Local function not found: {function_name}",
                source='local',
                latency=0
            )
        except Exception as error:
            return FunctionResult(
                success=False,
                error=str(error),
                source='local',
                latency=0
            )
    
    def get_available_functions(self) -> list[str]:
        functions = []
        
        for key in self.external_endpoints:
            functions.append(key)
        
        local_functions = self.registry.get('functions', {})
        for name in local_functions:
            functions.append(f"local:{name}")
        
        return functions
    
    def sync_function(self, repo: str, function_name: str) -> str:
        key = f"{repo}:{function_name}"
        url = self.external_endpoints.get(key)
        
        if not url:
            raise ValueError(f"No endpoint found for {key}")
        
        # Fetch function code from external repo
        response = requests.get(f"{url}/source", timeout=10)
        code = response.text
        
        # Save to local marketplace/external
        local_path = Path(__file__).parent.parent / 'external' / repo / f"{function_name}.py"
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(local_path, 'w') as f:
            f.write(code)
        
        return str(local_path)
    
    def clear_cache(self):
        self.cache.clear()

# Singleton instance
gateway = APIGateway()

# Convenience functions
def call_external(repo: str, function: str, params: Optional[Dict[str, Any]] = None) -> FunctionResult:
    return gateway.call_function(ExternalFunctionCall(repo, function, params))

def list_functions() -> list[str]:
    return gateway.get_available_functions()

if __name__ == "__main__":
    # Test the gateway
    print("Available functions:", list_functions())
    print("Gateway initialized successfully")
