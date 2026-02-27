# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
import yfinance as yf  # Library to fetch real web stock data
from typing import Optional, Any

# =====================================================================
# 1. CALLBACK DEFINITIONS
# =====================================================================


# Informational Disclaimer Callback: Ensures the disclaimer is shown before any analysis
def enforce_disclaimer(callback_context: CallbackContext) -> Optional[types.Content]:
    if not callback_context.state.get("disclaimer_shown"):
        callback_context.state["disclaimer_shown"] = True
        return types.Content(
            role="model",
            parts=[types.Part(text="### ⚠️ Legal Disclaimer: this is for informational and educational purposes only.\nPlease consult a financial advisor before making any investment decisions. ⚠️\n\n which ticker would you like to analyze?")],
        )
    return None

# Cache Callback: Serves a static analysis for GOOGL to demonstrate caching
async def cache_googl_analysis(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    current_query = callback_context.user_content
    text = current_query.parts[0].text.upper() if current_query and current_query.parts else ""
    
    if "GOOGL" in text:
        print("[Cache Hit] Serving static GOOGL report...")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="**GOOGL Analysis (Cached):\n** High growth in AI/Cloud...")]
            )
        )
    return None

# Tool Callback: Blocks analysis of certain cryptocurrencies to demonstrate tool-level control
def block_crypto_tool(tool, args: dict[str, Any], tool_context: ToolContext) -> Optional[dict]:
    
    # Update the reference here as well
    ticker = args.get("ticker", "").upper()
    
    if ticker in ["BTC", "ETH", "DOGE"]:
        print(f"[TOOL BLOCKED] Cannot analyze crypto: {ticker}")
        return {"error": "Crypto analysis is restricted by company policy."}
    return None

# =====================================================================
# 2. REAL WEB-FETCHING TOOL
# =====================================================================

def fetch_real_market_data(ticker: str) -> dict:
    """Fetches real-time stock data from the web for a given ticker."""
    print(f"--- 🛠️ Fetching real web data for {ticker} ---")
    try:
        # Use yfinance to pull real data from the web
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "ticker": ticker,
            "current_price": info.get("currentPrice", "Data unavailable"),
            "industry": info.get("industry", "Unknown"),
            "summary": info.get("longBusinessSummary", "No summary available")[:500] + "..."
        }
    except Exception as e:
        return {"error": f"Failed to fetch data from the web: {str(e)}"}

# =====================================================================
# 3. AGENT REGISTRATION
# =====================================================================

data_analyst = LlmAgent(
    name="data_analyst",
    model="gemini-2.5-flash",
    description="Analyzes real market data for tickers.",
    # Instruct the sub-agent to act as a silent worker:
    instruction="""
    Use the fetch_real_market_data tool to pull live data. 
    Do NOT summarize the findings to the user directly. 
    Once you have the data, use the transfer_to_agent tool to transfer control back to 'pro_advisor'.
    """,
    tools=[fetch_real_market_data],
    before_model_callback=cache_googl_analysis,
    before_tool_callback=block_crypto_tool
)

pro_advisor = LlmAgent(
    name="pro_advisor",
    model="gemini-2.5-flash",
    # Pro Advisor has baton back:
    instruction="""
    Coordinate with your analyst to help the user with financial questions. 
    step 1. Ask the user for a stock ticker they want to analyze.
    step 2. run the data_analyst sub-agent to fetch the data. 
    step 3. When data_analyst transfers control back to you, summarize its findings for the user. 
    step 4. IMPORTANT!!!! ALWAYS ask the user if they have follow-up questions or another ticker to analyze. 
    """,
    sub_agents=[data_analyst],
    before_agent_callback=enforce_disclaimer
)


root_agent = pro_advisor
