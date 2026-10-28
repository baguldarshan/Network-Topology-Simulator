import tkinter as tk
from tkinter import ttk
import math


# ---------- COLOR THEME ----------
BG = "#0B1120"
SIDEBAR = "#111827"
PANEL = "#172033"
BORDER = "#293548"
ACCENT = "#6366F1"
GREEN = "#10B981"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
CANVAS_BG = "#F8FAFC"
LINE = "#CBD5E1"


class NetworkTopologySimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("NetTopology | Network Simulator")
        self.root.geometry("1200x760")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.topology = tk.StringVar(value="Star")
        self.computer_count = 5

        self.setup_styles()
        self.create_interface()

        self.root.after(100, self.draw_network)

    # ---------- STYLES ----------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=BORDER,
            padding=8
        )

        style.configure(
            "Modern.TButton",
            background=PANEL,
            foreground=TEXT,
            padding=(12, 9),
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.map(
            "Modern.TButton",
            background=[("active", "#263449")]
        )

    # ---------- MAIN INTERFACE ----------
    def create_interface(self):

        # Main layout
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(fill="both", expand=True)

        # Sidebar
        self.create_sidebar()

        # Main content
        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=24,
            pady=20
        )

        self.create_header()
        self.create_toolbar()
        self.create_canvas()
        self.create_status_bar()

    # ---------- SIDEBAR ----------
    def create_sidebar(self):

        sidebar = tk.Frame(
            self.main,
            bg=SIDEBAR,
            width=230
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="◈  NetTopology",
            bg=SIDEBAR,
            fg=TEXT,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", padx=22, pady=(28, 5))

        tk.Label(
            sidebar,
            text="NETWORK LABORATORY",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=24, pady=(0, 35))

        self.sidebar_item(sidebar, "▦   Dashboard", True)
        self.sidebar_item(sidebar, "◎   Topologies", False)
        self.sidebar_item(sidebar, "⇄   Packet Routing", False)
        self.sidebar_item(sidebar, "▤   Network Devices", False)

        tk.Frame(
            sidebar,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=18, pady=24)

        tk.Label(
            sidebar,
            text="PROJECT DETAILS",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=23, pady=(0, 12))

        tk.Label(
            sidebar,
            text="Computer Networks\nSemester V\n\nTopology Visualization\n& Simulation",
            bg=SIDEBAR,
            fg=TEXT,
            justify="left",
            font=("Segoe UI", 10),
            wraplength=180
        ).pack(anchor="w", padx=23)

        tk.Label(
            sidebar,
            text="●  System Ready",
            bg=SIDEBAR,
            fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(side="bottom", anchor="w", padx=23, pady=25)

    def sidebar_item(self, parent, text, selected):

        color = "#252B54" if selected else SIDEBAR
        fg = "#A5B4FC" if selected else MUTED

        tk.Label(
            parent,
            text=text,
            bg=color,
            fg=fg,
            font=("Segoe UI", 10, "bold" if selected else "normal"),
            padx=15,
            pady=13,
            anchor="w"
        ).pack(fill="x", padx=12, pady=3)

    # ---------- HEADER ----------
    def create_header(self):

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill="x", pady=(0, 22))

        left = tk.Frame(header, bg=BG)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(
            left,
            text="Network Topology Simulator",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Visualize network structures and connections",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            header,
            text="●  SIMULATION READY",
            bg="#12352E",
            fg="#6EE7B7",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=10
        ).pack(side="right", anchor="center")

    # ---------- TOOLBAR ----------
    def create_toolbar(self):

        toolbar = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        toolbar.pack(fill="x", pady=(0, 18))

        tk.Label(
            toolbar,
            text="TOPOLOGY",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, padx=(16, 8), pady=16)

        self.topology_box = ttk.Combobox(
            toolbar,
            textvariable=self.topology,
            values=["Star", "Bus", "Ring", "Mesh"],
            state="readonly",
            width=12,
            style="Modern.TCombobox"
        )
        self.topology_box.grid(row=0, column=1, padx=5, pady=12)

        self.topology_box.bind(
            "<<ComboboxSelected>>",
            self.change_topology
        )

        ttk.Button(
            toolbar,
            text="+ Add Computer",
            style="Modern.TButton",
            command=self.add_computer
        ).grid(row=0, column=2, padx=(16, 5), pady=12)

        ttk.Button(
            toolbar,
            text="− Remove",
            style="Modern.TButton",
            command=self.remove_computer
        ).grid(row=0, column=3, padx=5, pady=12)

        toolbar.grid_columnconfigure(4, weight=1)

    # ---------- NETWORK CANVAS ----------
    def create_canvas(self):

        card = tk.Frame(
            self.content,
            bg=CANVAS_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        canvas_header = tk.Frame(card, bg=CANVAS_BG)
        canvas_header.pack(fill="x", padx=18, pady=14)

        tk.Label(
            canvas_header,
            text="NETWORK WORKSPACE",
            bg=CANVAS_BG,
            fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        tk.Label(
            canvas_header,
            text="● Computers     ━ Connections",
            bg=CANVAS_BG,
            fg="#64748B",
            font=("Segoe UI", 9)
        ).pack(side="right")

        self.canvas = tk.Canvas(
            card,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.draw_network()
        )

    # ---------- STATUS BAR ----------
    def create_status_bar(self):

        self.status = tk.StringVar(value="Initializing network...")

        footer = tk.Frame(self.content, bg=BG)
        footer.pack(fill="x", pady=(14, 0))

        tk.Label(
            footer,
            textvariable=self.status,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="left")

        tk.Label(
            footer,
            text="NetTopology v1.0",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="right")

    # ---------- TOPOLOGY ----------
    def change_topology(self, event=None):
        self.draw_network()

    def add_computer(self):

        if self.computer_count >= 8:
            self.status.set("Maximum limit: 8 computers.")
            return

        self.computer_count += 1
        self.draw_network()

    def remove_computer(self):

        if self.computer_count <= 2:
            self.status.set("At least 2 computers are required.")
            return

        self.computer_count -= 1
        self.draw_network()

    def draw_network(self):

        if not hasattr(self, "canvas"):
            return

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            return

        center_x = width / 2
        center_y = height / 2
        radius = min(width * 0.34, height * 0.34)

        topology = self.topology.get()
        positions = {}

        # Calculate computer positions
        for i in range(self.computer_count):

            angle = (
                2 * math.pi * i / self.computer_count
                - math.pi / 2
            )

            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            positions[f"PC{i + 1}"] = (x, y)

        # Draw network connections
        if topology == "Star":

            for x, y in positions.values():
                self.canvas.create_line(
                    center_x, center_y, x, y,
                    fill=LINE,
                    width=2
                )

        elif topology == "Bus":

            bus_y = center_y

            self.canvas.create_line(
                center_x - radius - 35,
                bus_y,
                center_x + radius + 35,
                bus_y,
                fill="#64748B",
                width=4
            )

            for x, y in positions.values():
                self.canvas.create_line(
                    x, bus_y, x, y,
                    fill=LINE,
                    width=2
                )

        elif topology == "Ring":

            names = list(positions.keys())

            for i in range(len(names)):

                x1, y1 = positions[names[i]]
                x2, y2 = positions[
                    names[(i + 1) % len(names)]
                ]

                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=LINE,
                    width=2
                )

        elif topology == "Mesh":

            names = list(positions.keys())

            for i in range(len(names)):
                for j in range(i + 1, len(names)):

                    x1, y1 = positions[names[i]]
                    x2, y2 = positions[names[j]]

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=LINE,
                        width=2
                    )

        # Draw central switch
        if topology == "Star":

            self.canvas.create_oval(
                center_x - 25,
                center_y - 25,
                center_x + 25,
                center_y + 25,
                fill=ACCENT,
                outline="white",
                width=3
            )

            self.canvas.create_text(
                center_x,
                center_y,
                text="SW1",
                fill="white",
                font=("Segoe UI", 9, "bold")
            )

        # Draw computers
        for name, (x, y) in positions.items():

            self.canvas.create_oval(
                x - 24, y - 24,
                x + 24, y + 24,
                fill=GREEN,
                outline="white",
                width=3
            )

            self.canvas.create_text(
                x, y,
                text=name,
                fill="white",
                font=("Segoe UI", 9, "bold")
            )

        # Workspace title
        self.canvas.create_text(
            center_x,
            20,
            text=f"{topology.upper()} TOPOLOGY",
            fill="#334155",
            font=("Segoe UI", 12, "bold")
        )

        connection_count = (
            self.computer_count
            if topology == "Star" or topology == "Ring"
            else (
                self.computer_count
                if topology == "Bus"
                else self.computer_count
                * (self.computer_count - 1) // 2
            )
        )

        self.status.set(
            f"Topology: {topology}   |   "
            f"Computers: {self.computer_count}   |   "
            f"Connections: {connection_count}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTopologySimulator(root)
    root.mainloop()