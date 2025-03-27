import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.deepseek_service import DeepSeekService

async def test_date_context():
    # Initialize services
    openai_service = OpenAIService()
    deepseek_service = DeepSeekService()
    
    # Test OpenAI date context
    print('Testing OpenAI date context...')
    query = 'What is the latest price of Bitcoin?'
    api_plan = await openai_service.analyze_query(query, 'test_session')
    print(json.dumps(api_plan, indent=2))
    
    # Test DeepSeek date context
    print('\nTesting DeepSeek date context...')
    # Create sample data
    mock_data = {
        "perplexity_sonar": {
            "choices": [
                {
                    "message": {
                        "content": "Bitcoin is currently trading at approximately $82,450."
                    }
                }
            ]
        }
    }
    
    # Format data for DeepSeek
    formatted_data = deepseek_service._format_data_for_prompt_simplified(mock_data)
    print(f"Formatted data with date context:\n{formatted_data}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_date_context()) 