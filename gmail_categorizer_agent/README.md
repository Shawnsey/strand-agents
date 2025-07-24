# Gmail Email Categorization Agent

An intelligent Gmail email management system built using the Strands Agents framework that automatically categorizes incoming emails and provides users with actionable summaries.

## 🎯 Overview

This agent uses ChatGPT to analyze and categorize emails into four predefined categories:
- **🚨 URGENT**: Time-sensitive emails requiring immediate action
- **💼 OPPORTUNITIES**: Business opportunities, job offers, networking
- **🗑️ JUNK**: Spam, low-value promotional content, newsletters  
- **💰 BILLS**: Invoices, payment reminders, financial statements

## 🏗️ Architecture

- **Framework**: Strands Agents SDK
- **AI Model**: ChatGPT (GPT-4o) via LiteLLM
- **Gmail Integration**: @shinzolabs/gmail-mcp MCP server
- **Authentication**: OAuth2 via Google Cloud Platform

## 📁 Project Structure

```
gmail_categorizer_agent/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
│
├── src/                        # Main application code
│   ├── agent.py                # Main agent implementation
│   ├── categorizer.py          # Email categorization logic
│   ├── summarizer.py           # Summary generation
│   ├── gmail_client.py         # Gmail MCP integration
│   ├── config.py              # Configuration management
│   └── utils.py               # Utility functions
│
├── tests/                      # Test suite
│   ├── test_categorizer.py    # Categorization tests
│   ├── test_summarizer.py     # Summary generation tests
│   ├── test_gmail_client.py   # Gmail integration tests
│   ├── test_integration.py    # End-to-end tests
│   └── fixtures/              # Test data
│
├── config/                     # Configuration files
│   ├── prompts.py             # System prompts
│   ├── labels.py              # Gmail label definitions
│   └── templates.py           # Email templates
│
├── scripts/                    # Setup and deployment scripts
│   ├── setup.py               # Initial setup script
│   ├── auth.py                # OAuth authentication
│   └── deploy.py              # Deployment script
│
└── docs/                       # Documentation
    ├── setup.md               # Setup instructions
    ├── configuration.md       # Configuration guide
    ├── troubleshooting.md     # Common issues
    └── api.md                 # API documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Google Cloud Platform account
- Gmail API access

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd gmail_categorizer_agent

# Install Python dependencies
pip install -r requirements.txt

# Install Gmail MCP server
npm install -g @shinzolabs/gmail-mcp

# Run setup script
python scripts/setup.py
```

### Configuration
1. Set up Google Cloud project and enable Gmail API
2. Create OAuth 2.0 credentials
3. Run authentication: `npx @shinzolabs/gmail-mcp auth`
4. Configure environment variables in `.env`

## 📊 Features

- **Intelligent Categorization**: AI-powered email classification
- **Gmail Label Management**: Automatic label creation and application
- **Periodic Summaries**: Daily/weekly email summaries delivered to inbox
- **Secure Authentication**: OAuth2 integration with Google
- **Error Handling**: Robust retry logic and rate limiting
- **Privacy Focused**: No permanent email content storage

## 🔧 Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_categorizer.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

## 📝 Documentation

- [Setup Guide](docs/setup.md) - Detailed setup instructions
- [Configuration](docs/configuration.md) - Configuration options
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions
- [API Reference](docs/api.md) - API documentation

## 🔒 Security & Privacy

- Uses OAuth2 for secure Gmail authentication
- No permanent storage of email content
- Processes emails in memory only
- Minimal required Gmail API permissions
- Secure credential management via MCP standards

## 📈 Performance

- Processes up to 100 emails per batch
- Categorization completed within 2 minutes per batch
- Efficient API usage with batch operations
- Memory-optimized for long-running processes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [troubleshooting guide](docs/troubleshooting.md)
- Review existing GitHub issues
- Create a new issue with detailed information

---

**Status**: In Development  
**Version**: 0.1.0  
**Last Updated**: 2025-07-24
