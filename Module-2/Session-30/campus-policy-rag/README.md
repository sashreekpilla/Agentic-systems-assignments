This project "Campus Policy Rag" responds to student's queries based on the context provided from the campus policy documents. 
If the student query is not related to any document in the campus policy document, LLM must let the student know that there's no document related to it instead of guessing.

Steps to run the program-
1. Create and activate virtual environment.
2. After installing all the packages from the requirements.txt file.
3. set the gemini api key or openai api key in the terminal so that its not exposed in the code.


--some basic snippets to run in the terminal are--

1. py -m venv venv   # This is to create a virtual environment.

2. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
3. .\venv\Scripts\Activate.ps1  # These two lines of snippet will activate the virtual environment.

4. $env:GEMINI_API_KEY= "" # This is used to set the global environment variable

5. $env:OPENAI_API_KEY= "" # This is used to set the global environment variable

6. echo $env:GEMINI_API_KEY # This is used to view the global environment variable

7. echo $env:OPENAI_API_KEY # This is used to view the global environment variable

#Some basic things to install using the terminal

1. py -m pip install chromadb # This install a package for a vector database called chromadb

2. py -m pip install google-genai # This snippet installs a package used for making google LLM calls.

3. py -m pip install openai # This snippet installs a package used for making calls to openai.


#To run the program file.
py -m campus_policy_rag # This snippet is used to run the program.