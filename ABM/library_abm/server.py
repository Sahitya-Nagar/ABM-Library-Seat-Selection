from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from library_model import (
    LibraryModel,
    get_utilization,
    get_avg_satisfaction,
    get_total_entered,
    get_seated,
    get_rejected
)
from seat import Seat
from student_agent import StudentAgent


SEAT_STYLES = {
    "quiet":    {"color": "#aed6f1", "label": "Q", "text_color": "#1a5276"},
    "window":   {"color": "#a9dfbf", "label": "W", "text_color": "#196f3d"},
    "charging": {"color": "#fad7a0", "label": "C", "text_color": "#935116"},
    "normal":   {"color": "#d5d8dc", "label": "R", "text_color": "#555555"},
}


class StatsPanel(TextElement):
    def render(self, model):
        util = round(get_utilization(model), 1)
        sat = round(get_avg_satisfaction(model), 1)
        seated = model.metrics["seated"]
        rej = model.metrics["rejected"]

        return f"""
        <div style="
            display:flex;
            justify-content:space-around;
            padding:15px;
            background:#f8f9fa;
            border-radius:8px;
            border:1px solid #dee2e6;
            margin-bottom:15px;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            
            <div style="text-align:center">
                <div style="font-size:24px; font-weight:bold; color:#2ecc71;">{util}%</div>
                <div style="font-size:12px; color:#6c757d; text-transform:uppercase;">Utilization</div>
            </div>

            <div style="text-align:center">
                <div style="font-size:24px; font-weight:bold; color:#3498db;">{sat}</div>
                <div style="font-size:12px; color:#6c757d; text-transform:uppercase;">Avg Satisfaction</div>
            </div>

            <div style="text-align:center">
                <div style="font-size:24px; font-weight:bold; color:#9b59b6;">{seated}</div>
                <div style="font-size:12px; color:#6c757d; text-transform:uppercase;">Currently Seated</div>
            </div>

            <div style="text-align:center">
                <div style="font-size:24px; font-weight:bold; color:#e74c3c;">{rej}</div>
                <div style="font-size:12px; color:#6c757d; text-transform:uppercase;">Total Rejected</div>
            </div>
        </div>
        """


class LegendPanel(TextElement):
    def render(self, model):
        return """
        <div style="
            position: absolute;
            top: 260px;
            right: 112px;
            width: 250px;
            z-index: 999;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size:13px;
            padding:14px;
            background:#ffffff;
            border:1px solid #dee2e6;
            border-radius:10px;
            line-height:1.8;
            box-shadow:0 2px 8px rgba(0,0,0,0.12);
        ">
            <b style="
                font-size:15px;
                color:#2c3e50;
                border-bottom:1px solid #eee;
                display:block;
                margin-bottom:10px;
                padding-bottom:6px;
            ">Floor Plan Legend</b>

            <div style="display:grid; grid-template-columns:1fr; gap:6px;">
                <span><span style="color:#aed6f1; font-size:18px;">■</span> <b>Q:</b> Quiet Zone</span>
                <span><span style="color:#a9dfbf; font-size:18px;">■</span> <b>W:</b> Window Seats</span>
                <span><span style="color:#fad7a0; font-size:18px;">■</span> <b>C:</b> Charging Hub</span>
                <span><span style="color:#d5d8dc; font-size:18px;">■</span> <b>R:</b> Regular Seating</span>
                <span><span style="color:#c0392b; font-size:18px;">■</span> <b>S:</b> Occupied</span>
                <span><span style="color:#27ae60; font-size:18px;">●</span> Student Agent</span>
            </div>
        </div>
        """


def library_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if isinstance(agent, Seat):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.85
        portrayal["h"] = 0.85
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0

        if agent.occupied:
            portrayal["Color"] = "#c0392b"
            portrayal["text"] = "S"
            portrayal["text_color"] = "white"
        else:
            style = SEAT_STYLES.get(agent.seat_type, SEAT_STYLES["normal"])
            portrayal["Color"] = style["color"]
            portrayal["text"] = style["label"]
            portrayal["text_color"] = style["text_color"]

    elif isinstance(agent, StudentAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.42
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Color"] = "#27ae60"

    return portrayal


stats = StatsPanel()
legend = LegendPanel()

grid = CanvasGrid(library_portrayal, 20, 20, 550, 550)

combined_chart = ChartModule([
    {"Label": "Seat Utilization (%)", "Color": "#2ecc71"},
    {"Label": "Average Satisfaction", "Color": "#3498db"},
    {"Label": "Rejected", "Color": "#e74c3c"},
])

throughput_chart = ChartModule([
    {"Label": "Total Entered", "Color": "#9b59b6"},
    {"Label": "Seated", "Color": "#27ae60"},
])

model_params = {
    "students_per_step": Slider("Students per step", value=2, min_value=1, max_value=10, step=1),
    "num_quiet": Slider("Quiet Seats", value=30, min_value=0, max_value=30, step=1),
    "num_charging": Slider("Charging Seats", value=25, min_value=0, max_value=25, step=1),
    "total_capacity": Slider("Total Capacity", value=144, min_value=30, max_value=144, step=10),
}

DESCRIPTION = """
<div style="font-family:'Segoe UI', Arial, sans-serif; line-height:1.6; color:#444; max-width:800px;">
    <h4 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"> Library Seat Selection ABM</h4>
    <p>This model simulates student behavior in a library environment, analyzing how seat preferences and study durations impact overall capacity and satisfaction.</p>
    
    <h5 style="color:#2980b9;"> Quick Start</h5>
    <p>Adjust the <b>Total Capacity</b> and <b>Students per step</b> sliders to observe how the library handles different load levels.</p>
</div>
"""

server = ModularServer(
    LibraryModel,
    [stats, grid, legend, combined_chart, throughput_chart],
    " Library Seat Selection Dashboard",
    model_params
)

server.description = DESCRIPTION
server.port = 8521