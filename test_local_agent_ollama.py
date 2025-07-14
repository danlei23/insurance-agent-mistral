from agents.insurance_agent_mistral import InsuranceAgent

agent = InsuranceAgent(config={})

print("Ask a coverage question:")
user_query = input("> ")

result = agent.process_message(user_query)

print("\n=== Agent Response ===")
print(result["response"])
