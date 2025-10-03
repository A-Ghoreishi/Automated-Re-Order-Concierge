# 📦 Automated Re-Order Concierge  
*(Educational Project with LangGraph + HITL + Google Sheets + Email)*

---

## 🎯 Project Overview  

Small online retailers often lose sales when stock runs out unexpectedly. This project demonstrates how to design an **AI-powered workflow** that:  

- Monitors inventory data stored in **Google Sheets**.  
- Detects items that fall below a **reorder threshold**.  
- Requests human approval before placing a purchase order (HITL – *Human in the Loop*).  
- Uses an **LLM** to draft a professional purchase order.  
- Sends the PO to the supplier by email and logs the action back into Google Sheets.  

This project is for **educational purposes** — to show how to orchestrate AI + automation + human approval into a state machine workflow using **LangGraph**.

---

## 🛠️ Architecture & Workflow  

### Core Flow (State Machine)  

```

CheckInventory → NeedApproval → WaitForReply → [Confirmed | Rejected] → Update Sheet → Done

```

1. **Check Inventory**  
   - Reads stock levels from Google Sheets.  
   - Selects items where `on_hand_qty < reorder_threshold`.  

2. **Need Approval (HITL)**  
   - Sends an email to the store owner with item details.  
   - Asks the owner to reply `YES` or `NO`.  

3. **Wait for Reply**  
   - Connects to the mailbox (IMAP).  
   - Reads the owner’s reply.  

4. **Confirm Path**  
   - Updates Google Sheet (`last_checked`, `comments`).  
   - Uses an LLM to draft a **purchase order (PO)**.  
   - Sends PO to supplier via email.  

5. **Reject Path**  
   - Updates Google Sheet (`last_checked`, `comments = "Rejected by owner"`).  

6. **Error Handling**  
   - If an email fails, the workflow notifies the owner immediately.  

---

## 📂 Project Structure  

```

auto-reorder-concierge/
├── README.md
├── requirements.txt
├── .env.example
├── demo/
│   └── inventory_template.csv
└── src/
├── main.py                 # Entry point
├── langgraph_workflow.py   # Orchestrates state machine
├── google_sheets.py        # Read/write Google Sheets
├── email_client.py         # Send/receive emails
└── po_draft.py             # LLM-generated Purchase Orders

````

---

## ⚙️ Setup Instructions  

### 1. Install Dependencies  
```bash
pip install -r requirements.txt
````

### 2. Configure Google Sheets

1. Create a **Google Cloud Project**.
2. Generate a **Service Account JSON key**.
3. Share your Google Sheet with the `client_email` from that JSON.
4. Import the sample `demo/inventory_template.csv` into the sheet.

### 3. Configure Email (Liara)

* Create a Liara Mailbox or connect your domain.
* Add SMTP/IMAP details to `.env`.
* Example:

  ```bash
  EMAIL_HOST=smtp.liara.ir
  EMAIL_PORT=587
  EMAIL_IMAP=imap.liara.ir
  EMAIL_USER=orders@yourdomain.com
  EMAIL_PASS=yourpassword
  ```

### 4. LLM API Key

Add your **OpenAI API key** (or other LLM provider):

```bash
LLM_API_KEY=sk-xxxxxxxx
```

### 5. Environment Variables

Copy `.env.example` → `.env` and fill your values.

---

## ▶️ Running the Workflow

From the project root:

```bash
python -m src.main
```

* The workflow checks inventory.
* Sends approval emails for low-stock items.
* Waits for owner reply.
* Drafts & sends POs (if approved).
* Updates Google Sheets.

---

## 🎥 Demo Checklist

When recording your demo:

1. Show Google Sheet with a low-stock item.
2. Run the workflow manually.
3. Show the approval email arriving in the owner’s inbox.
4. Reply `YES` → workflow drafts & sends PO to supplier.
5. Show updated Google Sheet with approval log.

---

## 🔍 Educational Takeaways

* **LangGraph** helps model business logic as a clear state machine.
* **Google Sheets** works as a lightweight database for inventory.
* **HITL (Human in the Loop)** ensures humans stay in control of critical actions.
* **LLMs** can automate structured business tasks like drafting a purchase order.
* **Email Integration** turns the workflow into a practical, end-to-end automation.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Do not use in production without proper security, error handling, and domain/email verification.

---

```

---

✅ This README is written for teaching purposes: clear, structured, and explains *why* each part exists.  

Do you want me to also add a **diagram/flowchart (in Markdown with Mermaid)** to visually show the workflow?
```
