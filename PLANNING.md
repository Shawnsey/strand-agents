# Gmail Email Categorization Agent - Planning Document

## 🎯 Vision

### Product Vision
Create an intelligent Gmail email management system that automatically categorizes incoming emails and provides users with actionable summaries, reducing email overwhelm and improving productivity through AI-powered organization.

### Mission Statement
Empower users to focus on what matters most by intelligently filtering, categorizing, and summarizing their email communications using advanced AI capabilities integrated seamlessly with Gmail.

### Success Metrics
- **Productivity**: 30% reduction in time spent on email organization
- **Accuracy**: >90% correct email categorization
- **User Satisfaction**: Users actively utilize categorized labels for email management
- **Engagement**: Regular use of email summaries for decision-making

## 🏗️ Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gmail API     │◄───┤  Gmail MCP       │◄───┤  Strands Agent  │
│                 │    │  Server          │    │                 │
│ - Messages      │    │ @shinzolabs/     │    │ - ChatGPT Model │
│ - Labels        │    │ gmail-mcp        │    │ - Categorizer   │
│ - Threads       │    │                  │    │ - Summarizer    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲                        │
                                │                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User's Gmail  │◄───┤   OAuth2 Auth    │    │   Scheduler     │
│   Inbox         │    │   Flow           │    │                 │
│                 │    │                  │    │ - Processing    │
│ - Categorized   │    │ - Google Cloud   │    │ - Summaries     │
│   Labels        │    │ - Credentials    │    │ - Monitoring    │
│ - Summaries     │    │ - Token Refresh  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Component Architecture

#### 1. Core Agent Layer
- **Strands Agent**: Main orchestration and decision-making
- **ChatGPT Model**: Email content analysis and categorization
- **System Prompt**: Categorization logic and guidelines

#### 2. Integration Layer
- **Gmail MCP Client**: Interface to Gmail API via MCP protocol
- **OAuth2 Handler**: Authentication and token management
- **Rate Limiter**: API quota and throttling management

#### 3. Processing Layer
- **Email Categorizer**: Core categorization logic
- **Label Manager**: Gmail label creation and application
- **Summary Generator**: Periodic email summary creation

#### 4. Data Flow
```
Incoming Email → MCP Client → Agent Analysis → ChatGPT Categorization → 
Label Application → Summary Aggregation → Scheduled Delivery
```

## 💻 Technology Stack

### Core Framework
- **Strands Agents SDK** (`strands-agents>=0.1.0`)
  - Agent orchestration and tool management
  - Model integration and prompt handling
  - Streaming and callback support

### AI/ML Components
- **OpenAI GPT-4o** (via LiteLLM)
  - Email content analysis
  - Intelligent categorization
  - Summary generation
- **LiteLLM** (`strands-agents[litellm]`)
  - Unified LLM interface
  - Model configuration management

### Gmail Integration
- **Gmail MCP Server** (`@shinzolabs/gmail-mcp`)
  - Gmail API access via Model Context Protocol
  - Message, label, and thread management
  - OAuth2 authentication handling

### Supporting Libraries
- **Python Standard Library**
  - `logging`: Application logging and monitoring
  - `json`: Configuration and data handling
  - `datetime`: Timestamp and scheduling
  - `os`: Environment variable management

- **Third-party Dependencies**
  - `python-dotenv>=1.0.0`: Environment configuration
  - `schedule>=1.2.0`: Task scheduling
  - `typing`: Type hints and annotations

### Infrastructure
- **Node.js 18+**: Required for Gmail MCP server
- **Google Cloud Platform**: Gmail API and OAuth2 setup
- **Local File System**: Configuration and credential storage

## 🛠️ Required Tools List

### Development Tools

#### 1. Gmail MCP Tools (from @shinzolabs/gmail-mcp)
```python
# Message Management
- list_messages: Retrieve emails with filtering
- get_message: Get specific email content
- modify_message: Apply/remove labels
- send_message: Send summary emails
- delete_message: Permanent email deletion
- trash_message: Move to trash
- untrash_message: Restore from trash

# Label Management  
- list_labels: Get all Gmail labels
- get_label: Get specific label details
- create_label: Create new categorization labels
- update_label: Modify existing labels
- delete_label: Remove labels

# Thread Management
- list_threads: Get email conversations
- get_thread: Get specific thread
- modify_thread: Apply labels to threads
```

#### 2. Strands Agent Tools
```python
# Core Agent Tools
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands.tools.mcp import MCPClient

# Custom Tools (to be implemented)
@tool
def categorize_email(subject: str, sender: str, body: str) -> str:
    """Categorize email into urgent/opportunities/junk/bills"""
    
@tool  
def apply_gmail_label(message_id: str, label: str) -> bool:
    """Apply categorization label to Gmail message"""
    
@tool
def generate_summary(emails: List[Dict], date_range: str) -> str:
    """Generate formatted email summary"""
```

#### 3. Configuration Tools
```python
# Environment Management
- load_dotenv(): Load environment variables
- validate_config(): Verify required settings
- setup_oauth(): Initialize Gmail authentication
- create_labels(): Set up categorization labels
```

### External Dependencies

#### 1. Google Cloud Setup
```bash
# Required Google Cloud Components
- Gmail API enabled
- OAuth2 Client ID (Desktop application)
- Client credentials file
- User consent and refresh tokens
```

#### 2. Node.js Environment
```bash
# Gmail MCP Server Requirements
npm install -g @shinzolabs/gmail-mcp
npx @shinzolabs/gmail-mcp auth  # User authentication
```

#### 3. Python Environment
```bash
# Core Dependencies
pip install strands-agents>=0.1.0
pip install strands-agents-tools>=0.1.0
pip install strands-agents[litellm]
pip install python-dotenv>=1.0.0
pip install schedule>=1.2.0
```

## 📁 Project Structure

```
gmail_categorizer_agent/
├── README.md                    # Project documentation
├── PLANNING.md                  # This planning document
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── agent.py                # Main agent implementation
│   ├── categorizer.py          # Email categorization logic
│   ├── summarizer.py           # Summary generation
│   ├── gmail_client.py         # Gmail MCP integration
│   ├── config.py              # Configuration management
│   ├── scheduler.py           # Task scheduling
│   └── utils.py               # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_categorizer.py    # Categorization tests
│   ├── test_summarizer.py     # Summary generation tests
│   ├── test_gmail_client.py   # Gmail integration tests
│   ├── test_integration.py    # End-to-end tests
│   └── fixtures/              # Test data
│       ├── sample_emails.json
│       └── expected_outputs.json
│
├── config/
│   ├── prompts.py             # System prompts
│   ├── labels.py              # Gmail label definitions
│   └── templates.py           # Email templates
│
├── scripts/
│   ├── setup.py               # Initial setup script
│   ├── auth.py                # OAuth authentication
│   └── deploy.py              # Deployment script
│
└── docs/
    ├── setup.md               # Setup instructions
    ├── configuration.md       # Configuration guide
    ├── troubleshooting.md     # Common issues
    └── api.md                 # API documentation
```

## 🔧 Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Deliverables:**
- [ ] Project structure setup
- [ ] Strands Agent with ChatGPT integration
- [ ] Gmail MCP client connection
- [ ] Basic email retrieval and analysis
- [ ] Core categorization logic

**Key Tools:**
- Strands Agent framework
- LiteLLM for ChatGPT
- Gmail MCP server setup
- OAuth2 authentication

### Phase 2: Categorization (Week 3-4)
**Deliverables:**
- [ ] Email categorization engine
- [ ] Gmail label management
- [ ] Label application system
- [ ] Categorization accuracy tracking
- [ ] Error handling and retry logic

**Key Tools:**
- ChatGPT categorization prompts
- Gmail label management tools
- Logging and monitoring systems

### Phase 3: Summarization (Week 5-6)
**Deliverables:**
- [ ] Summary generation system
- [ ] Email template formatting
- [ ] Scheduled summary delivery
- [ ] Configuration management
- [ ] Performance optimization

**Key Tools:**
- Summary generation algorithms
- Email formatting templates
- Task scheduling system

### Phase 4: Production (Week 7-8)
**Deliverables:**
- [ ] Comprehensive testing suite
- [ ] Documentation and guides
- [ ] Deployment automation
- [ ] Monitoring and alerting
- [ ] User acceptance testing

**Key Tools:**
- Testing frameworks
- Documentation generators
- Deployment scripts
- Monitoring dashboards

## 🔒 Security & Privacy Considerations

### Data Protection
- **No Persistent Storage**: Email content processed in memory only
- **Minimal Permissions**: Request only required Gmail API scopes
- **Secure Credentials**: OAuth2 tokens stored securely via MCP standards
- **Audit Logging**: Track all categorization decisions without content

### Authentication Security
- **OAuth2 Flow**: Standard Google authentication
- **Token Refresh**: Automatic credential renewal
- **Scope Limitation**: Minimal required Gmail permissions
- **Credential Isolation**: Separate user credentials per installation

## 📊 Monitoring & Analytics

### Performance Metrics
- **Processing Speed**: Emails categorized per minute
- **API Usage**: Gmail API call efficiency
- **Memory Usage**: Resource consumption tracking
- **Error Rates**: Failure and retry statistics

### Business Metrics
- **Categorization Accuracy**: Percentage of correct classifications
- **User Engagement**: Label usage and summary interaction
- **Time Savings**: Estimated productivity improvements
- **Summary Effectiveness**: User feedback and actions taken

## 🚀 Deployment Strategy

### Local Development
```bash
# Setup development environment
git clone <repository>
cd gmail_categorizer_agent
pip install -r requirements.txt
npm install -g @shinzolabs/gmail-mcp
python scripts/setup.py
```

### Production Deployment
```bash
# Production setup
python scripts/deploy.py --environment production
systemctl enable gmail-categorizer
systemctl start gmail-categorizer
```

### Configuration Management
- Environment-specific configuration files
- Secure credential management
- Automated deployment scripts
- Health check endpoints

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-24  
**Status**: Planning Phase  
**Next Review**: Implementation Phase 1 Completion
