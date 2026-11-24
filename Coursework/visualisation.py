from collections import deque
import math
import tempfile
import webbrowser
from pathlib import Path

from intersection import Intersection


class NetworkVisualiser:
    def _layout_nodes(self, nodes: list[Intersection], size: int) -> dict[int, tuple[float, float]]:
        adjacency = {node.id: [] for node in nodes}
        for node in nodes:
            for route in node.routes:
                angle = math.radians(route.direction)
                dx = route.length * math.sin(angle)
                dy = -route.length * math.cos(angle)
                dx = 0 if math.isclose(dx, 0, abs_tol=1e-12) else dx
                dy = 0 if math.isclose(dy, 0, abs_tol=1e-12) else dy
                adjacency[route.origin_id].append((route.destination_id, dx, dy))
                adjacency[route.destination_id].append((route.origin_id, -dx, -dy))

        world_positions = {}
        positions = {}
        component_offset = 0
        for node in nodes:
            if node.id in world_positions:
                continue
            world_positions[node.id] = (0, 0)
            component = []
            pending = deque([node.id])
            while pending:
                node_id = pending.popleft()
                component.append(node_id)
                x, y = world_positions[node_id]
                for neighbor_id, dx, dy in adjacency[node_id]:
                    if neighbor_id not in world_positions:
                        world_positions[neighbor_id] = (x + dx, y + dy)
                        pending.append(neighbor_id)

            min_x = min(world_positions[node_id][0] for node_id in component)
            max_x = max(world_positions[node_id][0] for node_id in component)
            min_y = min(world_positions[node_id][1] for node_id in component)
            max_y = max(world_positions[node_id][1] for node_id in component)
            positions.update({
                node_id: (component_offset + world_positions[node_id][0] - min_x,
                          world_positions[node_id][1] - min_y)
                for node_id in component
            })
            component_offset += max_x - min_x + 40

        if not positions:
            return positions

        min_x = min(x for x, _ in positions.values())
        max_x = max(x for x, _ in positions.values())
        min_y = min(y for _, y in positions.values())
        max_y = max(y for _, y in positions.values())
        span = max(max_x - min_x, max_y - min_y, 1)
        scale = (size - 100) / span
        offset_x = (size - (max_x - min_x) * scale) / 2 - min_x * scale
        offset_y = (size - (max_y - min_y) * scale) / 2 - min_y * scale
        return {
            node_id: (x * scale + offset_x, y * scale + offset_y)
            for node_id, (x, y) in positions.items()
        }

    def visualise(self, nodes: list[Intersection]) -> None:
        size = 600
        positions = self._layout_nodes(nodes, size)

        def render_route(route):
            x1, y1 = positions[route.origin_id]
            x2, y2 = positions[route.destination_id]
            dx, dy = x2 - x1, y2 - y1
            distance = math.hypot(dx, dy)
            if distance == 0:
                return (
                    '<g>'
                    f'<path d="M{x1 + 14} {y1 - 14} C{x1 + 72} {y1 - 58}, '
                    f'{x1 + 72} {y1 + 58}, {x1 + 14} {y1 + 14}" '
                    'fill="none" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>'
                    f'<text x="{x1 + 72}" y="{y1 + 5}" text-anchor="middle" '
                    f'font-family="sans-serif">{route.id}</text></g>'
                )
            ux, uy = dx / distance, dy / distance
            left_x, left_y = uy, -ux
            offset = 8
            inset = min(22, distance / 3)
            label_x = (x1 + x2) / 2 + left_x * (offset + 12)
            label_y = (y1 + y2) / 2 + left_y * (offset + 12)
            return (
                '<g>'
                f'<line x1="{x1 + ux * inset + left_x * offset}" '
                f'y1="{y1 + uy * inset + left_y * offset}" '
                f'x2="{x2 - ux * inset + left_x * offset}" '
                f'y2="{y2 - uy * inset + left_y * offset}" '
                'stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>'
                f'<text x="{label_x}" y="{label_y}" text-anchor="middle" '
                f'font-family="sans-serif">{route.id}</text></g>'
            )

        routes = "\n".join(
            render_route(route)
            for node in nodes
            for route in node.routes
        )
        intersections = "\n".join(
            f'<circle cx="{x}" cy="{y}" r="20" fill="#38bdf8" stroke="#0f172a"/>'
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="sans-serif">{node.id}</text>'
            for node in nodes
            for x, y in [positions[node.id]]
        )
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}"><defs>'
            '<marker id="arrow" markerWidth="8" markerHeight="8" refX="8" refY="4" '
            'orient="auto" markerUnits="userSpaceOnUse">'
            '<path d="M0 0 L8 4 L0 8 Z" fill="#64748b"/></marker>'
            f'</defs>{routes}{intersections}</svg>'
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", encoding="utf-8", delete=False) as file:
            file.write(svg)
        if not webbrowser.open_new_tab(Path(file.name).as_uri()):
            raise RuntimeError(f"Could not open network visualisation: {file.name}")
