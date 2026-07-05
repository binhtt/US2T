#!/usr/bin/env python3
"""
US2T - Interactive Demo
"""

import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from us2t import US2TGenerator
from utils import load_benchmark, save_benchmark_results


def print_header(text: str, char: str = "=") -> None:
    """Print a formatted header"""
    print("\n" + char * 60)
    print(text)
    print(char * 60)


def get_user_story_interactive() -> str:
    """Get user story from interactive input"""
    print_header("📝 USER STORY INPUT", "-")
    print("\nEnter your user story (type 'END' on a new line to finish):")
    print("Example: As a student, I want to register for a course")
    print()
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    
    if not lines:
        print("\n⚠️  No input received. Using example story.")
        return get_example_story()
    
    return "\n".join(lines)


def get_example_story() -> str:
    """Return example user story"""
    return """As a student, I want to register for a course
so that I can complete my study plan."""


def get_stories_from_benchmark(project: str = "ecommerce") -> List[Dict]:
    """Load stories from benchmark"""
    benchmark_path = Path(__file__).parent.parent / "benchmark" / project / "stories.json"
    
    if not benchmark_path.exists():
        print(f"❌ Benchmark file not found: {benchmark_path}")
        return []
    
    return load_benchmark(str(benchmark_path))


def run_demo():
    """Run interactive demo"""
    print_header("🚀 US2T - Explainable Test Case Generation")
    print("\nChoose an option:")
    print("  1. Enter a single user story")
    print("  2. Run benchmark (all stories from a project)")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "3":
        print("\nGoodbye! 👋")
        return
    
    # Initialize generator
    print("\n🔧 Initializing US2T Generator...")
    generator = US2TGenerator(verbose=True)
    generator.load_models()
    
    if choice == "1":
        # Single story mode
        user_story = get_user_story_interactive()
        
        print_header("📄 USER STORY")
        print(user_story)
        
        # Generate test cases
        results = generator.generate(user_story, save_results=True)
        
        # Display results
        print_header("📊 RESULTS")
        print(f"Coverage: {results['coverage']:.1f}%")
        print(f"Test Cases: {len(results['test_cases'])}")
        
        # Print test cases
        print("\nTest Cases:")
        for tc in results['test_cases']:
            print(f"\n  {tc.id} - {tc.type.upper()}")
            print(f"    Preconditions: {tc.preconditions}")
            print(f"    Input: {tc.input}")
            print(f"    Steps: {tc.steps.replace(chr(92) + 'n', '\n    ')}")
            print(f"    Expected: {tc.expected_result}")
            print(f"    Covers: {', '.join(tc.covered_ac)}")
    
    elif choice == "2":
        # Benchmark mode
        print("\nSelect a project:")
        projects = ["ecommerce", "online_banking", "course_management", "healthcare", "mobile_payment"]
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p.replace('_', ' ').title()}")
        
        proj_choice = input("\nEnter choice: ").strip()
        
        try:
            idx = int(proj_choice) - 1
            project = projects[idx]
        except:
            print("Invalid choice. Using ecommerce.")
            project = "ecommerce"
        
        # Load stories
        stories = get_stories_from_benchmark(project)
        
        if not stories:
            print("❌ No stories found.")
            return
        
        print(f"\n📚 Found {len(stories)} stories in {project}")
        
       
