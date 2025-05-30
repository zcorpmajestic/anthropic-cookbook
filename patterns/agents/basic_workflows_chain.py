from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable
from util import llm_call
import time

#The time was actually better unchained, but the result was terrible - run it again and compare.

def chain(input: str, prompts: List[str]) -> str:
    start_time = time.time()
    result = input 
    for i, prompt in enumerate(prompts, 1):
        #print(f"\nStep {i}:")
        result = llm_call(f"{prompt}\nInput: {result}")
        print(result)
    elapsed = time.time() - start_time
    print(f"\nTotal elapsed time: {elapsed:.2f} seconds")
    return result

def unchain(input: str, prompts: List[str]) -> str:
    start_time = time.time()
    prompt = "\n".join(prompts)
    #print(f"Final Prompt: {prompt}\nInput: {input}")
    result = llm_call(f"{prompt}\nInput: {input}")
    elapsed = time.time() - start_time
    print(f"\nTotal elapsed time: {elapsed:.2f} seconds")
    print(f"\n{result}")
    return result

data_processing_steps = [
    """Extract only the numerical values and their associated metrics from the text.
    Format each as 'value: metric' on a new line.
    Example format:
    92: customer satisfaction
    45%: revenue growth""",
    
    """Convert all numerical values to percentages where possible.
    If not a percentage or points, convert to decimal (e.g., 92 points -> 92%).
    Keep one number per line.
    Example format:
    92%: customer satisfaction
    45%: revenue growth""",
    
    """Sort all lines in descending order by numerical value.
    Keep the format 'value: metric' on each line.
    Example:
    92%: customer satisfaction
    87%: employee satisfaction""",
    
    """Format the sorted data as a markdown table with columns:
    | Metric | Value |
    |:--|--:|
    | Customer Satisfaction | 92% |"""
]

report = """
Q3 Performance Summary:
Our customer satisfaction score rose to 92 points this quarter.
Revenue grew by 45% compared to last year.
Market share is now at 23% in our primary market.
Customer churn decreased to 5% from 8%.
New user acquisition cost is $43 per user.
Product adoption rate increased to 78%.
Employee satisfaction is at 87 points.
Operating margin improved to 34%.
"""

print("<---Chained--->")
formatted_result = chain(report, data_processing_steps)
print("<---Unchained--->")
formatted_result = unchain(report, data_processing_steps)
