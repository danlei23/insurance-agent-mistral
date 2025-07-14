import json
import re
import requests
from typing import Dict, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[Dict], add_messages]
    user_input: str
    intent: str
    analysis_result: Dict
    error: str
    response: str

class InsuranceAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        workflow.add_node("classify_intent", self._classify_intent)
        workflow.add_node("policy_query", self._policy_query_node)
        workflow.add_node("format_response", self._format_response)

        workflow.set_entry_point("classify_intent")
        workflow.add_conditional_edges(
            "classify_intent",
            self._route_intent,
            {
                "policy_query": "policy_query",
                "error": END
            }
        )
        workflow.add_edge("policy_query", "format_response")
        workflow.add_edge("format_response", END)
        return workflow.compile()

    def _classify_intent(self, state: AgentState) -> AgentState:
        user_input = state["user_input"].lower()
        state["intent"] = "policy_query"
        return state

    def _route_intent(self, state: AgentState) -> str:
        if state.get("error"):
            return "error"
        return state["intent"]

    def _policy_query_node(self, state: AgentState) -> AgentState:
        try:
            policy_content = self._mock_retrieve_policy()
            
            prompt = f"""
    You are an insurance expert. Your job is to determine if the situation described in the question is covered by the policy below.

    Answer in **valid JSON only**. Format:
    {{
    "covered": true/false,
    "explanation": "...",
    "deductible": "$1000"
    }}

    Do not guess. Use only the policy text to justify your answer.

    Question: {state["user_input"]}
    Policy:
    {policy_content}
    """
            response = self._call_mistral_ollama(prompt)
            state["analysis_result"] = response

        except Exception as e:
            state["error"] = str(e)

        return state


    def _format_response(self, state: AgentState) -> AgentState:
        result = state.get("analysis_result", {})
        if result.get("covered") is True:
            state["response"] = f"✅ **Covered**\n\n{result.get('explanation')}\n\n**Deductible:** {result.get('deductible')}"
        elif result.get("covered") is False:
            state["response"] = f"❌ **Not Covered**\n\n{result.get('explanation')}"
        else:
            state["response"] = f"❓ Unable to determine coverage."
        return state

    def _mock_retrieve_policy(self) -> str:
        with open("example_policy.txt", "r") as f:
            return f.read()

    def _call_mistral_ollama(self, prompt: str) -> Dict:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        output = res.json()["response"]
        try:
            json_match = re.search(r'{.*}', output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception:
            pass
        return {"response": output}
    
    def process_message(self, user_input: str, conversation_history: List[Dict] = None) -> Dict:
        initial_state = {
            "messages": conversation_history or [],
            "user_input": user_input,
            "intent": "",
            "analysis_result": {},
            "error": "",
            "response": ""
        }
        final_state = self.workflow.invoke(initial_state)
        final_state["messages"].extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": final_state["response"]}
        ])
        return {
            "success": not bool(final_state.get("error")),
            "response": final_state["response"],
            "messages": final_state["messages"],
            "intent": final_state.get("intent", "unknown")
        }

