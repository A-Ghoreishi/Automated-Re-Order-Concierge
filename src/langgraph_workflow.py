from datetime import datetime
from langgraph.graph import StateGraph, END
from src.google_sheets import read_inventory, update_inventory_row
from src.email_client import send_email, check_inbox
from src.po_draft import draft_purchase_order
import os

OWNER_EMAIL = os.getenv("OWNER_EMAIL")


class AgentState(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def check_inventory(state: AgentState):
    print("📦 Checking inventory...")
    items = read_inventory()
    low_stock = [i for i in items if int(i["on_hand_qty"]) < int(i["reorder_threshold"])]
    state["items"] = low_stock
    state["current_index"] = 0
    if not low_stock:
        print("✅ No low-stock items.")
    else:
        print(f"⚠️ Found {len(low_stock)} low-stock items.")
    return state


def need_approval(state: AgentState):
    item = state["items"][state["current_index"]]
    subject = f"Reorder Approval Needed: {item['item_name']} ({item['item_sku']})"
    body = f"""
    Item: {item['item_name']}
    SKU: {item['item_sku']}
    Current Qty: {item['on_hand_qty']}
    Threshold: {item['reorder_threshold']}
    Order Qty: {item['order_qty']}

    Reply YES to confirm, NO to reject.
    """
    send_email(OWNER_EMAIL, subject, body)
    return state


def wait_for_reply(state: AgentState):
    item = state["items"][state["current_index"]]
    subject = f"Reorder Approval Needed: {item['item_name']} ({item['item_sku']})"
    print("⏳ Waiting for reply...")
    reply = check_inbox(subject)
    if not reply:
        print("❌ No reply found yet. Defaulting to NO.")
        reply = "NO"
    state["owner_reply"] = reply.strip().upper()
    return state


def confirmed(state: AgentState):
    item = state["items"][state["current_index"]]
    print(f"✅ Approved reorder for {item['item_name']}")
    po_text = draft_purchase_order(item)
    send_email(item["supplier_email"], f"Purchase Order: {item['item_name']}", po_text)
    update_inventory_row(item["item_sku"], {
        "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comments": "Approved by owner"
    })
    return state


def rejected(state: AgentState):
    item = state["items"][state["current_index"]]
    print(f"❌ Rejected reorder for {item['item_name']}")
    update_inventory_row(item["item_sku"], {
        "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comments": "Rejected by owner"
    })
    return state


def move_to_next_or_end(state: AgentState):
    state["current_index"] += 1
    if state["current_index"] < len(state["items"]):
        return "need_approval"
    return END


def run_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("check_inventory", check_inventory)
    workflow.add_node("need_approval", need_approval)
    workflow.add_node("wait_for_reply", wait_for_reply)
    workflow.add_node("confirmed", confirmed)
    workflow.add_node("rejected", rejected)

    workflow.set_entry_point("check_inventory")

    def branch_on_items(state: AgentState):
        return "need_approval" if state.get("items") else END

    workflow.add_conditional_edges("check_inventory", branch_on_items,
        {"need_approval": "need_approval", END: END})

    workflow.add_edge("need_approval", "wait_for_reply")

    def branch_on_reply(state: AgentState):
        return "confirmed" if state.get("owner_reply") == "YES" else "rejected"

    workflow.add_conditional_edges("wait_for_reply", branch_on_reply,
        {"confirmed": "confirmed", "rejected": "rejected"})

    workflow.add_conditional_edges("confirmed", move_to_next_or_end,
        {"need_approval": "need_approval", END: END})
    workflow.add_conditional_edges("rejected", move_to_next_or_end,
        {"need_approval": "need_approval", END: END})

    app = workflow.compile()
    app.invoke(AgentState())
