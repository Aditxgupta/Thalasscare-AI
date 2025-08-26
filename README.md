# ThalassCare AI - GitHub Gist Analyzer

A comprehensive AI-powered platform for analyzing GitHub gists and generating detailed code reports using OpenAI's GPT-4.

## Features

- **GitHub Gist Analysis**: Input any GitHub gist URL and get AI-powered analysis
- **Comprehensive Reports**: Get detailed summaries, code analysis, and technical insights
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **Real-time Processing**: Live analysis with progress indicators
- **Export Functionality**: Download analysis reports as JSON files
- **Dashboard Integration**: Seamlessly integrated with ThalassCare AI dashboard

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

The application uses the following environment variables (already configured with default values):

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
- `AZURE_OPENAI_API_VERSION`: API version (default: 2024-08-01-preview)
- `AZURE_OPENAI_DEPLOYMENT`: Model deployment name (default: gpt-4-1106-preview)

### 3. Run the Application

```bash
streamlit streamlits.py
```

The application will start on `http://localhost:5000`

## Usage

### Main Dashboard
- Navigate to `http://localhost:5000/dashboard` to access the main ThalassCare AI dashboard
- View real-time analytics and blood donation management data

### GitHub Gist Analyzer
- Navigate to `http://localhost:5000/gist-analyzer` or click "Generate Report" on the dashboard
- Enter a GitHub gist URL (e.g., `https://gist.github.com/username/gist-id`)
- Choose analysis options:
  - **Include code in analysis**: Shows original code alongside analysis
  - **Detailed analysis**: Provides more comprehensive technical insights
- Click "Analyze Gist" to generate the report
- View results in three sections:
  - **AI Summary**: High-level overview of the code
  - **Code Analysis**: Detailed technical analysis
  - **Technical Insights**: Recommendations and best practices
- Download the complete report as a JSON file

## API Endpoints

- `GET /dashboard` - Main dashboard page
- `GET /gist-analyzer` - Gist analyzer page
- `POST /analyze-gist` - Analyze a GitHub gist
- `POST /chat` - General chat endpoint

## Example Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the dashboard**:
   - Open `http://localhost:5000/dashboard` in your browser

3. **Generate a report**:
   - Click "Generate Report" button
   - Enter a GitHub gist URL
   - Configure analysis options
   - Click "Analyze Gist"

4. **View results**:
   - Review the AI-generated summary
   - Examine code analysis and technical insights
   - Download the complete report

## Technical Details

### Backend Architecture
- **Flask**: Web framework for API endpoints
- **Azure OpenAI**: GPT-4 integration for code analysis
- **GitHub API**: Fetches gist content
- **Requests**: HTTP client for API calls

### Frontend Features
- **Tailwind CSS**: Modern, responsive styling
- **JavaScript**: Dynamic UI interactions
- **Chart.js**: Data visualization
- **PapaParse**: CSV data processing

### AI Analysis Capabilities
- Code language detection
- Architecture analysis
- Best practices assessment
- Performance recommendations
- Security considerations
- Maintainability insights

## File Structure

```
thalasscare_chatbot/
├── app.py                 # Main Flask application
├── dashobard .html        # Main dashboard page
├── gist_analyzer.html     # GitHub gist analyzer page
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your Azure OpenAI API key is valid and has sufficient credits
2. **Gist Not Found**: Verify the GitHub gist URL is correct and publicly accessible
3. **Analysis Timeout**: Large gists may take longer to analyze; wait for completion
4. **Network Issues**: Check your internet connection for GitHub API access

### Error Messages

- **"Invalid GitHub gist URL"**: Ensure the URL follows the pattern `https://gist.github.com/username/gist-id`
- **"Failed to fetch gist"**: The gist may be private or the URL is incorrect
- **"OpenAI analysis failed"**: Check your API credentials and quota

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the ThalassCare AI platform and is designed for blood donation management and analysis.

## Support

For support or questions, please refer to the project documentation or contact the development team.

