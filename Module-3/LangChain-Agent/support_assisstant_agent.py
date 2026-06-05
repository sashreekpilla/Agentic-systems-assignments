from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgnetExecutor, create_tool_calling_agent

ORDERS_DB={
    "ORD-101":{
        "status":"shipped",
        "city":"Delhi",
        "amount":2500,
        "delivery_days":2
    },
    "ORD-102":{
        "status":"delivered",
        "city":"Bangalore",
        "amount":3000,
        "delivery_days":0
    },
    "ORD-103":{
        "status":"cancelled",
        "city":"Mumbai",
        "amount":1500,
        "delivery_days":0
    }
}

@tool
def get_order_status(order_id:str)-> str:
    order= ORDERS_DB.get(order_id)

    if not order:
        return f"No order found for the given order_id: {order_id}"
    
    return(
        f"Order id:{order_id}"
        f"Order status:{order["status"]}"
        f"city: {order["city"]}"
        f"Order amount: {order["amount"]}"
    )

@tool
def estimate_delivery_timeline(order_id:str) -> str:
    order= ORDERS_DB.get(order_id)

    if not order:
        return f"No order found for the given order_id: {order_id}"
    
    if order["status"]=="delivered":
        return f"Order {order_id} has already been delivered"
    
    if order["status"]== "cancelled":
        return f"Order {order_id} has beeen cancelled."
    
    if order["status"]== "shipped":
        return f"Order {order_id} has been shipped and expected to be arrived in {order["delivery_days"]} days"
    
    return f"Delivery status for order id: {order_id} is not available"

@tool
def calculate_refund_amount(order_id:str) -> str:
    order= ORDERS_DB.get(order_id)

    if not order:
        return f"No order founf for the given order_id: {order_id}"
    
    if order["status"]== "cancelled":
        return f"Refund amount for the order_id: {order_id} is {order["amount"]} rupees"
    
    if order["status"]== "delivered":
        return f"Refund amount for the order_id: {order_id} is based on product policy"
    
    return f"Refund for the order_id:{order_id} cannot be calculated at this point"
    
    
tools=[
    get_order_status,
    estimate_delivery_timeline,
    calculate_refund_amount
]


llm=ChatOpenAI(
    model="gpt-5.2",
    temperature= 0
)

prompt= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful e-commerce support assistant.

Rules:
1. Use tools only when required.
2. If the user asks about a specific order, use the relevant tool.
3. If the user asks a general conceptual question, answer it directly without tools.
4. If the order id is missing, ask the user for the order id.
5. Keep the final answer clear and beginner-friendly.
            """
        ),
        ("human","{input}"),
        MessagesPlaceholder(variable_name="agents_scratchpad")
    ]
)

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgnetExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

query= "For the order_id ORD_102, check the status, tell me the delivery estimate and refund amount"

result= agent_executor.invoke(
    {
        "input": query
    }
)

print (result["output"])

print("="*100)

for index,step in enumerate(result["intermediate_steps"], start=1):
    action, observation = step
    print(f"Step-{index}")
    print(f"Tool selected: {action.tool}")
    print(f"Tool input: {action.tool_input}")
    print(f"Tool observation:", observation)


