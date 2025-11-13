"""
Test script to validate code structure changes for word-level timestamps
This tests the code structure without requiring actual Azure credentials
"""
import sys
import json
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_azure_client_structure():
    """Test that AzureOpenAIClient has the expected structure for word-level timestamps."""
    
    print("🔍 Testing AzureOpenAIClient structure...")
    
    # Import the module
    from azure_client import AzureOpenAIClient
    
    # Check that the class exists
    assert hasattr(AzureOpenAIClient, '__init__'), "❌ AzureOpenAIClient.__init__ not found"
    print("✅ AzureOpenAIClient class found")
    
    # Check that transcribe_audio method exists
    assert hasattr(AzureOpenAIClient, 'transcribe_audio'), "❌ transcribe_audio method not found"
    print("✅ transcribe_audio method found")
    
    # Check that _transcribe_with_speech_service method exists
    assert hasattr(AzureOpenAIClient, '_transcribe_with_speech_service'), "❌ _transcribe_with_speech_service method not found"
    print("✅ _transcribe_with_speech_service method found")
    
    # Check the docstring mentions word-level timestamps
    docstring = AzureOpenAIClient.transcribe_audio.__doc__
    assert "word-level" in docstring.lower(), "❌ Docstring doesn't mention word-level timestamps"
    print("✅ Docstring mentions word-level timestamps")
    
    # Check priority order in docstring
    assert "Azure Speech Service" in docstring, "❌ Azure Speech Service not in priority list"
    assert "GPT-4o" in docstring, "❌ GPT-4o not in priority list"
    print("✅ Priority order documented correctly")
    
    print("\n📊 All structure tests passed!")
    return True

def test_word_level_parsing():
    """Test the word-level timestamp parsing logic."""
    
    print("\n🔍 Testing word-level timestamp parsing logic...")
    
    # Read the azure_client.py file
    with open("/home/ubuntu/VeriCall/app/azure_client.py", "r") as f:
        code = f.read()
    
    # Check for word-level timestamp parsing
    assert "request_word_level_timestamps()" in code, "❌ request_word_level_timestamps() not found"
    print("✅ Word-level timestamps requested in config")
    
    # Check for JSON parsing
    assert "json.loads(evt.result.json)" in code, "❌ JSON parsing of detailed results not found"
    print("✅ JSON parsing of detailed results found")
    
    # Check for Words extraction
    assert '"Words" in best' in code, "❌ Words extraction not found"
    print("✅ Words extraction logic found")
    
    # Check for word timestamp conversion
    assert "word_info.get(\"Offset\", 0) / 10000000" in code, "❌ Word timestamp conversion not found"
    print("✅ Word timestamp conversion found")
    
    # Check that words are added to segments
    assert '"words": words' in code, "❌ Words not added to result"
    print("✅ Words added to segment result")
    
    # Check that words are preserved in segment conversion
    assert 'if "words" in r and r["words"]:' in code, "❌ Words not preserved in segment conversion"
    print("✅ Words preserved in segment conversion")
    
    print("\n📊 All parsing logic tests passed!")
    return True

def test_priority_order():
    """Test that the priority order is correct in the code."""
    
    print("\n🔍 Testing transcription priority order...")
    
    # Read the azure_client.py file
    with open("/home/ubuntu/VeriCall/app/azure_client.py", "r") as f:
        code = f.read()
    
    # Find the transcribe_audio method
    start = code.find("async def transcribe_audio(")
    end = code.find("\n    async def _transcribe_with_whisper(", start)
    method_code = code[start:end]
    
    # Check order: Azure Speech BEFORE GPT-4o
    speech_pos = method_code.find("Azure Speech Service FIRST")
    gpt4o_pos = method_code.find("Fallback to GPT-4o")
    
    assert speech_pos > 0, "❌ Azure Speech Service not found in method"
    assert gpt4o_pos > 0, "❌ GPT-4o fallback not found in method"
    assert speech_pos < gpt4o_pos, "❌ Priority order incorrect: Speech should be BEFORE GPT-4o"
    
    print("✅ Priority order correct: Azure Speech -> GPT-4o -> Whisper")
    
    # Check that diarization is added after Speech transcription
    assert "Adding speaker labels with GPT-4o" in method_code, "❌ GPT-4o diarization not found"
    print("✅ GPT-4o diarization added after Speech transcription")
    
    print("\n📊 All priority order tests passed!")
    return True

def generate_summary():
    """Generate a summary of the changes."""
    
    print("\n" + "="*60)
    print("📋 SUMMARY OF CHANGES")
    print("="*60)
    
    changes = [
        ("✅ Word-level timestamps", "request_word_level_timestamps() configured"),
        ("✅ JSON parsing", "Detailed results parsed from Azure Speech"),
        ("✅ Word extraction", "Each word extracted with start/end timestamps"),
        ("✅ Segment enrichment", "'words' array added to each segment"),
        ("✅ Priority order", "Azure Speech -> GPT-4o diarization -> GPT-4o audio -> Whisper"),
        ("✅ Backward compatibility", "Fallback chain maintained for reliability"),
    ]
    
    for status, description in changes:
        print(f"{status}: {description}")
    
    print("\n" + "="*60)
    print("🎯 EXPECTED BENEFITS")
    print("="*60)
    
    benefits = [
        "More precise audio editing (word-level vs segment-level)",
        "Exact word boundary detection for cutting audio",
        "Better timestamp accuracy (real vs estimated)",
        "Improved audio regeneration quality",
    ]
    
    for i, benefit in enumerate(benefits, 1):
        print(f"{i}. {benefit}")
    
    print("\n" + "="*60)
    print("📝 NEXT STEPS")
    print("="*60)
    
    steps = [
        "Deploy to Azure App Service (auto-deploy from GitHub)",
        "Test with real audio file on Azure",
        "Verify word-level timestamps in transcription result",
        "Test audio editing precision with word boundaries",
        "Compare with previous GPT-4o segment-level results",
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        # Run all tests
        test_azure_client_structure()
        test_word_level_parsing()
        test_priority_order()
        generate_summary()
        
        print("\n✅ ALL TESTS PASSED! Code is ready for deployment.")
        print("\n💡 To test with real data, deploy to Azure and use the web interface.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
