from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable
from util import llm_call, extract_xml, log_to_file, time_invocation

ROUTE_LOG_FILE = "./logs/basic_workflows_route_routing.log"
SINGLE_AGENT_LOG_FILE = "./logs/basic_workflows_route_single_agent.log"

def route(input: str, routes: Dict[str, str], log_file: str, singleAgent: bool = False, routingLogging: bool = False) -> str:
    """Route input to specialized prompt using content classification."""

    if singleAgent:
        # Use a single agent with a comprehensive prompt
        return llm_call(f"{single_agent_prompt}\nInput: {input}")
    
    # First determine appropriate route using LLM with chain-of-thought
    if routingLogging:
        log_to_file(log_file, f"\nAvailable routes: {list(routes.keys())}")
    selector_prompt = f"""
    Analyze the input and select the most appropriate support team from these options: {list(routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>

    Input: {input}""".strip()
    
    route_response = llm_call(selector_prompt)
    reasoning = extract_xml(route_response, 'reasoning')
    route_key = extract_xml(route_response, 'selection').strip().lower()
    
    if routingLogging:
        log_to_file(log_file, "Routing Analysis:")
        log_to_file(log_file, reasoning)
        log_to_file(log_file, f"\nSelected route: {route_key}")
    
    # Process input with selected specialized prompt
    selected_prompt = routes[route_key]
    return llm_call(f"{selected_prompt}\nInput: {input}")

support_routes = {
    "billing": """You are a billing support specialist. Follow these guidelines:
    1. Always start with "Billing Support Response:"
    2. First acknowledge the specific billing issue
    3. Explain any charges or discrepancies clearly
    4. List concrete next steps with timeline
    5. End with payment options if relevant
    
    Keep responses professional but friendly.
    
    Input: """,
    
    "technical": """You are a technical support engineer. Follow these guidelines:
    1. Always start with "Technical Support Response:"
    2. List exact steps to resolve the issue
    3. Include system requirements if relevant
    4. Provide workarounds for common problems
    5. End with escalation path if needed
    
    Use clear, numbered steps and technical details.
    
    Input: """,
    
    "account": """You are an account security specialist. Follow these guidelines:
    1. Always start with "Account Support Response:"
    2. Prioritize account security and verification
    3. Provide clear steps for account recovery/changes
    4. Include security tips and warnings
    5. Set clear expectations for resolution time
    
    Maintain a serious, security-focused tone.
    
    Input: """,
    
    "product": """You are a product specialist. Follow these guidelines:
    1. Always start with "Product Support Response:"
    2. Focus on feature education and best practices
    3. Include specific examples of usage
    4. Link to relevant documentation sections
    5. Suggest related features that might help
    
    Be educational and encouraging in tone.
    
    Input: """
}

single_agent_prompt = """

    You are a powerful agent capable of dealing with many different types of support tickets.

    For billing support, follow these guidelines:
    1. Always start with "Billing Support Response:"
    2. First acknowledge the specific billing issue
    3. Explain any charges or discrepancies clearly
    4. List concrete next steps with timeline
    5. End with payment options if relevant
    
    Keep responses professional but friendly.
    
    For technical support, follow these guidelines:
    1. Always start with "Technical Support Response:"
    2. List exact steps to resolve the issue
    3. Include system requirements if relevant
    4. Provide workarounds for common problems
    5. End with escalation path if needed
    
    Use clear, numbered steps and technical details.
    
    For account security queries, follow these guidelines:
    1. Always start with "Account Support Response:"
    2. Prioritize account security and verification
    3. Provide clear steps for account recovery/changes
    4. Include security tips and warnings
    5. Set clear expectations for resolution time
    
    Maintain a serious, security-focused tone.

    For product queries, follow these guidelines:
    1. Always start with "Product Support Response:"
    2. Focus on feature education and best practices
    3. Include specific examples of usage
    4. Link to relevant documentation sections
    5. Suggest related features that might help
    
    Be educational and encouraging in tone.
    """

# Test with different support tickets
tickets = [
    """Subject: Can't access my account
    Message: Hi, I've been trying to log in for the past hour but keep getting an 'invalid password' error. 
    I'm sure I'm using the right password. Can you help me regain access? This is urgent as I need to 
    submit a report by end of day.
    - John""",
    
    """Subject: Unexpected charge on my card
    Message: Hello, I just noticed a charge of $49.99 on my credit card from your company, but I thought
    I was on the $29.99 plan. Can you explain this charge and adjust it if it's a mistake?
    Thanks,
    Sarah""",
    
    """Subject: How to export data?
    Message: I need to export all my project data to Excel. I've looked through the docs but can't
    figure out how to do a bulk export. Is this possible? If so, could you walk me through the steps?
    Best regards,
    Mike"""
]

log_to_file(ROUTE_LOG_FILE, "Processing support tickets using routing...\n")
for i, ticket in enumerate(tickets, 1):
    log_to_file(ROUTE_LOG_FILE, f"\nTicket {i}:")
    log_to_file(ROUTE_LOG_FILE, "-" * 40)
    log_to_file(ROUTE_LOG_FILE, ticket)
    log_to_file(ROUTE_LOG_FILE, "\nResponse:")
    log_to_file(ROUTE_LOG_FILE, "-" * 40)
    response =  time_invocation(ROUTE_LOG_FILE, lambda: route(ticket, support_routes, ROUTE_LOG_FILE))
    log_to_file(ROUTE_LOG_FILE, response)
    log_to_file(ROUTE_LOG_FILE, "+" * 80)

log_to_file(SINGLE_AGENT_LOG_FILE, "Processing support tickets using single agent...\n")
for i, ticket in enumerate(tickets, 1):
    log_to_file(SINGLE_AGENT_LOG_FILE, f"\nTicket {i}:")
    log_to_file(SINGLE_AGENT_LOG_FILE, "-" * 40)
    log_to_file(SINGLE_AGENT_LOG_FILE, ticket)
    log_to_file(SINGLE_AGENT_LOG_FILE, "\nResponse:")
    log_to_file(SINGLE_AGENT_LOG_FILE, "-" * 40)
    response = time_invocation(SINGLE_AGENT_LOG_FILE, lambda: route(ticket, support_routes, SINGLE_AGENT_LOG_FILE, True))
    log_to_file(SINGLE_AGENT_LOG_FILE, response)
    log_to_file(SINGLE_AGENT_LOG_FILE, "+" * 80)
