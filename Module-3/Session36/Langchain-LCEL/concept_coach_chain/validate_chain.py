from build_chain import build_chain

def is_response_valid(response: str) -> tuple[bool, list[str]]:
    errors = []

    if not isinstance(response, str):
        errors.append("Response is not a string")
        return False, errors
    
    if not response.strip():
        errors.append("Response is empty")

    word_count= len(response.split())

    if word_count > 100:
        errors.append("Response longer than 100 words")

    return len(errors)==0 , errors

chain= build_chain()
test_case= {
    "topic":"LangChain Expression Language",
    "analogy_domain":"school assembly line"
}

response= chain.invoke(test_case)
print(response)

is_valid, errors = is_response_valid(response)

if is_valid:
    print ("Valid response")
else:
    print("Invalid response")
    print(errors)

