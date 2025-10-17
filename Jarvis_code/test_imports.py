def test_imports():
    modules = [
        'langchain',
        'langchain.tools',
        'livekit',
        'livekit.agents',
        'livekit.plugins',
        'livekit.plugins.google',
        'livekit.plugins.noise_cancellation',
        'Jarvis_prompts',
        'Jarvis_google_search',
        'memory_loop',
        'jarvis_reasoning',
        'fuzzywuzzy'  # Add this to verify our compatibility layer
    ]
    
    for module in modules:
        try:
            imported = __import__(module)
            print(f"✅ {module}")
            if module == 'fuzzywuzzy':
                # Verify key functions exist
                assert all(hasattr(imported, attr) for attr in ['ratio', 'partial_ratio', 'extract'])
        except ImportError as e:
            print(f"❌ {module}: {str(e)}")
        except AssertionError:
            print(f"❌ {module}: missing required functions")

if __name__ == "__main__":
    test_imports()