# Project Title: ReadmeAgent

## Overview / Description
The ReadmeAgent project is designed to automate the generation of README.md files for software projects. It utilizes multiple agents to extract information from project files, write structured documentation, review the content, and perform web searches for additional context.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd ReadmeAgent
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To generate a README.md file for your project, run the following command:
```bash
python main.py --path <project-path> --model <model-type>
```
Replace `<project-path>` with the path to your project and `<model-type>` with either `local` or `openai`.

## Features
- **File Extraction**: Automatically extracts content from project files.
- **Structured README Generation**: Creates a well-structured README.md file based on the extracted information.
- **Feedback Mechanism**: Allows for review and feedback on the generated README content.
- **Web Search Integration**: Performs external web searches to enhance the README with additional context.

## Folder Structure
```
/ReadmeAgent
├── agents
│   ├── file_viewer_agent.py
│   ├── write_agent.py
│   ├── review_agent.py
│   └── search_agent.py
├── tools
│   ├── file_viewer_tools.py
│   ├── write_readme_tool.py
│   ├── review_readme_tool.py
│   └── search_web_tool.py
├── model.py
├── cli.py
└── main.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License.