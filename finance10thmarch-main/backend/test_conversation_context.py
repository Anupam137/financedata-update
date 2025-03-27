"""
Test script to debug conversation context issues
"""
import asyncio
import uuid
from app.services.openai_service import OpenAIService

async def test_conversation_context():
    """
    Test the conversation context handling
    """
    print("Starting conversation context test...")
    
    # Create a session ID
    session_id = str(uuid.uuid4())
    print(f"Created session ID: {session_id}")
    
    # Create an OpenAI service
    openai_service = OpenAIService()
    
    # First query about NVDA
    first_query = "What's the sentiment around NVDA?"
    print(f"\n--- First query: '{first_query}' ---")
    
    # Add the first query to conversation history
    openai_service.add_to_conversation(session_id, "user", first_query)
    
    # Simulate a response
    first_response = """
    Market Sentiment for NVIDIA (NVDA)
    The sentiment around NVIDIA Corporation (NVDA) is currently mixed with various factors influencing investor perception:
    
    Positive Sentiment:
    Analyst Optimism: Analysts are generally bullish on NVIDIA, citing its strong potential in AI and other technology sectors.
    Growth Prospects: NVIDIA is recognized for its growth potential, particularly in AI and cloud computing spaces.
    
    Negative Sentiment:
    Investor Caution: Macroaxis reports that a significant portion of NVIDIA's investor base is inclined towards shorting the stock.
    Market Volatility: Recent underwhelming earnings reports and increased competition have led to some negativity.
    
    Conclusion
    While NVIDIA faces some short-term challenges and market volatility, the overall long-term sentiment remains positive due to its strategic position in high-growth areas like AI and cloud computing.
    """
    
    # Add the response to conversation history
    openai_service.add_to_conversation(session_id, "assistant", first_response)
    
    # Print the conversation history
    history = openai_service.get_conversation_history(session_id)
    print(f"Conversation history after first exchange: {len(history)} messages")
    
    # Second query about analyst ratings
    second_query = "What are the latest analyst ratings and price targets"
    print(f"\n--- Second query: '{second_query}' ---")
    
    # Add the second query to conversation history
    openai_service.add_to_conversation(session_id, "user", second_query)
    
    # Test the analyze_query method
    print("\nTesting analyze_query method...")
    api_plan = await openai_service.analyze_query(second_query, session_id)
    print(f"API plan: {api_plan}")
    
    # Test the generate_financial_insight method
    print("\nTesting generate_financial_insight method...")
    dummy_data = {"dummy": "data"}
    insight = await openai_service.generate_financial_insight(second_query, dummy_data, session_id)
    print(f"Generated insight: {insight[:200]}...")
    
    print("\nTest completed.")

if __name__ == "__main__":
    asyncio.run(test_conversation_context()) 