# Promptfoo Debugger

A comprehensive guide to debugging and troubleshooting Promptfoo test configurations when YAML files are misconfigured or tests fail unexpectedly.

## Overview

This directory contains progressively complex examples designed to help you identify, diagnose, and fix common issues in Promptfoo test configurations. Whether you're dealing with YAML syntax errors, provider connection issues, or assertion failures, these examples provide practical debugging strategies.

## Directory Structure

```
promptfoo-debugger/
├── 1_basic/           # Simple configurations - learn fundamentals
├── 2_moderate/        # Intermediate complexity - common patterns
├── 3_advance/         # Complex setups - multiple files and providers
└── README.md          # This file
```

## Common Issues & How to Debug

### 1. YAML Configuration Errors

#### Indentation Problems
YAML is whitespace-sensitive. Common mistakes:

```yaml
# ❌ WRONG - Inconsistent indentation
prompts:
- You are a helper
  providers:
  - openai:gpt-4

# ✅ CORRECT - Consistent indentation (2 spaces)
prompts:
  - You are a helper

providers:
  - openai:gpt-4
```

**How to debug:**
- Use a YAML validator (most code editors have built-in validation)
- Check that all nested items are indented consistently
- Ensure lists (`-`) are properly aligned

#### File Reference Errors
```yaml
# ❌ WRONG - File doesn't exist or path is incorrect
prompts:
  - file://prompt/my_prompt.txt  # Typo in directory name

# ✅ CORRECT - Verify file paths exist
prompts:
  - file://prompts/my_prompt.txt
```

**How to debug:**
- Verify all file paths relative to the config file location
- Check for typos in filenames and extensions
- Ensure referenced files actually exist

### 2. Provider Configuration Issues

#### Missing API Keys
```
Error: API call error: Error: Request failed - Invalid API key
```

**How to debug:**
- Check if environment variables are set: `echo $OPENAI_API_KEY`
- Verify `.env` file exists and is in the correct location
- Ensure API key format is correct (no extra spaces/quotes)

#### Connection Errors
```
Error: connect ECONNREFUSED 127.0.0.1:1234
```

**How to debug:**
- Check if the provider endpoint is correct
- Verify local servers are running (for custom providers)
- Test API connectivity with a simple curl command
- Review `promptfoo-errors.log` for detailed error messages

#### Provider Naming Issues
```yaml
# ❌ WRONG - Invalid provider name
providers:
  - id: openai:gpt-6 # GPT-6 doesn't exist yet

# ✅ CORRECT - Valid provider name
providers:
  - id: openai:gpt-4
```

**How to debug:**
- Check [Promptfoo documentation](https://www.promptfoo.dev/docs/providers/) for valid provider names
- Verify model availability for your API tier
- Test provider separately before adding to config

### 3. Test Assertion Problems

#### Type Mismatches
```yaml
# ❌ WRONG - Using wrong assertion type
tests:
  - vars:
      message: "Hello"
    assert:
      - type: contains-any
        value: "hello"  # Should be an array, not a string

# ✅ CORRECT - Proper assertion format
tests:
  - vars:
      message: "Hello"
    assert:
      - type: contains-any
        value: ["hello", "hi", "hey"]
```

**Common assertion types:**
- `contains`: Checks if output contains a specific string
- `contains-any`: Checks if output contains any item from a list
- `not-contains`: Checks if output does NOT contain a string
- `not-contains-any`: Checks if output does NOT contain any item from a list
- `regex`: Matches against a regular expression
- `is-json`: Validates JSON structure
- `similarity`: Semantic similarity check

#### Variable Substitution Issues
```yaml
# ❌ WRONG - Variable name mismatch
prompts:
  - "Respond to: {{user_message}}"

tests:
  - vars:
      message: "Hello"  # Variable name doesn't match

# ✅ CORRECT - Variable names must match
prompts:
  - "Respond to: {{message}}"

tests:
  - vars:
      message: "Hello"
```

**How to debug:**
- Ensure variable names in prompts match those in test vars
- Check for typos in variable names (case-sensitive)
- Use consistent naming conventions

### 4. Performance & Timeout Issues

#### Slow Test Execution
```yaml
# Add timeout configuration
providers:
  - id: openai:gpt-4
    config:
      temperature: 0.7
      max_tokens: 150  # Limit tokens to speed up tests
      timeout: 30000   # 30 second timeout
```

**How to debug:**
- Set appropriate `max_tokens` limits
- Configure reasonable timeout values
- Check network connectivity
- Monitor API rate limits

### 5. Complex Configuration Debugging

#### Multiple File References
When using file references (like in `3_advance/`):

```yaml
prompts:
  - file://prompts/empathetic_assistant.txt

providers:
  - file://providers/providers_temp_0.7.yaml

tests:
  - file://tests/empathetic_test.yaml
```

**How to debug:**
- Test each file independently first
- Verify file paths are relative to the config file
- Check that each referenced file has valid YAML
- Look for circular dependencies

## Debugging Workflow

### Step 1: Validate YAML Syntax
```bash
# Use a YAML validator
npm install -g yaml-validator
yaml-validator promptfooconfig.yaml
```

### Step 2: Test Provider Connection
```bash
# Set environment variable
export OPENAI_API_KEY=your_key_here

# Run a simple test
promptfoo eval --no-cache
```

### Step 3: Run with Verbose Output
```bash
# Enable debug mode for detailed logs
export DEBUG=promptfoo*
promptfoo eval
```

### Step 4: Check Error Logs
```bash
# Review error logs (created in your directory)
cat promptfoo-errors.log
```

### Step 5: Isolate the Problem
- Comment out sections of your config
- Test with minimal configuration first
- Gradually add complexity back

### Step 6: View Results
```bash
# Open the web UI to inspect results
promptfoo view
```

## Progressive Learning Path

### Start Here: Basic (1_basic/)
- Simple single-provider setup
- Basic assertion types
- Foundation for debugging skills

**Key learning:**
- YAML structure basics
- Simple test cases
- Provider configuration
- Basic assertion syntax

### Next: Moderate (2_moderate/)
- Multiple providers
- More complex assertions
- Provider configuration options

**Key learning:**
- Provider comparison
- Multiple test scenarios
- Custom provider settings
- Assertion combinations

### Advanced: Complex (3_advance/)
- Multiple file references
- Separate prompts, providers, and tests
- Production-ready patterns

**Key learning:**
- Modular configuration
- File organization best practices
- Complex test scenarios
- Error log analysis

## Common Error Messages & Solutions

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| `YAML parse error` | Invalid YAML syntax | Check indentation, quotes, colons |
| `Cannot find module` | File path incorrect | Verify file paths are correct |
| `Invalid API key` | Missing or wrong API key | Set environment variable correctly |
| `ECONNREFUSED` | Provider not accessible | Check connection, port, endpoint |
| `Assertion failed` | Test expectations not met | Review test logic and expected outputs |
| `Variable not found` | Variable name mismatch | Ensure prompt and test vars match |
| `Timeout` | Request taking too long | Increase timeout or reduce max_tokens |

## Best Practices for Debugging

1. **Start Simple**: Begin with basic configurations and add complexity gradually
2. **Use Version Control**: Track changes to identify what broke
3. **Comment Liberally**: Document why certain configurations exist
4. **Test Incrementally**: Add one test at a time
5. **Check Logs**: Review `promptfoo-errors.log` for detailed errors
6. **Validate YAML**: Use a YAML linter before running tests
7. **Isolate Issues**: Comment out sections to narrow down problems
8. **Use Explicit Values**: Avoid implicit defaults when debugging

## Environment Setup Checklist

- [ ] Promptfoo installed (`npm install -g promptfoo`)
- [ ] API keys set as environment variables
- [ ] `.env` file created (if using one)
- [ ] All referenced files exist in correct locations
- [ ] YAML files validated for syntax
- [ ] Provider endpoints accessible
- [ ] Internet connection available (for cloud providers)

## Useful Commands

```bash
# Initialize new config
promptfoo init

# Run tests
promptfoo eval

# Run with fresh cache
promptfoo eval --no-cache

# View results in browser
promptfoo view

# List available providers
promptfoo providers

# Validate config (doesn't run tests)
promptfoo eval --dry-run

# Run specific test file
promptfoo eval -c path/to/promptfooconfig.yaml

# Export results to JSON
promptfoo eval --output results.json
```

## Additional Resources

- [Promptfoo Documentation](https://www.promptfoo.dev/docs/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [Promptfoo Assertions Reference](https://www.promptfoo.dev/docs/configuration/expected-outputs/)
- [Provider Configuration Guide](https://www.promptfoo.dev/docs/providers/)

## Getting Help

1. Check the example configs in this directory
2. Review error logs in `promptfoo-errors.log`
3. Consult Promptfoo documentation
4. Search GitHub issues for similar problems
5. Join the Promptfoo community Discord

---

**Remember**: Debugging is an iterative process. Start with the basics, validate each component, and build up complexity gradually. Most issues are configuration-related and can be resolved by careful attention to YAML syntax and file paths.

