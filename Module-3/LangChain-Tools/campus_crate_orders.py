import json
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()
MODEL_NAME= "gpt-5.2"

ORDERS_DB = {
    "CC2001": {
        "order_id": "CC2001",
        "item": "Hoodie — Batch 2026",
        "status": "shipped",
        "eta_days": 3,
    },
}


# TODO 1: Define OrderStatusInput (Pydantic)
class OrderStatusInput(BaseModel):
   order_id : str = Field(description="Format of the order_id is CC2001")


# TODO 2: Define get_order_status with @tool
@tool(args_schema=OrderStatusInput)
def get_order_status(order_id: str):
   
   order_id= order_id.strip().upper()
   order= ORDERS_DB.get(order_id)

   if not order:
      return json.dumps({"ok": False, "message": "Order not found"})
   json.dumps({"ok": True, "order": order})



# TODO 3: Create model and model_with_tools = model.bind_tools(...)
model= init_chat_model(MODEL_NAME, temperature= 0)
model_with_tools = model.bind_tools([get_order_status])


def run_order_help(user_query: str) -> str:
  # TODO 4: Build messages, invoke, handle tool_calls or return early,
  #         then second invoke after ToolMessage(s)
  messages = [
        {
            "role": "system",
            "content": ("use the order tool when the user asks about an order")
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
  ai_msg= model_with_tools.invoke(messages)
  messages.append(ai_msg)

  if not ai_msg.tool_calls:
     return ai_msg.content
  
  for tool_call in ai_msg.tool_calls:
     tool_msg= get_order_status.invoke(tool_call["args"])
     messages.append(tool_msg)
  
  final_answer= model_with_tools.invoke(messages)
  
  return final_answer.content


if __name__ == "__main__":
        queries=[
            "Where is my order CC2001?",
            "What is Python?"
        ]

        for query in queries:
            print ("\n"+ "=" * 100)
            print ("USER:", query)
            final_answer=run_order_help(query)
            print ("\nFINAL ANSWER")
            print(final_answer)
        # TODO 5: Run the two test queries and print answers
       
    
