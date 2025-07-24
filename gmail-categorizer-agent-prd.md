# Gmail Email Categorization Agent - Product Requirements Document

## 1. Executive Summary

### 1.1 Product Overview
The Gmail Email Categorization Agent is an intelligent email management system built using the Strands Agents framework. The agent automatically categorizes incoming emails into predefined labels (urgent, opportunities, junk, bills) and provides users with periodic email summaries delivered directly to their inbox. The system leverages the [shinzo-labs/gmail-mcp](https://github.com/shinzo-labs/gmail-mcp) Model Context Protocol server for secure Gmail integration.

### 1.2 Business Objectives
- **Improve Email Productivity**: Reduce time spent manually sorting and prioritizing emails
- **Enhance Email Organization**: Automatically categorize emails with consistent, intelligent labeling
- **Provide Actionable Insights**: Deliver concise summaries of email activity to help users stay informed
- **Reduce Email Overwhelm**: Help users focus on important communications by filtering noise

### 1.3 Success Metrics
- **Categorization Accuracy**: >90% correct email categorization
- **User Engagement**: Users actively use categorized labels for email management
- **Time Savings**: 30% reduction in time spent on email organization
- **Summary Utility**: Users find email summaries actionable and valuable

## 2. Product Requirements

### 2.1 Core Functionality

#### 2.1.1 Email Categorization
- **Automatic Processing**: Monitor Gmail inbox for new emails
- **Intelligent Classification**: Use ChatGPT to analyze email content and categorize into:
  - **Urgent**: Time-sensitive emails requiring immediate attention
  - **Opportunities**: Business opportunities, job offers, networking requests
  - **Junk**: Spam, promotional emails, newsletters with low value
  - **Bills**: Invoices, payment reminders, financial statements
- **Label Application**: Automatically apply Gmail labels to categorized emails
- **Batch Processing**: Handle multiple emails efficiently in single processing cycles

#### 2.1.2 Email Summarization
- **Periodic Summaries**: Generate email summaries on configurable schedules (daily, weekly)
- **Category-based Grouping**: Organize summary by email categories
- **Key Insights**: Highlight important emails, trends, and actionable items
- **Summary Delivery**: Send summary as formatted email to user's inbox

#### 2.1.3 Gmail Integration
- **MCP Integration**: Utilize [shinzo-labs/gmail-mcp](https://github.com/shinzo-labs/gmail-mcp) for Gmail API interactions
- **Available Tools**: The MCP server provides comprehensive Gmail API coverage including:
  - `list_messages`: Retrieve emails with filtering options
  - `get_message`: Get specific email content and metadata
  - `modify_message`: Apply/remove labels from emails
  - `send_message`: Send email summaries to users
  - `list_labels`: Manage Gmail labels
  - `create_label`: Create new categorization labels
  - `list_threads`: Handle email conversations
- **Authentication**: Secure OAuth2 authentication with Google Cloud credentials
- **Permission Management**: Request minimal required Gmail API scopes
- **Rate Limiting**: Built-in respect for Gmail API rate limits and quotas

### 2.2 Technical Architecture

#### 2.2.1 Model Configuration
```python
# ChatGPT model configuration
from strands.models.litellm import LiteLLMModel

chatgpt_model = LiteLLMModel(
    client_args={
        "api_key": "<OPENAI_API_KEY>",
    },
    model_id="gpt-4o",
    params={
        "temperature": 0.3,  # Lower temperature for consistent categorization
        "max_tokens": 2000
    }
)
```

#### 2.2.2 Agent Structure
```python
from strands import Agent, tool
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

# Gmail MCP client setup
gmail_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="npx", args=["@shinzolabs/gmail-mcp"])
))

# Agent initialization
agent = Agent(
    model=chatgpt_model,
    tools=[gmail_tools],  # From MCP client
    system_prompt=EMAIL_CATEGORIZATION_PROMPT
)
```

#### 2.2.3 System Prompt Design
```
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
```

### 2.3 Feature Specifications

#### 2.3.1 Email Processing Workflow
1. **Email Retrieval**: Fetch unprocessed emails from Gmail inbox
2. **Content Analysis**: Extract and analyze email metadata and content
3. **Categorization**: Use ChatGPT to classify email into appropriate category
4. **Label Application**: Apply corresponding Gmail label to email
5. **Logging**: Record categorization decisions for audit and improvement
6. **Error Handling**: Manage API failures and retry logic

#### 2.3.2 Summary Generation
1. **Data Collection**: Gather categorized emails from specified time period
2. **Content Aggregation**: Group emails by category and extract key information
3. **Summary Creation**: Generate structured summary with:
   - Total email count by category
   - Highlighted urgent items
   - Notable opportunities
   - Bill payment reminders
   - Junk email statistics
4. **Email Composition**: Format summary as HTML email
5. **Delivery**: Send summary to user's primary email address

#### 2.3.3 Configuration Management
- **Processing Schedule**: Configurable intervals for email processing
- **Summary Frequency**: User-defined summary delivery schedule
- **Category Customization**: Ability to modify or add email categories
- **Filter Rules**: Custom rules for specific senders or subjects
- **Notification Preferences**: Control over summary content and format

### 2.4 User Experience Requirements

#### 2.4.1 Setup Process
1. **Authentication**: Simple OAuth2 flow for Gmail access
2. **Permission Grant**: Clear explanation of required permissions
3. **Configuration**: Easy setup of processing and summary preferences
4. **Testing**: Verification that categorization is working correctly

#### 2.4.2 Email Summary Format
```
Subject: Gmail Summary - [Date Range]

📧 Email Summary for [Date Range]

🚨 URGENT (X emails)
- [Email subject] from [Sender] - [Brief description]
- [Action required items]

💼 OPPORTUNITIES (X emails)  
- [Email subject] from [Sender] - [Brief description]
- [Notable opportunities]

💰 BILLS (X emails)
- [Email subject] from [Sender] - Due: [Date]
- [Payment reminders]

🗑️ JUNK (X emails)
- [Summary of filtered content]

📊 Statistics
- Total emails processed: X
- Categorization accuracy: X%
- Time saved: ~X minutes
```

#### 2.4.3 Gmail Label Structure
- `Agent/Urgent` - Red color, high priority
- `Agent/Opportunities` - Green color, medium priority  
- `Agent/Bills` - Yellow color, medium priority
- `Agent/Junk` - Gray color, low priority

## 3. Technical Requirements

### 3.1 Dependencies
```python
# requirements.txt
strands-agents>=0.1.0
strands-agents-tools>=0.1.0
openai>=1.0.0
python-dotenv>=1.0.0
schedule>=1.2.0
```

```bash
# Node.js dependencies for Gmail MCP server
npm install -g @shinzolabs/gmail-mcp
```

### 3.2 Environment Configuration
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key
PROCESSING_INTERVAL=3600  # seconds
SUMMARY_FREQUENCY=daily   # daily, weekly
USER_EMAIL=user@example.com

# Gmail MCP Configuration (optional - defaults to ~/.gmail-mcp/)
MCP_CONFIG_DIR=~/.gmail-mcp
GMAIL_CREDENTIALS_PATH=~/.gmail-mcp/credentials.json
GMAIL_OAUTH_PATH=~/.gmail-mcp/gcp-oauth.keys.json

# For remote server setup (Smithery)
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
REFRESH_TOKEN=your_oauth_refresh_token
```

### 3.3 MCP Server Setup

#### Google Cloud Setup (One-time)
```bash
# 1. Create Google Cloud project and enable Gmail API
# 2. Create OAuth 2.0 Client ID (Desktop app type)
# 3. Download OAuth keys to ~/.gmail-mcp/gcp-oauth.keys.json
```

#### User Authentication (Per User)
```bash
# Install and authenticate with Gmail MCP server
npm install -g @shinzolabs/gmail-mcp

# Run authentication flow
npx @shinzolabs/gmail-mcp auth
# This opens browser for OAuth consent and saves credentials
```

#### MCP Client Configuration
```javascript
// Add to MCP client config.json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["@shinzolabs/gmail-mcp"]
    }
  }
}
```

For detailed setup instructions, see: https://github.com/shinzo-labs/gmail-mcp

### 3.4 Performance Requirements
- **Processing Speed**: Categorize 100 emails within 2 minutes
- **API Efficiency**: Minimize Gmail API calls through batching
- **Memory Usage**: Handle large email volumes without memory issues
- **Reliability**: 99.5% uptime for email processing

### 3.5 Security Requirements
- **OAuth2 Security**: Secure token storage and refresh handling
- **API Key Protection**: Environment-based configuration for sensitive data
- **Data Privacy**: No permanent storage of email content
- **Access Control**: Minimal required Gmail permissions

## 4. Implementation Plan

### 4.1 Phase 1: Core Development (Weeks 1-2)
- [ ] Set up Strands Agent with ChatGPT model
- [ ] Integrate shinzo/gmail-mcp for Gmail access
- [ ] Implement basic email categorization logic
- [ ] Create Gmail label management system
- [ ] Develop email processing workflow

### 4.2 Phase 2: Summarization (Weeks 3-4)
- [ ] Build email summary generation system
- [ ] Create HTML email template for summaries
- [ ] Implement summary delivery mechanism
- [ ] Add configuration management
- [ ] Develop scheduling system

### 4.3 Phase 3: Enhancement (Weeks 5-6)
- [ ] Add error handling and retry logic
- [ ] Implement logging and monitoring
- [ ] Create user configuration interface
- [ ] Add categorization accuracy tracking
- [ ] Optimize performance and API usage

### 4.4 Phase 4: Testing & Deployment (Weeks 7-8)
- [ ] Comprehensive testing with various email types
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Documentation and user guides
- [ ] Production deployment setup

## 5. Risk Assessment

### 5.1 Technical Risks
- **Gmail API Limitations**: Rate limiting may affect processing speed
- **MCP Server Reliability**: Dependency on third-party MCP server
- **Model Accuracy**: ChatGPT categorization may have edge cases
- **Authentication Issues**: OAuth token expiration handling

### 5.2 Mitigation Strategies
- **API Management**: Implement robust rate limiting and retry logic
- **Fallback Systems**: Alternative categorization methods if MCP fails
- **Model Training**: Fine-tune prompts based on categorization feedback
- **Auth Resilience**: Automatic token refresh and error recovery

## 6. Success Criteria

### 6.1 Functional Success
- [ ] Agent successfully categorizes emails with >90% accuracy
- [ ] Gmail labels are applied correctly and consistently
- [ ] Email summaries are generated and delivered on schedule
- [ ] System handles various email types and volumes

### 6.2 User Success
- [ ] Users report improved email organization
- [ ] Time savings measurably achieved
- [ ] Summary emails provide actionable insights
- [ ] System operates reliably without user intervention

### 6.3 Technical Success
- [ ] System meets performance requirements
- [ ] Error rates remain below 1%
- [ ] API usage stays within quotas
- [ ] Security standards are maintained

## 7. Future Enhancements

### 7.1 Advanced Features
- **Custom Categories**: User-defined email categories
- **Smart Filters**: Learning-based filter improvements
- **Integration Expansion**: Support for other email providers
- **Mobile Notifications**: Push notifications for urgent emails

### 7.2 Analytics & Insights
- **Email Patterns**: Analysis of email trends and patterns
- **Productivity Metrics**: Detailed time savings calculations
- **Sender Analysis**: Insights into frequent senders and types
- **Category Optimization**: ML-based category refinement

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-24  
**Author**: Product Team  
**Status**: Draft
