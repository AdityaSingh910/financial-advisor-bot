"""
Agent 2: Risk Analysis Agent
Evaluates financial risk factors based on the user's query
and the retrieved context from Agent 1.
Uses Groq API with Llama 3.3 for fast, free inference.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


RISK_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Financial Risk Analyst AI Agent working at a major financial consulting firm.

Your role is to analyze the financial risk factors related to the user's query based on the retrieved context.

INSTRUCTIONS:
1. Identify the type of financial decision the user is considering
2. List the key risk factors (market risk, credit risk, interest rate risk, inflation risk, liquidity risk, etc.)
3. Provide a risk rating (Low / Moderate / High / Critical) with justification
4. Highlight any red flags or warnings
5. Be specific with numbers and data from the provided context

OUTPUT FORMAT (strictly follow this):
**Risk Category:** [type of financial risk]
**Overall Risk Level:** [Low/Moderate/High/Critical]

**Key Risk Factors:**
1. [Risk factor with explanation]
2. [Risk factor with explanation]
3. [Risk factor with explanation]

**Risk Mitigation Suggestions:**
- [Suggestion 1]
- [Suggestion 2]

**⚠️ Warnings:**
- [Any critical warnings or red flags]

Keep your analysis concise but thorough. Use data from the context to support your assessment.
"""),
    ("human", """User Query: {query}

Retrieved Financial Context:
{context}

Provide your risk analysis:"""),
])


def analyze_risk(query: str, context: str, api_key: str) -> dict:
    """
    Analyze financial risks related to the user's query.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3,
        max_tokens=1024,
    )

    chain = RISK_ANALYSIS_PROMPT | llm

    response = chain.invoke({
        "query": query,
        "context": context,
    })

    return {
        "agent": "Risk Analyst",
        "status": "completed",
        "analysis": response.content,
    }
