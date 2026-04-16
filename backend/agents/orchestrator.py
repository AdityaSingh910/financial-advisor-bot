"""
Agent Orchestrator
Coordinates the 3-agent pipeline:
  1. Data Retriever → retrieves relevant documents from vector store
  2. Risk Analyst → evaluates financial risk factors
  3. Financial Advisor → generates comprehensive advisory response

Uses a sequential pipeline where each agent's output feeds into the next.
"""

import time
from agents.retriever_agent import retrieve
from agents.risk_agent import analyze_risk
from agents.advisor_agent import generate_advice


def run_pipeline(query: str, api_key: str) -> dict:
    """
    Run the full 3-agent advisory pipeline.
    
    Args:
        query: User's financial question
        api_key: Google API key for Gemini
        
    Returns:
        Complete pipeline result with each agent's output
    """
    pipeline_start = time.time()
    agent_trace = []
    
    # ── Agent 1: Data Retriever ──────────────────────────────
    step1_start = time.time()
    try:
        retrieval_result = retrieve(query, k=5)
        retrieval_result["duration_ms"] = int((time.time() - step1_start) * 1000)
        agent_trace.append(retrieval_result)
    except Exception as e:
        return {
            "success": False,
            "error": f"Retrieval Agent failed: {str(e)}",
            "agent_trace": agent_trace,
        }
    
    # ── Agent 2: Risk Analyst ────────────────────────────────
    step2_start = time.time()
    try:
        risk_result = analyze_risk(
            query=query,
            context=retrieval_result["context"],
            api_key=api_key,
        )
        risk_result["duration_ms"] = int((time.time() - step2_start) * 1000)
        agent_trace.append(risk_result)
    except Exception as e:
        return {
            "success": False,
            "error": f"Risk Analysis Agent failed: {str(e)}",
            "agent_trace": agent_trace,
        }
    
    # ── Agent 3: Financial Advisor ───────────────────────────
    step3_start = time.time()
    try:
        advice_result = generate_advice(
            query=query,
            context=retrieval_result["context"],
            risk_analysis=risk_result["analysis"],
            api_key=api_key,
        )
        advice_result["duration_ms"] = int((time.time() - step3_start) * 1000)
        agent_trace.append(advice_result)
    except Exception as e:
        return {
            "success": False,
            "error": f"Advisor Agent failed: {str(e)}",
            "agent_trace": agent_trace,
        }
    
    # ── Compile Result ───────────────────────────────────────
    total_duration = int((time.time() - pipeline_start) * 1000)
    
    return {
        "success": True,
        "query": query,
        "response": advice_result["advice"],
        "risk_analysis": risk_result["analysis"],
        "sources": retrieval_result["sources"],
        "chunks_retrieved": retrieval_result["chunks_retrieved"],
        "agent_trace": agent_trace,
        "total_duration_ms": total_duration,
    }
