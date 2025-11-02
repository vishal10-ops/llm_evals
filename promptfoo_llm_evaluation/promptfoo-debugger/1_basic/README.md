# Basic Promptfoo Testing Setup

This basic setup demonstrates how to test simple AI responses for common PayPal customer service scenarios. It focuses on catching obvious response failures like inappropriate reactions to serious issues (scams, fraud, account compromise).

## Configuration
The `promptfooconfig.yaml` in this directory contains:
- Basic test cases for common customer issues
- Single provider setup (OpenAI)
- Simple pass/fail assertions

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
- Basic response appropriateness
- Simple sentiment matching
- Fundamental error detection

This setup helps catch obvious AI response failures like responding "Great!" to reports of fraud or scams.