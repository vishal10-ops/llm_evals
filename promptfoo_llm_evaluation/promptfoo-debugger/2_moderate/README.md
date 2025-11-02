# Moderate Promptfoo Testing Setup

This intermediate setup expands on basic testing by introducing more complex scenarios and multiple test variations for PayPal customer service responses.

## Configuration
The `promptfooconfig.yaml` includes:
- Multiple test cases with varying complexity
- Custom provider settings (temperature, max tokens)
- Response validation rules
- Basic sentiment analysis

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
- Response appropriateness across different scenarios
- Handling of complex customer issues
- Consistent tone and empathy
- Basic security awareness
- Multiple response variations

This setup helps ensure AI responses are both appropriate and helpful across a range of customer service scenarios, with particular attention to security-sensitive situations like fraud reports.