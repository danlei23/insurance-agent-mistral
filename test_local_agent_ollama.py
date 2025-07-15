# Import the InsuranceAgent class from your local agent implementation
from agents.insurance_agent_mistral import InsuranceAgent


# Initialize the agent with an empty configuration
agent = InsuranceAgent(config={})


# Prompt the user to enter a question in the terminal
print("Ask a coverage question:")
user_query = input("> ") # Capture user input from terminal

# Send the input to the agent for processing
result = agent.process_message(user_query)

# Print the formatted response from the agent
print("\n=== Agent Response ===")
print(result["response"])
