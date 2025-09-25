#!/usr/bin/env python3
"""
Script to find duplicate scenario names in Runloop public benchmarks.
"""

import os
from collections import Counter
from runloop_api_client import Runloop

def find_duplicate_scenarios():
    client = Runloop(
        bearer_token=os.environ["RUNLOOP_API_KEY"],
        base_url=os.environ.get("RUNLOOP_BASE_URL")
    )
    
    benchmarks_page = client.benchmarks.list_public()
    
    for benchmark in benchmarks_page.benchmarks:
        print(f"Checking {benchmark.name} ({benchmark.id})...")
        
        try:
            scenario_defs = client.benchmarks.definitions(benchmark.id)
            scenario_names = [s.name for s in scenario_defs.scenarios]
            
            # Find duplicates
            name_counts = Counter(scenario_names)
            duplicates = {name: count for name, count in name_counts.items() if count > 1}
            
            if duplicates:
                print(f"  ❌ DUPLICATES FOUND:")
                for name, count in duplicates.items():
                    print(f"    '{name}': {count} times")
            else:
                print(f"  ✅ No duplicates")
                
        except Exception as e:
            print(f"  ⚠️  Error: {e}")

if __name__ == "__main__":
    find_duplicate_scenarios()