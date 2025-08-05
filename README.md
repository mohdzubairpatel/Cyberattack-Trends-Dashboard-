# 🛡️ CyberAttack Trend Dashboard

An interactive data analytics dashboard built using **Python**, **Streamlit**, and **Plotly** to explore trends in global cyberattacks, financial impacts, and targeted industries. This tool supports filtering, forecasting, and exporting reports based on a sample cybersecurity dataset (2015–2024).

---

## 📊 Project Highlights

- 🔍 **Explore Trends**: Analyze the frequency of cyberattacks over time across countries, industries, and attack types.
- 📈 **Forecast Attacks**: Predict future cyberattack trends using machine learning-based forecasting.
- 💸 **Financial Loss Insights**: Identify regions with the highest financial impact.
- 🏭 **Industry Vulnerability**: See which industries are most targeted over time.
- 📄 **PDF & CSV Export**: Download filtered incident reports and summary reports.
- 🎥 **Animated Trend Explorer**: Visualize trends over years via dynamic bubble charts.

---

## 🚀 Live Demo

> ⚠️ Deployment link not added.  
> You can deploy it to **Streamlit Cloud** or **Hugging Face Spaces**.

---

## 📁 Folder Structure

CyberAttack_Trend_Dashboard/
│
├── data/
│ ├── cyberattacks_by_year.csv
│ └── Global_Cybersecurity_Threats_2015-2024.csv
│ └── forecast_attacks.csv
│
├── app.py # Main Streamlit dashboard file
├── forecast.py # Forecasting script 
├── requirements.txt # Python dependencies
└── README.md # You're reading it


---

## 🧪 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) + [Plotly](https://plotly.com/python/)
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly Express
- **PDF Export**: FPDF
- **Forecasting**: Prophet / Preprocessed CSV (optional)

---

## ⚙️ Installation & Run Locally

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/CyberAttack_Trend_Dashboard.git
cd CyberAttack_Trend_Dashboard

Install dependencies
pip install -r requirements.txt

Run the app
streamlit run app.py

📥 Sample Data Used
All data is mocked for demonstration purposes and does not reflect real cyberattacks.
The datasets simulate patterns for educational and internship use only.

📌 License
This project is open-source and free to use under the MIT License.

✍️ Author
Mohammed Zubair
Data Analytics & Cybersecurity 

🔗 LinkedIn
📧 mohammedzubair@example.com
🌐 GitHub

⭐ Acknowledgment
Inspired by real-world dashboarding practices in cybersecurity analytics.

