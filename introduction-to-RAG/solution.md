
Q1. Why did the plain ChatGPT-style chatbot give wrong answers? (target length: ~100–150 words)

Be specific. Do not just define limitations in general — explain exactly why a plain LLM fails for a ShopEase use case. Your answer must clearly cover all three of the following:

The root cause — e.g., the LLM has no access to ShopEase's internal policy documents (lack of domain-specific context), and anything updated recently is beyond its training cutoff (static knowledge).
What hallucination means — and why it happens when the LLM has no real information to rely on.
One realistic wrong-answer example at ShopEase — use a real-looking number or policy line, e.g. "the chatbot told a customer that refunds take 3 days, when ShopEase's actual refund timeline is 7 working days." Make the example concrete, not generic.

Answer 1-
1. root cause- ShopEase's internal policy is a document that is personal to the company.this information is not fed to the LLM for fine tuning. this is because the policy can be changed at any time by the company.
Hallucination- When there is no information in LLM from which the query can be answered, it predicts and generates the answer without checking for facts. this can lead to LLM giving worng answers. this is called hallucinations.
Ex- when LLM is asked for the refund time, since it doesn't have the internal policy file, it will make up a seemingly real refund time and provide this to the user. this style of just providing answer without checking can lead to giving wrong information. 


Q2. What should the new assistant "read from" to give correct answers?

List 3 to 5 real-sounding ShopEase documents the assistant should be grounded on. For each, write one line describing the kind of question it helps answer.

(Example format: "Returns & Replacements Policy — answers questions about return windows, damaged products, and exchange rules.")

Answer 2-
 A few plausible sounding ShopEase documents-
 a. returns should be applied within 3 days of delivery. Any failure to do so cannot be considered for return.
 - it will help with users to answer questions related to return timeline.
 b. Replacements can only be done for products that have a manufacturing defect or damaged products.
 - this document will help to understand what products can be returned.
 c. for exhange offers to buy a new phone, the exchanged product has to be functional and the cost of that product is determined after being inspected by the company. the exchange price shown on the app is subject to changes based on the quakity of the product returned for exchange.



Q3. Walk through the 4-step RAG flow for one realistic ShopEase customer question. (target length: ~150–200 words)

Pick one realistic customer question (example: "I received a damaged mixer-grinder 5 days ago. Can I still get a replacement?"). Then explain each of the four RAG steps in proper detail — not in one line each. Your answer must clearly show:

Query — the exact customer question that reaches the assistant.
Retrieve — which ShopEase document is looked into, and what is actually retrieved (include a realistic 2–3 line example chunk from that document, e.g. a real-sounding rule from the Returns Policy).
Context — how the retrieved chunk is used — i.e., it is placed alongside the customer's question in the prompt given to the LLM, so the LLM now has both the question and the correct policy text in front of it.
Generate — how the retrieved context helps produce the final answer, and the final grounded answer the assistant gives the customer. Make it clear that the answer is built from the retrieved chunk, not from the LLM's guesswork.

Answer 3-
RAG flow for the customer query "I received a damaged mixer-grinder 5 days ago. Can I still get a replacement?"
Step 1- Query is tokenised and converted into vector embeddings. considering that the documents are also already available, they are converted into vector embeddings too.
Step 2- the vector embeddings of the documents are retreived based on the vector embeddings of the user query. this is basically a semantic search of the query. the words damaged is mapped with damaged or defected in the document. also because the product has to be returned for a replacement to happen, the document with return is also fetched.
Step 3- all these retrived documents are put with the user query. this helps the llm to have the query and the supported documents. from the above answer, the first and second documents are selected.
Step 4- now using the LLM transformer, the reply is generated and provided to the user. it combines the both documents and says something like "the return of a product has to be applied within 3 days of delivery, it also mentions about the product can only be replaced if it has a manufacturing defect."