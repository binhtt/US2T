"""
US2T - Explainable Test Case Generation from User Stories
Main implementation
"""

import os
import re
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import pandas as pd
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm


@dataclass
class SemanticModel:
    """Semantic model extracted from user story"""
    actor: str
    functionality: str
    goal: str
    constraints: List[str]
    acceptance_criteria: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SemanticModel':
        return cls(
            actor=data.get("actor", "unknown"),
            functionality=data.get("functionality", "unknown"),
            goal=data.get("goal", "unknown"),
            constraints=data.get("constraints", []),
            acceptance_criteria=data.get("acceptance_criteria", [])
        )


@dataclass
class TestCase:
    """Test case structure"""
    id: str
    type: str
    preconditions: str
    input: str
    steps: str
    expected_result: str
    covered_ac: List[str] = None
    explanation: str = None
    
    def __post_init__(self):
        if self.covered_ac is None:
            self.covered_ac = []
        if self.explanation is None:
            self.explanation = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "preconditions": self.preconditions,
            "input": self.input,
            "steps": self.steps,
            "expected_result": self.expected_result,
            "covered_ac": self.covered_ac,
            "explanation": self.explanation
        }


class US2TGenerator:
    """
    US2T Framework: Explainable Test Case Generation from User Stories
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-3B-Instruct",
        embedding_model: str = "all-MiniLM-L6-v2",
        device_map: str = "auto",
        torch_dtype: str = "float16",
        similarity_threshold: float = 0.6,
        max_new_tokens_semantic: int = 300,
        max_new_tokens_test: int = 800,
        temperature: float = 0.1,
        verbose: bool = True
    ):
        """
        Initialize US2T generator.
        
        Args:
            model_name: LLM model name
            embedding_model: Sentence transformer model for embeddings
            device_map: Device mapping for model loading
            torch_dtype: Data type for model
            similarity_threshold: Threshold for semantic similarity
            max_new_tokens_semantic: Max tokens for semantic extraction
            max_new_tokens_test: Max tokens for test generation
            temperature: Temperature for generation
            verbose: Print progress messages
        """
        self.model_name = model_name
        self.embedding_model_name = embedding_model
        self.device_map = device_map
        self.torch_dtype = getattr(torch, torch_dtype, torch.float16)
        self.similarity_threshold = similarity_threshold
        self.max_new_tokens_semantic = max_new_tokens_semantic
        self.max_new_tokens_test = max_new_tokens_test
        self.temperature = temperature
        self.verbose = verbose
        
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.embedder = None
        self._models_loaded = False
        
        if self.verbose:
            print(f"Initializing US2T with model: {model_name}")
    
    def load_models(self) -> None:
        """Load LLM and embedding models"""
        if self._models_loaded:
            return
            
        if self.verbose:
            print("Loading models...")
        start_time = time.time()
        
        # Load LLM
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device_map,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True
        )
        
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map=self.device_map
        )
        
        # Load embedding model
        if self.verbose:
            print("Loading embedding model...")
        self.embedder = SentenceTransformer(self.embedding_model_name)
        
        self._models_loaded = True
        
        if self.verbose:
            print(f"Models loaded in {time.time() - start_time:.2f}s")
    
    def extract_semantic_model(self, user_story: str) -> Optional[SemanticModel]:
        """
        Extract semantic model from user story using LLM.
        
        Args:
            user_story: User story text
            
        Returns:
            SemanticModel object or None if extraction fails
        """
        if not self._models_loaded:
            self.load_models()
        
        prompt = f"""
Analyze this user story and extract semantic information:

User Story: {user_story}

Return a JSON object with these 5 fields:
1. actor: Who is using the system? (single word or short phrase)
2. functionality: What action do they want to perform? (short phrase)
3. goal: Why do they want to do this? (short phrase)
4. constraints: What rules or limitations apply? (list of strings)
5. acceptance_criteria: What conditions must be met for success? (list of 3-5 strings)

Example for "As a student, I want to register for a course so that I can complete my study plan":
{{
    "actor": "student",
    "functionality": "register for a course",
    "goal": "complete study plan",
    "constraints": ["course availability", "prerequisites", "credit limit", "schedule conflict"],
    "acceptance_criteria": [
        "Course is available for registration",
        "Student satisfies prerequisites",
        "Credit limit not exceeded",
        "No schedule conflict",
        "Student not already registered"
    ]
}}

Return ONLY the JSON object, no other text.
"""
        
        messages = [
            {"role": "system", "content": "You are a requirement analyzer. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            if self.verbose:
                print("  → Extracting semantic model...")
            
            output = self.generator(
                messages,
                max_new_tokens=self.max_new_tokens_semantic,
                do_sample=False,
                return_full_text=False,
                temperature=self.temperature
            )
            
            response = output[0]["generated_text"]
            
            # Extract JSON
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start == -1 or end == 0:
                if self.verbose:
                    print("  ⚠️  No JSON found, using fallback")
                return self._create_fallback_semantic_model(user_story)
                
            json_str = response[start:end]
            
            # Clean JSON
            json_str = json_str.replace("'", '"')
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            data = json.loads(json_str)
            
            # Ensure all fields exist
            required_fields = ["actor", "functionality", "goal", "constraints", "acceptance_criteria"]
            for field in required_fields:
                if field not in data:
                    if field in ["actor", "functionality", "goal"]:
                        data[field] = "unknown"
                    else:
                        data[field] = []
            
            # Ensure acceptance_criteria has at least 3 items
            if len(data["acceptance_criteria"]) < 3:
                data["acceptance_criteria"] = self._generate_default_ac(data["functionality"])
            
            return SemanticModel(
                actor=data["actor"],
                functionality=data["functionality"],
                goal=data["goal"],
                constraints=data["constraints"],
                acceptance_criteria=data["acceptance_criteria"]
            )
            
        except Exception as e:
            if self.verbose:
                print(f"  ❌ Error extracting semantic model: {e}")
            return self._create_fallback_semantic_model(user_story)
    
    def _create_fallback_semantic_model(self, user_story: str) -> SemanticModel:
        """Create fallback semantic model from user story"""
        # Try to extract basic information using regex
        actor_match = re.search(r"As an? ([^,]+)", user_story, re.IGNORECASE)
        actor = actor_match.group(1).strip() if actor_match else "user"
        
        functionality_match = re.search(r"I want to ([^.]+)", user_story, re.IGNORECASE)
        functionality = functionality_match.group(1).strip() if functionality_match else "perform action"
        
        goal_match = re.search(r"so that ([^.]+)", user_story, re.IGNORECASE)
        goal = goal_match.group(1).strip() if goal_match else "achieve goal"
        
        return SemanticModel(
            actor=actor,
            functionality=functionality,
            goal=goal,
            constraints=["valid input", "user authenticated", "system operational"],
            acceptance_criteria=[
                f"{functionality} is performed successfully",
                "User receives confirmation",
                "System maintains consistency"
            ]
        )
    
    def _generate_default_ac(self, functionality: str) -> List[str]:
        """Generate default acceptance criteria based on functionality"""
        return [
            f"{functionality} is performed successfully",
            f"User receives confirmation of {functionality}",
            "System state is updated correctly",
            "All business rules are enforced",
            "System handles errors gracefully"
        ]
    
    def generate_test_cases(
        self,
        user_story: str,
        semantic_model: SemanticModel
    ) -> List[TestCase]:
        """
        Generate test cases from user story and semantic model.
        
        Args:
            user_story: Original user story
            semantic_model: Extracted semantic model
            
        Returns:
            List of TestCase objects
        """
        if not self._models_loaded:
            self.load_models()
        
        ac_text = "\n".join([f"  - {ac}" for ac in semantic_model.acceptance_criteria])
        constraints_text = "\n".join([f"  - {c}" for c in semantic_model.constraints])
        
        prompt = f"""
Generate 5 test cases for this user story:

User Story: {user_story}
Actor: {semantic_model.actor}
Functionality: {semantic_model.functionality}
Goal: {semantic_model.goal}

Constraints:
{constraints_text}

Acceptance Criteria:
{ac_text}

Generate:
1. Positive test: Valid flow, everything works
2. Negative test: Invalid input or conditions
3. Boundary test: Edge cases (max/min values)
4. Exception test: Error conditions
5. Concurrency test: Multiple users/operations

Each test case must have:
- id: TC01 to TC05
- type: positive/negative/boundary/exception/concurrency
- preconditions: What must be true before test
- input: What data is provided
- steps: How to execute the test
- expected_result: What should happen

Return JSON array only, exactly like this:
[
{{
    "id": "TC01",
    "type": "positive",
    "preconditions": "Course is available, prerequisites met",
    "input": "Valid course registration details",
    "steps": "1. Login as student\\n2. Select course\\n3. Click Register",
    "expected_result": "Registration successful, course added to schedule"
}}
]
"""
        
        messages = [
            {"role": "system", "content": "You are a test case designer. Return JSON array only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            if self.verbose:
                print("  → Generating test cases...")
            
            output = self.generator(
                messages,
                max_new_tokens=self.max_new_tokens_test,
                do_sample=False,
                return_full_text=False,
                temperature=self.temperature
            )
            
            response = output[0]["generated_text"]
            
            # Extract and parse JSON
            from .utils import extract_json
            test_cases_json = extract_json(response)
            
            if not test_cases_json:
                if self.verbose:
                    print("  ⚠️  No JSON found, using fallback")
                return self._create_fallback_tests(semantic_model)
            
            # Convert to TestCase objects
            test_cases = []
            for tc_data in test_cases_json:
                test_cases.append(TestCase(
                    id=tc_data.get("id", f"TC{len(test_cases)+1:02d}"),
                    type=tc_data.get("type", "positive"),
                    preconditions=tc_data.get("preconditions", ""),
                    input=tc_data.get("input", ""),
                    steps=tc_data.get("steps", ""),
                    expected_result=tc_data.get("expected_result", ""),
                    covered_ac=[],
                    explanation=""
                ))
            
            # Ensure we have exactly 5 test cases
            while len(test_cases) < 5:
                test_cases.append(self._create_fallback_test(semantic_model, len(test_cases) + 1))
            
            return test_cases[:5]
            
        except Exception as e:
            if self.verbose:
                print(f"  ❌ Error generating test cases: {e}")
            return self._create_fallback_tests(semantic_model)
    
    def _create_fallback_tests(self, semantic_model: SemanticModel) -> List[TestCase]:
        """Create fallback test suite"""
        test_cases = []
        for i in range(1, 6):
            test_cases.append(self._create_fallback_test(semantic_model, i))
        return test_cases
    
    def _create_fallback_test(self, semantic_model: SemanticModel, num: int) -> TestCase:
        """Create a single fallback test case"""
        types = ["positive", "negative", "boundary", "exception", "concurrency"]
        type_name = types[(num - 1) % len(types)]
        
        actor = semantic_model.actor
        functionality = semantic_model.functionality
        
        test_cases = {
            "positive": {
                "preconditions": f"All requirements for {functionality} are met",
                "input": f"Valid {functionality} request",
                "steps": f"1. {actor} initiates {functionality}\n2. System processes request\n3. Confirmation received",
                "expected_result": f"{functionality} completed successfully"
            },
            "negative": {
                "preconditions": "Invalid input conditions",
                "input": f"Invalid {functionality} request",
                "steps": f"1. {actor} submits invalid data\n2. System validates input\n3. Error message shown",
                "expected_result": "Request rejected with appropriate error message"
            },
            "boundary": {
                "preconditions": "System at boundary condition",
                "input": f"Edge case {functionality} request",
                "steps": f"1. {actor} tests boundary values\n2. System processes edge case\n3. Result validated",
                "expected_result": "System handles boundary conditions correctly"
            },
            "exception": {
                "preconditions": "Error condition exists",
                "input": f"Exceptional {functionality} request",
                "steps": f"1. {actor} triggers exception\n2. System catches error\n3. Error handled gracefully",
                "expected_result": "System handles exceptions without crashing"
            },
            "concurrency": {
                "preconditions": f"Multiple {actor}s accessing system",
                "input": f"Concurrent {functionality} requests",
                "steps": f"1. Multiple {actor}s initiate {functionality}\n2. System processes concurrently\n3. Verify consistency",
                "expected_result": "System maintains data consistency with concurrent operations"
            }
        }
        
        tc_data = test_cases[type_name]
        
        return TestCase(
            id=f"TC{num:02d}",
            type=type_name,
            preconditions=tc_data["preconditions"],
            input=tc_data["input"],
            steps=tc_data["steps"],
            expected_result=tc_data["expected_result"],
            covered_ac=[],
            explanation=""
        )
    
    def compute_traceability(
        self,
        test_cases: List[TestCase],
        semantic_model: SemanticModel
    ) -> Tuple[List[TestCase], pd.DataFrame, float]:
        """
        Compute traceability between test cases and acceptance criteria.
        
        Args:
            test_cases: List of test cases
            semantic_model: Semantic model
            
        Returns:
            Tuple of (updated test cases, traceability matrix, coverage)
        """
        if not self._models_loaded:
            self.load_models()
        
        ac_list = semantic_model.acceptance_criteria
        
        # Compute coverage for each test case
        for tc in test_cases:
            text = " ".join([
                tc.preconditions,
                tc.input,
                tc.steps,
                tc.expected_result
            ]).lower()
            
            covered = []
            
            for ac in ac_list:
                # Check coverage
                if self._check_coverage(ac, text):
                    covered.append(ac)
            
            tc.covered_ac = covered if covered else ["No acceptance criteria matched"]
            tc.explanation = f"This {tc.type} test verifies: " + ", ".join(tc.covered_ac)
        
        # Build traceability matrix
        rows = []
        for ac in ac_list:
            ids = [tc.id for tc in test_cases if ac in tc.covered_ac]
            rows.append({
                "Acceptance Criteria": ac,
                "Test Cases": ", ".join(ids) if ids else "❌ Not covered"
            })
        
        traceability_matrix = pd.DataFrame(rows)
        
        # Calculate coverage
        covered_set = set()
        for tc in test_cases:
            covered_set.update(tc.covered_ac)
        covered_set.discard("No acceptance criteria matched")
        
        coverage = (len(covered_set) / len(ac_list)) * 100 if ac_list else 0
        
        return test_cases, traceability_matrix, coverage
    
    def _check_coverage(self, acceptance_criterion: str, text: str) -> bool:
        """
        Check if a test case covers an acceptance criterion.
        
        Args:
            acceptance_criterion: Acceptance criterion text
            text: Combined test case text
            
        Returns:
            True if covered, False otherwise
        """
        # Keyword matching
        keywords = acceptance_criterion.lower().split()
        common = {"the", "a", "an", "is", "are", "was", "were", "to", "for", "of", "with", "and", "or"}
        keywords = [w for w in keywords if w not in common and len(w) > 3]
        
        if keywords:
            for kw in keywords:
                if kw in text:
                    return True
        
        # Semantic similarity
        try:
            criterion_embedding = self.embedder.encode(acceptance_criterion)
            text_embedding = self.embedder.encode(text)
            
            similarity = np.dot(criterion_embedding, text_embedding) / (
                np.linalg.norm(criterion_embedding) * np.linalg.norm(text_embedding) + 1e-8
            )
            
            return similarity >= self.similarity_threshold
        except:
            return False
    
    def generate(
        self,
        user_story: str,
        save_results: bool = True,
        output_dir: str = "outputs/"
    ) -> Dict:
        """
        Main generation pipeline.
        
        Args:
            user_story: User story text
            save_results: Whether to save results to files
            output_dir: Output directory
            
        Returns:
            Dictionary containing all results
        """
        if self.verbose:
            print("\n" + "="*60)
            print("🚀 Starting US2T Generation")
            print("="*60)
        
        # Load models if not loaded
        if not self._models_loaded:
            self.load_models()
        
        # Extract semantic model
        if self.verbose:
            print("\n📝 Extracting semantic model...")
        start_time = time.time()
        semantic_model = self.extract_semantic_model(user_story)
        
        if semantic_model is None:
            raise ValueError("Failed to extract semantic model")
        
        if self.verbose:
            print(f"✅ Semantic model extracted in {time.time() - start_time:.2f}s")
        
        if self.verbose:
            print("\n========== SEMANTIC MODEL ==========")
            print(json.dumps({
                "actor": semantic_model.actor,
                "functionality": semantic_model.functionality,
                "goal": semantic_model.goal,
                "constraints": semantic_model.constraints,
                "acceptance_criteria": semantic_model.acceptance_criteria
            }, indent=2))
        
        # Generate test cases
        if self.verbose:
            print("\n🔄 Generating test cases...")
        start_time = time.time()
        test_cases = self.generate_test_cases(user_story, semantic_model)
        if self.verbose:
            print(f"✅ Test cases generated in {time.time() - start_time:.2f}s")
        
        # Compute traceability
        if self.verbose:
            print("\n🔄 Computing traceability...")
        test_cases, traceability_matrix, coverage = self.compute_traceability(
            test_cases, semantic_model
        )
        
        if self.verbose:
            print(f"\n📊 Requirement Coverage: {coverage:.1f}%")
        
        # Prepare results
        results = {
            "user_story": user_story,
            "semantic_model": semantic_model,
            "test_cases": test_cases,
            "traceability_matrix": traceability_matrix,
            "coverage": coverage
        }
        
        # Save results
        if save_results:
            self.save_results(results, output_dir)
        
        return results
    
    def save_results(self, results: Dict, output_dir: str = "outputs/") -> None:
        """Save results to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save test cases
        tc_data = []
        for tc in results["test_cases"]:
            tc_data.append({
                "id": tc.id,
                "type": tc.type,
                "preconditions": tc.preconditions,
                "input": tc.input,
                "steps": tc.steps,
                "expected_result": tc.expected_result,
                "covered_ac": ", ".join(tc.covered_ac),
                "explanation": tc.explanation
            })
        
        df_tc = pd.DataFrame(tc_data)
        df_tc.to_csv(f"{output_dir}/generated_test_cases.csv", index=False)
        
        # Save traceability matrix
        results["traceability_matrix"].to_csv(
            f"{output_dir}/traceability_matrix.csv",
            index=False
        )
        
        # Save semantic model
        sm = results["semantic_model"]
        with open(f"{output_dir}/semantic_model.json", "w") as f:
            json.dump({
                "actor": sm.actor,
                "functionality": sm.functionality,
                "goal": sm.goal,
                "constraints": sm.constraints,
                "acceptance_criteria": sm.acceptance_criteria
            }, f, indent=2)
        
        # Save test cases JSON
        tc_json = []
        for tc in results["test_cases"]:
            tc_json.append(tc.to_dict())
        
        with open(f"{output_dir}/test_cases.json", "w") as f:
            json.dump(tc_json, f, indent=2)
        
        # Save summary
        with open(f"{output_dir}/summary.txt", "w") as f:
            f.write("="*60 + "\n")
            f.write("US2T GENERATION SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"User Story: {results['user_story']}\n\n")
            f.write(f"Actor: {results['semantic_model'].actor}\n")
            f.write(f"Functionality: {results['semantic_model'].functionality}\n")
            f.write(f"Goal: {results['semantic_model'].goal}\n\n")
            f.write(f"Test Cases Generated: {len(results['test_cases'])}\n")
            f.write(f"Requirement Coverage: {results['coverage']:.1f}%\n")
            f.write("="*60 + "\n")
        
        if self.verbose:
            print(f"\n✅ Results saved to {output_dir}/")
    
    def generate_batch(
        self,
        user_stories: List[str],
        save_results: bool = True,
        output_dir: str = "outputs/"
    ) -> List[Dict]:
        """
        Generate test cases for multiple user stories.
        
        Args:
            user_stories: List of user stories
            save_results: Whether to save results
            output_dir: Output directory
            
        Returns:
            List of results
        """
        results = []
        
        for i, story in enumerate(user_stories):
            if self.verbose:
                print(f"\n📝 Processing story {i+1}/{len(user_stories)}")
            
            result = self.generate(story, save_results, f"{output_dir}/story_{i+1:03d}/")
            results.append(result)
        
        return results
