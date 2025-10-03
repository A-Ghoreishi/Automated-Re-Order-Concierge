import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("LLM_API_KEY"))

def draft_purchase_order(item: dict):
    prompt = f"""
    Write a professional purchase order email:

    SKU: {item['item_sku']}
    Item: {item['item_name']}
    Quantity: {item['order_qty']}
    Supplier: {item['supplier_name']}
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a purchasing agent."},
                  {"role":"user","content":prompt}]
    )

    return resp.choices[0].message.content.strip()
