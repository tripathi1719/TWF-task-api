# app.py
from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

DISTANCE = {
    ("C1", "L1"): 10,
    ("C2", "L1"): 20,
    ("C3", "L1"): 30,
    ("C1", "C2"): 20,
    ("C1", "C3"): 30,
    ("C2", "C3"): 10,
}
WAREHOUSES = {
    "C1": {"A", "B", "C"},
    "C2": {"D", "E", "F"},
    "C3": {"G", "H", "I"},
}

def get_centers_for_order(order):
    centers_needed = set()
    for product in order:
        for center, items in WAREHOUSES.items():
            if product in items:
                centers_needed.add(center)
    return centers_needed

def calc_cost(path):
    cost = 0
    for i in range(len(path)-1):
        step = (path[i], path[i+1])
        cost += DISTANCE.get(step) or DISTANCE.get((step[1], step[0]))
    return cost

@app.route("/min-cost", methods=["POST"])
def min_cost():
    order = request.json
    required_products = {k for k, v in order.items() if v > 0}
    centers_needed = get_centers_for_order(required_products)

    min_total_cost = float('inf')

    for start_center in centers_needed:
        other_centers = list(centers_needed - {start_center})
        for perm in permutations(other_centers):
            path = [start_center]
            for center in perm:
                path += ["L1", center]
            path += ["L1"]
            cost = calc_cost(path)
            min_total_cost = min(min_total_cost, cost)

    return jsonify({"min_cost": min_total_cost})

if __name__ == "__main__":
    app.run(debug=True)
