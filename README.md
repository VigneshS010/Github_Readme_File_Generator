
# streamlit_github_readme_generator

A Streamlit application that generates a README file for a given GitHub repository URL using the OpenRouter API.

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/username/streamlit_github_readme_generator.git
cd streamlit_github_readme_generator
```

2. Set up a virtual environment (optional but recommended):
```bash
# Using Python's built-in venv module
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` yet, you need to manually install the required packages:
```bash
pip install streamlit requests
```

4. Set up your OpenRouter API key. For this, you need to create a `.streamlit/secrets.toml` file in the project root directory with the following content:
```toml
[secrets]
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
```

5. Run the Streamlit app:
```bash
streamlit run streamlit_github_readme_generator.py
```

## Usage

1. Once the Streamlit application is running, open your web browser to the specified local URL (usually `http://localhost:8501`).
2. In the given text input field, enter the GitHub repository URL for which you want to generate a README file (e.g., `https://github.com/username/repo-name`).
3. Click on the "Generate Readme file" button.
4. The application will display a simple summary of the project and the generated README content.
5. You can directly download the generated README as a `README.md` file by clicking on the "Download README.md" link.

### Example
1. Launch the Streamlit application.
2. Input the GitHub repository URL such as `https://github.com/openai/CLIP` in the text input field.
3. Click on the "Generate Readme file" button.
4. Once processing is complete, a "Simple explanation about the Project" section will show a one-line summary.
5. The "Readme.md content" section will display the full generated README text.
6. Click the "Download README.md" link to download the generated README file.

## Contributing

Contributions are welcome! If you have any suggestions or would like to make improvements, feel free to fork the repository, make your changes, and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Notes

- The application uses the OpenRouter API key stored securely in Streamlit secrets. Make sure you have an OpenRouter account and obtain an API key from [OpenRouter](https://openrouter.ai/).
- Currently, the script uses the `deepseek/deepseek-r1-zero:free` model for generating the README content.

## Acknowledgments

- Thanks to [Streamlit](https://streamlit.io/) for providing a great platform for building data applications with ease.
- Thanks to [OpenRouter](https://openrouter.ai/) for offering a model to generate comprehensive content.

If you encounter any issues or need assistance, please open an issue on the GitHub repository.
