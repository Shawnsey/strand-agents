# Gmail Email Categorization Agent - Amazon Q Development Rules

## Overview
This rule defines development guidelines and constraints for building a Gmail Email Categorization Agent using the Strands Agents framework. The agent automatically categorizes emails into predefined labels and sends periodic summaries to users.

## Project Context
- **Framework**: Strands Agents SDK
- **Model**: ChatGPT (GPT-4o) via LiteLLM
- **Gmail Integration**: @shinzolabs/gmail-mcp MCP server
- **Categories**: urgent, opportunities, junk, bills
- **Output**: Automated email summaries delivered to user inbox

## Development Rules

### 1. Architecture Requirements

#### Model Configuration
```python
# REQUIRED: Use ChatGPT with specific configuration
from strands.models.litellm import LiteLLMModel

chatgpt_model = LiteLLMModel(
    client_args={"api_key": "<OPENAI_API_KEY>"},
    model_id="gpt-4o",
    params={
        "temperature": 0.3,  # Low temperature for consistent categorization
        "max_tokens": 2000
    }
)
```

#### Gmail MCP Integration
```python
# REQUIRED: Use shinzo-labs Gmail MCP server
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

gmail_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="npx", args=["@shinzolabs/gmail-mcp"])
))
```

#### Agent Structure
```python
# REQUIRED: Agent initialization pattern
from strands import Agent

agent = Agent(
    model=chatgpt_model,
    tools=gmail_tools,  # From MCP client
    system_prompt=EMAIL_CATEGORIZATION_PROMPT
)
```

### 2. Email Categorization Rules

#### Required Categories
- **URGENT**: Time-sensitive emails requiring immediate action
  - Meeting requests, deadlines, critical updates
  - Keywords: "urgent", "asap", "deadline", "meeting", "emergency"
  
- **OPPORTUNITIES**: Business opportunities and networking
  - Job postings, business proposals, partnership inquiries
  - Keywords: "opportunity", "job", "position", "partnership", "collaboration"
  
- **JUNK**: Low-value promotional content
  - Marketing emails, newsletters, automated notifications
  - Keywords: "unsubscribe", "promotion", "sale", "newsletter"
  
- **BILLS**: Financial documents and payment requests
  - Invoices, payment reminders, account statements
  - Keywords: "invoice", "payment", "bill", "statement", "due"

#### System Prompt Template
```python
EMAIL_CATEGORIZATION_PROMPT = """
You are an intelligent email categorization assistant. Your role is to:

1. Analyze email content including subject, sender, and body text
2. Categorize emails into exactly one of these labels:
   - URGENT: Time-sensitive emails requiring immediate action
   - OPPORTUNITIES: Business opportunities, job offers, networking
   - JUNK: Spam, low-value promotional content, newsletters
   - BILLS: Invoices, payment reminders, financial statements

3. Apply appropriate Gmail labels to categorized emails
4. Generate concise summaries of email activity

Categorization Guidelines:
- URGENT: Emails with deadlines, meeting requests, critical updates
- OPPORTUNITIES: Job postings, business proposals, partnership inquiries
- JUNK: Marketing emails, newsletters, automated notifications
- BILLS: Any financial documents, payment requests, account statements

Always provide reasoning for categorization decisions.
"""
```

### 3. Gmail Label Management

#### Required Label Structure
```python
# REQUIRED: Create these specific labels
GMAIL_LABELS = {
    "Agent/Urgent": {"color": "red", "priority": "high"},
    "Agent/Opportunities": {"color": "green", "priority": "medium"},
    "Agent/Bills": {"color": "yellow", "priority": "medium"},
    "Agent/Junk": {"color": "gray", "priority": "low"}
}
```

#### Label Application Rules
- Each email must receive exactly one category label
- Use Gmail MCP `modify_message` tool to apply labels
- Log all categorization decisions for audit trail
- Handle label creation if labels don't exist

### 4. Email Summary Requirements

#### Summary Format Template
```python
SUMMARY_TEMPLATE = """
Subject: Gmail Summary - {date_range}

📧 Email Summary for {date_range}

🚨 URGENT ({urgent_count} emails)
{urgent_items}

💼 OPPORTUNITIES ({opportunities_count} emails)  
{opportunities_items}

💰 BILLS ({bills_count} emails)
{bills_items}

🗑️ JUNK ({junk_count} emails)
{junk_summary}

📊 Statistics
- Total emails processed: {total_count}
- Categorization accuracy: {accuracy}%
- Time saved: ~{time_saved} minutes
"""
```

#### Summary Generation Rules
- Generate summaries on configurable schedule (daily/weekly)
- Include top 5 items per category maximum
- Highlight actionable items in URGENT and BILLS
- Provide aggregate statistics for JUNK
- Send via Gmail MCP `send_message` tool

### 5. Error Handling Requirements

#### Required Error Handling
```python
# REQUIRED: Implement these error handling patterns
try:
    # Gmail API operations
    result = gmail_tool.list_messages()
except RateLimitError:
    # Implement exponential backoff
    time.sleep(exponential_backoff_delay)
    retry_operation()
except AuthenticationError:
    # Refresh OAuth tokens
    refresh_gmail_credentials()
except Exception as e:
    # Log error and continue processing
    logger.error(f"Email processing error: {e}")
    continue
```

#### Retry Logic
- Implement exponential backoff for rate limits
- Maximum 3 retry attempts per operation
- Log all failures for monitoring
- Graceful degradation when MCP server unavailable

### 6. Configuration Management

#### Required Environment Variables
```bash
# REQUIRED: These environment variables must be supported
OPENAI_API_KEY=your_openai_api_key
PROCESSING_INTERVAL=3600  # seconds
SUMMARY_FREQUENCY=daily   # daily, weekly
USER_EMAIL=user@example.com
MCP_CONFIG_DIR=~/.gmail-mcp
```

#### Configuration Validation
- Validate all required environment variables on startup
- Provide clear error messages for missing configuration
- Support both local and remote MCP server setup
- Allow runtime configuration updates

### 7. Performance Requirements

#### Processing Constraints
- Process maximum 100 emails per batch
- Complete categorization within 2 minutes per batch
- Use batch operations where possible to minimize API calls
- Implement pagination for large email volumes

#### Memory Management
- Clear processed email data after categorization
- Implement garbage collection for long-running processes
- Monitor memory usage and implement limits
- Use streaming for large email processing

### 8. Security Requirements

#### Authentication Rules
- Use OAuth2 for Gmail authentication only
- Store credentials securely using MCP server standards
- Never log email content or sensitive data
- Implement token refresh handling

#### Data Privacy
- No permanent storage of email content
- Process emails in memory only
- Respect user privacy settings
- Comply with Gmail API terms of service

### 9. Testing Requirements

#### Required Test Coverage
```python
# REQUIRED: Implement these test categories
def test_email_categorization():
    """Test categorization accuracy for each category"""
    pass

def test_gmail_label_application():
    """Test Gmail label creation and application"""
    pass

def test_summary_generation():
    """Test email summary format and content"""
    pass

def test_error_handling():
    """Test error scenarios and recovery"""
    pass

def test_rate_limiting():
    """Test API rate limit handling"""
    pass
```

#### Test Data Requirements
- Create sample emails for each category
- Test edge cases (empty emails, malformed content)
- Validate summary generation with various data volumes
- Test authentication failure scenarios

### 10. Deployment Requirements

#### Prerequisites Validation
```bash
# REQUIRED: Validate these before deployment
- Node.js 18+ installed
- @shinzolabs/gmail-mcp package available
- Google Cloud project with Gmail API enabled
- OAuth2 credentials configured
- Python dependencies installed
```

#### Monitoring Requirements
- Log categorization accuracy metrics
- Monitor API usage and rate limits
- Track processing times and performance
- Alert on authentication failures
- Monitor summary delivery success rates

### 11. Code Organization Rules

#### Required File Structure
```
gmail_categorizer_agent/
├── __init__.py
├── agent.py              # Main agent implementation
├── categorizer.py        # Email categorization logic
├── summarizer.py         # Summary generation
├── gmail_client.py       # Gmail MCP integration
├── config.py            # Configuration management
├── utils.py             # Utility functions
└── tests/
    ├── test_categorizer.py
    ├── test_summarizer.py
    └── test_integration.py
```

#### Import Rules
```python
# REQUIRED: Use these import patterns
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
import logging
import schedule
import time
from typing import Dict, List, Optional
```

### 12. Documentation Requirements

#### Required Documentation
- Setup instructions for Google Cloud Console
- OAuth2 authentication flow documentation
- Configuration options and environment variables
- Troubleshooting guide for common issues
- API usage examples and best practices

#### Code Documentation
- Docstrings for all functions and classes
- Type hints for all function parameters and returns
- Inline comments for complex categorization logic
- README with quick start guide

## Compliance Checklist

Before considering the agent complete, verify:

- [ ] ChatGPT model configured with temperature 0.3
- [ ] Gmail MCP server integration implemented
- [ ] All four email categories supported
- [ ] Gmail labels created and applied correctly
- [ ] Email summaries generated and delivered
- [ ] Error handling and retry logic implemented
- [ ] Configuration management working
- [ ] Performance requirements met
- [ ] Security requirements satisfied
- [ ] Test coverage adequate
- [ ] Documentation complete

## Prohibited Practices

### DO NOT:
- Store email content permanently
- Use models other than ChatGPT without approval
- Modify the four required categories
- Skip error handling implementation
- Hardcode credentials or API keys
- Process emails without user consent
- Ignore Gmail API rate limits
- Create labels outside the "Agent/" namespace

### ALWAYS:
- Use the specified system prompt template
- Implement proper OAuth2 authentication
- Log categorization decisions
- Validate configuration on startup
- Handle API failures gracefully
- Respect user privacy
- Follow Gmail API terms of service
- Use the exact label naming convention

---

**Rule Version**: 1.0  
**Last Updated**: 2025-07-24  
**Applies To**: Gmail Categorization Agent Development  
**Framework**: Strands Agents SDK
