# Advanced Promptfoo Testing Setup

This advanced configuration demonstrates comprehensive testing of AI responses for PayPal's customer service scenarios, with a focus on empathy, security, and response appropriateness.

## Directory Structure
```
3_advance/
├── prompts/                 # Different prompt variations
├── providers/              # Provider configurations
└── tests/                  # Test cases and metrics
```

## Configuration
The setup includes:
- Multiple prompt variations (empathetic vs direct)
- Different provider temperature settings
- Comprehensive test metrics
- Advanced assertion testing
- Custom evaluation criteria

## Getting Started

1. Set your API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
   Or add it to your `.env` file

2. Run the tests:
   ```bash
   promptfoo eval
   ```

3. View results:
   ```bash
   promptfoo view
   ```

## What This Tests
- Response empathy levels
- Security awareness
- Handling of critical situations (fraud, scams, account compromise)
- Consistent tone across different scenarios
- Response appropriateness
- Language and cultural sensitivity
- Edge cases and complex scenarios

This advanced setup ensures comprehensive testing of AI responses, preventing inappropriate responses like the "Great!" response to scam reports, while maintaining appropriate empathy levels across all customer interactions.