from support_assisstant_agent import agent_executor

TEST_PACK= [
    {
        "id": "T1_SINGLE_TOOL_STATUS",
        "query":"What is the status of the order ORD_101",
        "query_class":"single-tool-query",
        "expected_tools":["get_order_status"]
    },
    {
        "id": "T2_MULTI_TOOL_STATUS",
        "query":"What is the status of the order ORD_101 and also tell me the refund amount",
        "query_class":"multi-tool-query",
        "expected_tools":["get_order_status","calculate_refund_amount"]
    },
    {
        "id": "T3_NO_TOOL_CONCEPTUAL",
        "query":"What is refund in simple words",
        "query_class":"no-tool-query",
        "expected_tools":[]
    },
    {
        "id": "T4_MISSING_ORDER_ID",
        "query":"What is the status of my order_id",
        "query_class":"invalid_order_id_query",
        "expected_tools":[]
    }
]


def run_test_pack():
    for test_case in TEST_PACK:
        print("Test Case Id:", test_case["id"])
        print("Test Case Class:", test_case["query_class"])
        print("Test Case query:", test_case["query"])

        result = agent_executor.invoke(
            {
                "input": test_case["query"]
            }
        )