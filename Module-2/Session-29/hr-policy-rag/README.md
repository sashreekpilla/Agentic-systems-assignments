This project "HR Policy Rag" responds to employee's queries based on the context provided from the hr policy documents. 
If the user query is not related to any document in the hr policy document, LLM must let the employee know that there's no document related to it instead of guessing.

Steps to run the program-
1. Create and activate virtual environment.
2. After installing all the packages from the requirements.txt file.
3. set the gemini api key in the terminal so that its not exposed in the code.
4. use the last snippet from the requirements.txt to run the hr_policy_rag file.


--some basic snippets to run in the terminal are--

1. py -m venv venv   # This is to create a virtual environment.

2. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
3. .\venv\Scripts\Activate.ps1  # These two lines of snippet will activate the virtual environment.

4. $env:GEMINI_API_KEY= "" # This is used to set the global environment variable
5. echo $env:GEMINI_API_KEY # This is used to view the global environment variable

#Some basic things to install using the terminal

1. py -m pip install chromadb # This install a package for a vector database called chromadb

2. py -m pip install google-genai # This snippet installs a package used for making google LLM calls.


#To run the program file.
py -m hr_policy_rag # This snippet is used to run the program.