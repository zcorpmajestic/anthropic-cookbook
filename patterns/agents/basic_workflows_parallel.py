from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable
from util import llm_call, time_invocation

def parallel(prompt: str, inputs: List[str], n_workers: int = 3) -> List[str]:
    """Process multiple inputs concurrently with the same prompt."""
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(llm_call, f"{prompt}\nInput: {x}") for x in inputs]
        return [f.result() for f in futures]

def serial(prompt: str, inputs: List[str], n_workers: int = 3) -> List[str]:
    """Process multiple inputs concurrently with the same prompt."""
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(llm_call, f"{prompt}\nInput: {x}") for x in inputs]
        return [f.result() for f in futures]

stakeholders = [
    """Customers:
    - Price sensitive
    - Want better tech
    - Environmental concerns""",
    
    """Employees:
    - Job security worries
    - Need new skills
    - Want clear direction""",
    
    """Investors:
    - Expect growth
    - Want cost control
    - Risk concerns""",
    
    """Suppliers:
    - Capacity constraints
    - Price pressures
    - Tech transitions"""
]

print("<---Parallel--->")
impact_results = time_invocation(lambda: parallel(
    """Analyze how market changes will impact this stakeholder group.
    Provide specific impacts and recommended actions.
    Format with clear sections and priorities.""",
    stakeholders))

print("<---Serial--->")
impact_results = time_invocation(lambda: serial(
    """Analyze how market changes will impact this stakeholder group.
    Provide specific impacts and recommended actions.
    Format with clear sections and priorities.""",
    stakeholders))


