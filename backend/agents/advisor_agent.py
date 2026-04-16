"""
Agent 3: Financial Advisor Agent
Generates a comprehensive, user-friendly financial advisory response
combining retrieved context and risk analysis.
Uses Groq API with Llama 3.3 for fast, free inference.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


ADVISOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Financial Advisor AI Agent at a leading financial consulting firm.

Your role is to provide clear, actionable, and comprehensive financial advice to the user based on:
1. The retrieved financial data and guidelines
2. The risk analysis performed by the Risk Analyst

INSTRUCTIONS:
1. Answer the user's question directly and clearly
2. Use specific data, numbers, and comparisons from the provided context
3. Structure your response logically with headers and bullet points
4. Provide actionable recommendations
5. Include relevant comparisons (e.g., interest rate comparison across banks)
6. Mention applicable tax benefits if relevant
7. Add important caveats and disclaimers
8. Use a professional but approachable tone
9. If the question is outside financial advisory scope, politely redirect

RESPONSE FORMAT:
- Start with a direct answer to the question
- Provide supporting details with data
- Include practical tips or recommendations
- End with any important disclaimers

IMPORTANT RULES:
- Always include: "⚠️ Disclaimer: This is AI-generated advisory for educational purposes. Please consult a certified financial advisor for personalized advice."
- Do NOT recommend specific stocks or guarantee returns
- Be honest about risks and uncertainties
- Use Indian financial context (₹, Indian regulations, Indian banks)
"""),
    ("human", """User Query: {query}

Retrieved Financial Context:
{context}

Risk Analysis:
{risk_analysis}

Provide your comprehensive financial advisory response:"""),
])


def generate_advice(query: str, context: str, risk_analysis: str, api_key: str) -> dict:
    """
    Generate comprehensive financial advisory response.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.5,
        max_tokens=2048,
    )

    chain = ADVISOR_PROMPT | llm

    response = chain.invoke({
        "query": query,
        "context": context,
        "risk_analysis": risk_analysis,
    })

    return {
        "agent": "Financial Advisor",
        "status": "completed",
        "advice": response.content,
    }
