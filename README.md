

# 🌿 Logiflow: The Human-Centric AI Logistics Bridge
!(LogiFlow/logiflowlogo.png)



## 📌 Project Vision

In modern supply chains, automation often creates a "black box"—systems make
decisions that humans don't understand or can't control. This leads to errors,
lack of trust, and massive food waste.

Logiflow flips this paradigm. We have built an Agentic Intelligence Bridge that
connects local producers and sellers directly to conscious consumers. Our system
doesn's just automate; it augments. It uses a multi-agent AI architecture to
identify opportunities (like reducing waste) and presents them to the human
operator for final authorization.

## 🧠 The "Human-in-the-Loop" (HITL) Philosophy

The core innovation of Logiflow is its Semi-Autonomous Decision Model. Unlike
traditional systems that execute tasks blindly, Logiflow operates on a "Propose
\rightarrow Authorize" workflow:

1.  Observation: AI Agents (Expiration & Stock) constantly monitor the data for
    "events" (e.g., an item is 2 days from expiry).
2.  Reasoning: The AI doesn't just flag an error; it generates a Strategic
    Proposal (e.g., "I suggest a 50% Zero-Waste discount to prevent loss").
3.  Human Authorization: The Seller receives a decision card. The AI cannot
    change prices or stock levels without a human "handshake." This ensures the
    merchant remains in total control of their business.

This builds a Bridge of Trust between the AI's speed and the Human's judgment.

## 🏗️ System Architecture

Logiflow is powered by a decentralized Multi-Agent System (MAS):

  - The Orchestrator: The central brain that routes user intents and manages
    agent handovers.
  - The Researcher Agent: Translates natural language queries (e. e., "Find me
    healthy breakfast options") into precise SQL-driven insights.
  - The Registrar Agent: Handles the structured entry of stock, ensuring data
    integrity.
  - The Proactive Co-Pilot (Expiration & Stock Agents): The "watchdogs" that
    scan for waste risks and low-stock events to generate intelligent proposals.
  - The Location Agent: Manages the spatial hierarchy, ensuring users find the
    exact "Pin" on the map.

## 🌍 Social & Environmental Impact

Logiflow is designed to drive the Circular Economy:

  - ♻️ Waste Reduction: By automatically identifying items nearing expiry and
    suggesting "Zero Waste" discounts, we divert food from landfills to
    consumers.
  - 🤝 Community Support: The system prioritsizes Local Producers, giving small
    farmers a digital "Voice" and a "Verified Local" badge to compete with
    big-box retailers.
  - 🎁 Donation Integration: When items reach a critical expiry threshold, the AI
    automatically transitions them to a "Donation Mode," facilitating easy
    connections with local food banks.

🚀 Key Features

| Feature              | Description                                         | Human Role                                |
| :------------------- | :-------------------------------------------------- | :---------------------------------------- |
| **Semantic Search**  | Natural language discovery for users.               | User explores.                            |
| **Zero-Waste Deals** | Dynamic pricing for expiring perishables.           | AI suggests $\rightarrow$ Human approves. |
| **Producer Badge**   | Highlighting local farm-to-table products.          | Verified via Seller Portal.               |
| **Decision Queue**   | A centralized hub for AI-generated proposals.       | Human provides final authority.           |
| **Impact Dashboard** | Real-time tracking of waste saved and money earned. | Human reviews performance.                |

🛠️ Installation & Running

This project is designed to run as a standalone interactive dashboard in a
Kaggle or Jupyter environment.

1.  Clone the repository:
    git clone https://github.com/your-username/logiflow.git
    cd logiflow
2.  Install dependencies:
    pip install pandas numpy ipywidgets
3.  Run the Dashboard: Open the notebook and run the main cell. You will see the
    interactive Seller Command Center and User Search Portal.

📝 License

Distributed under the Creative Commons License. See LICENSE for more information.

Developed for the Gemma 4 Hackathon — Building the future of human-AI
collaboration.
