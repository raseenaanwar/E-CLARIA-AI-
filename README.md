# 🤖 E-CLARIA: Empowering Charity Leaders & Autonomous Resource Impact Assistant

E-CLARIA is an enterprise-grade AI platform designed to help charity leaders and nonprofit professionals craft intelligent fundraising strategies, collaborate with peers, and build sustainable impact — all powered by the latest in Groq + LLaMA 3/3.1 technology.

🚀 Built for the [RAISE Your Hack 2025 Hackathon](https://lablab.ai/event/raise-your-hack), E-CLARIA aligns with the **“Agentic Workflows for the Future of Work”** track.

---

## ✨ Key Features

- 🧠 **AI Strategy Generator** – Create customized fundraising roadmaps using LLaMA 3 via Groq API
- 📇 **User Profile Setup** – Personalized onboarding for nonprofits and charity leaders
- 🛰️ **Agentic Outreach** – Smart email/message generation for donor engagement
- 🤝 **Mentorship & Q&A Forum** – Connect with experienced mentors and ask/answer questions
- 🏆 **Gamified Engagement** – Earn points for participation and impact
- 🌱 **Sustainability Tracker** – Promote eco-friendly actions in fundraising

---

## 🧰 Tech Stack

| Layer            | Tools Used                                |
|------------------|-------------------------------------------|
| 👩‍💻 Frontend      | React, Tailwind CSS                      |
| ⚙️ Backend       | FastAPI, Python, PostgreSQL               |
| 🧠 AI Engine     | Groq API + Meta LLaMA 3/3.1               |
| ☁️ Deployment    | Vultr, Docker                             |

---

## 🧪 Setup Instructions (Local)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/e-claria.git
cd e-claria

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Set up environment variables (create a .env file)
touch .env
# Add your keys:
# GROQ_API_KEY=your_api_key_here
# DATABASE_URL=postgresql://user:pass@host:port/dbname

# 5. Run FastAPI backend
uvicorn main:app --reload
