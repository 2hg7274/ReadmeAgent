# ReadmeAgent

## Overview

ReadmeAgent is a project designed to automate the generation of professional README.md files for software projects. It leverages multiple agents, each with a distinct responsibility to ensure the README is comprehensive, clear, and structured properly.

### Key Features

- **File Viewer Agent:** Analyzes the project directory, reading and interpreting files to write structured notes.
- **Write Agent:** Generates a detailed and well-structured README.md file using the notes provided by the File Viewer Agent.
- **Review Agent:** Reviews the generated README for completeness, clarity, and technical accuracy before finalizing.
- **Search Agent:** Supports the README generation by performing external web searches to fill in gaps or clarify complex concepts.

## Getting Started

To set up ReadmeAgent and generate a README for a new project, follow these steps:

1. Clone or download the ReadmeAgent repository to your local machine.
2. Install the necessary dependencies listed in `requirements.txt`.
3. Run the `main.py` script, specifying the path to the project directory you wish to analyze.

Example command:

```bash
python main.py --path /path/to/project
```

Once the process completes, a `README.md` file will be generated in the specified project directory.

## Usage

Run the `main.py` script with the path to the target project directory.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True, type=str, help="README를 작성할 프로젝트 경로")
args = parser.parse_args()

# Call the main function to start the agent workflow
asyncio.run(main(args.path))
```

### Parameters

- `--path`: Path to the directory of the project for which the README needs to be generated.

## Folder Structure

```text
ReadmeAgent/
├── README.md          # Auto-generated README file
├── main.py            # Entry point of the project
├── configs.py         # Configuration settings
└── tools.py           # Definitions for various functions and classes
```

## Contributing

If you would like to contribute to the ReadmeAgent project, feel free to fork the repository and submit pull requests. We welcome any suggestions or improvements to make the README generation process even better!

## License

ReadmeAgent is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

## Behind the Scenes
This README was also written by Agent! 😁
