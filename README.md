# 📚 Library Seat Selection Agent-Based Model (ABM)

A professional Agent-Based Model built with **Python** and the **Mesa** framework to simulate and analyze student seat-selection behavior in a university library.

![Library ABM Screenshot](https://raw.githubusercontent.com/project-placeholder/link-to-screenshot.png) *(Note: Add your own screenshot here!)*

## 📑 Overview

This simulation explores how environmental factors (seat types) and individual student preferences (Quiet, Window, Charging, or Regular) affect:
- **Library Utilization:** How effectively the space is used.
- **Student Satisfaction:** Whether students find their preferred study environment.
- **Rejection Rates:** How often the library reaches capacity and turns students away.

## 🚀 Key Features

- **Dynamic Interactive Dashboard:** Real-time visualization using Mesa's browser-based interface.
- **KPI Tracking:** Live header display for Utilization, Satisfaction, and Seated counts.
- **Rich Visualization:** 
  - **Grid Legend:** Easy interpretation of seat zones (Quiet, Window, etc.).
  - **Multi-Line Performance Charts:** Overlaid data series to observe correlations between metrics.
  - **Throughput Analysis:** Comparison of total arrivals vs. currently seated students.
- **Configurable Parameters:** Adjust students per step, seat distributions, and total capacity on the fly via sidebar sliders.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** [Mesa](https://mesa.readthedocs.io/) (Agent-Based Modeling)
- **Data Handling:** NumPy, Pandas
- **Visualization:** Matplotlib, JavaScript/HTML (Mesa UI)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/library-abm.git
   cd library-abm
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🏃 Usage

Launch the visualization server by running:
```bash
python run.py
```
Then, open your browser and navigate to:
`http://127.0.0.1:8521/`

### 🧪 Experimentation Tips
To observe the **Rejected** student spike:
1. Increase **Students per step** to the maximum (10).
2. Decrease **Total Capacity** to the minimum (30).
3. Click **Reset** and **Start**. Watch the rejections skyrocket as the library hits 100% capacity!

## 📂 Project Structure

- `library_model.py`: Core model logic and metrics collection.
- `student_agent.py`: Student agent behavior, preference logic, and satisfaction scoring.
- `seat.py`: Seat agent definition and occupancy state.
- `server.py`: Visualization server configuration, UI panels, and charts.
- `run.py`: Entry point script to launch the simulation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
*Created for the Library Seat Selection ABM Project.*
