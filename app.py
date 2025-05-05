import streamlit as st
import os 
import json
import requests
import base64

# Function to get content from a GitHub repository
def get_python_files_content(repo_url, access_token=None):
    """
    Retrieves Python and notebook files from a GitHub repository and returns a list of their contents.
    """
    repo_name = repo_url.replace("https://github.com/", "").rstrip('/')
    api_url = f"https://api.github.com/repos/{repo_name}/contents"

    headers = {}
    if access_token:
        headers["Authorization"] = f"token {access_token}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch repo contents. Error: {e}")
        return "", ""

    contents = response.json()
    python_files_content = []
    queue = contents

    while queue:
        item = queue.pop(0)
        if item["type"] == "file" and (item["name"].endswith(".py") or item['name'].endswith('.ipynb')):
            file_response = requests.get(item["download_url"], headers=headers)
            file_response.raise_for_status()
            python_files_content.append(file_response.text.splitlines())
        elif item["type"] == "dir":
            dir_response = requests.get(item["url"], headers=headers)
            dir_response.raise_for_status()
            queue.extend(dir_response.json())

    all_code = "\n".join(["\n".join(file_content) for file_content in python_files_content])

    # Prompt to generate full README
    prompt1 = f""" Create a comprehensive README file content for the following Python code from a GitHub repository. 
    Include installation instructions, usage examples, contributing guidelines, and license information if possible.

    Code:
    {all_code}

    Do not include any author or publish year. Simply mention the license.

    if any api keys in the file dont mention that in the readme file, dont show the api key in publically for the viewers in the readme file, it is very important
    Do not include any surrounding boxes, curly braces, or any other symbols. Just the plain text.
    """
    readme = get_summarization(prompt1)

    # Prompt to generate 1-line summary
     prompt2 = f"""
    {readme}
    Strictly the output need to be single line text
    Provide a simple 1-line explanation about the project.
    1-line description as plain text, without any special formatting like LaTeX or markdown. 
    """
    simple_summary = get_summarization(prompt2)

    return readme, simple_summary

# Function to summarize using OpenRouter
def get_summarization(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "GitHub README Generator",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": prompt}],
            })
        )
        result = response.json()

        # Debug log
        if "choices" not in result:
            st.error("OpenRouter API error:")
            st.json(result)  # Show the full response
            return "ERROR: Could not generate summary"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        st.error(f"OpenRouter call failed: {e}")
        return "ERROR: Summarization failed"


# --- Streamlit UI ---
st.title("🛠️ GitHub README File Generator")

url = st.text_input("Enter GitHub Repo URL (e.g., https://github.com/username/repo):")

if st.button("Generate README"):
    if url:
        readme_text, summary = get_python_files_content(
            url, access_token=st.secrets["GITHUB_ACCESS_TOKEN"]
        )

        if readme_text:
            st.subheader("📌 1-Line Project Summary")
            st.code(summary.strip())

            st.subheader("📄 Generated README.md Content")
            st.code(readme_text.strip())

            # Download Link
            b64 = base64.b64encode(readme_text.encode()).decode()
            href = f'<a href="data:file/md;base64,{b64}" download="README.md">📥 Download README.md</a>'
            st.markdown(href, unsafe_allow_html=True)




# import streamlit as st
# import os 
# import json
# import requests
# import base64


# def get_python_files_content(repo_url, access_token=None):
#     """
#     Retrieves Python files from a GitHub repository and returns a list of their contents.
#     """
    
#     repo_name = repo_url.replace("https://github.com/", "")
#     api_url = f"https://api.github.com/repos/{repo_name}/contents"

#     headers = {}
#     if access_token:
#         headers["Authorization"] = f"token {access_token}"

#     response = requests.get(api_url, headers=headers)
#     response.raise_for_status()

#     contents = response.json()
#     python_files_content = []
#     queue = contents

#     while queue:
#         item = queue.pop(0)
#         if item["type"] == "file" and item["name"].endswith(".py") or item['name'].endswith('.ipynb'):
#             file_response = requests.get(item["download_url"], headers=headers)
#             file_response.raise_for_status()
#             python_files_content.append(file_response.text.splitlines()) #split by lines.
#         elif item["type"] == "dir":
#             dir_response = requests.get(item["url"], headers=headers)
#             dir_response.raise_for_status()
#             queue.extend(dir_response.json())

#         # return python_files_content

#     # except requests.exceptions.RequestException as e:
#     #     return f"Error: {e}"
#     # except (KeyError, ValueError) as e:
#     #     return f"Error parsing response: {e}"
    
#     def get_summarization(prompt):
        

#         response = requests.post(
#         url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization":  f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
#             "Content-Type": "application/json",
#             "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#             "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#         },


#         data=json.dumps({
#             "model": "deepseek/deepseek-r1-zero:free",
#             "messages": [
#             {
#                 "role": "user",
#                 "content": prompt 
#             }
#             ],
            
#         })
#         )

#         result = response.json()
#         text = result["choices"][0]["message"]["content"]
#         return text
    
#     all_code = "\n".join(["\n".join(file_content) for file_content in python_files_content])

#         # 3. Construct the prompt for OpenRouter.
#     prompt1 = f"""
#     Create a comprehensive README file content for the following Python code from a GitHub repository. 
#     Include installation instructions, usage examples, contributing guidelines, and license information if possible.

#     Code:
#     {all_code}

#     Do not include any author or publish year. Simply mention the license.

#     if any api keys in the file dont mention that in the readme file, dont show the api key in publically for the viewers in the readme file, it is very important
#     Do not include any surrounding boxes, curly braces, or any other symbols. Just the plain text.
#     """

#     readme = get_summarization(prompt1)

#     prompt2 = f"""
#     {readme}
#     Strictly the output need to be single line text
#     Provide a simple 1-line explanation about the project.
#     1-line description as plain text, without any special formatting like LaTeX or markdown. 
#     """

#     simple_summary = get_summarization(prompt2)

#     return readme, simple_summary






# st.title("Github Readme file Generator")
# url = st.text_input("Enter Github Repo URL: ")
# if st.button("Generate Readme file"):

#     text, simple_summary = get_python_files_content(url)

#     st.write("Simple explanation about the Project: ")
#     st.code(simple_summary[7:-1])
#     st.write("Readme.md content")
#     st.code(text[7:-1])

#     b64 = base64.b64encode(text.encode()).decode()  # Encode to base64 (not decode)
#     href = f'<a href="data:file/md;base64,{b64}" download="README.md">Download README.md</a>'
#     st.markdown(href, unsafe_allow_html=True)

# # if isinstance(python_files_content, list):
# #     for file_content in python_files_content:
# #         for line in file_content:
# #             print(line)
# #         print("--------------------------------------------------") #seperator for files.
# # else:
# #     print(python_files_content)

# # print(python_files_content)


