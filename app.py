import requests
from flask import Flask, Response
import json

app = Flask(__name__)

DISPATCHER_URL = "http://dispatcher.citrus-dispatcher.svc.cluster.local:8888/metrics"

def normalize_key(key: str) -> str:
    """
    Нормализует ключ: заменяет . , = на _
    Например:
    "websocket.connections.total" → "websocket_connections_total"
    "tasks.completed.by_type,success=True,type=enhance_image" → "tasks_completed_by_type_success_True_type_enhance_image"
    """
    return key.replace(".", "_").replace(",", "_").replace("=", "_")

def format_metrics(data: dict) -> str:
    """
    Преобразует JSON метрики в Prometheus-совместимый текст
    """
    lines = []

    # uptime_seconds (простое число)
    if "uptime_seconds" in data:
        lines.append(f'dispatcher_uptime_seconds {data["uptime_seconds"]}')

    # counters
    if "counters" in data:
        for k, v in data["counters"].items():
            metric = normalize_key(k)
            lines.append(f'dispatcher_counters{{metric="{metric}"}} {v}')

    # gauges
    if "gauges" in data:
        for k, v in data["gauges"].items():
            metric = normalize_key(k)
            lines.append(f'dispatcher_gauges{{metric="{metric}"}} {v}')

    # rates
    if "rates" in data:
        for k, v in data["rates"].items():
            metric = normalize_key(k)
            lines.append(f'dispatcher_rates{{metric="{metric}"}} {v}')

    # histograms
    if "histograms" in data:
        for k, v in data["histograms"].items():
            hist_name = normalize_key(k)
            for stat, value in v.items():
                lines.append(f'dispatcher_histograms{{histogram="{hist_name}",stat="{stat}"}} {value}')

    return "\n".join(lines) + "\n"

@app.route("/metrics_processed")
def metrics():
    try:
        r = requests.get(DISPATCHER_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
        body = format_metrics(data)
        return Response(body, mimetype="text/plain")
    except Exception as e:
        return Response(f"# error: {str(e)}\n", mimetype="text/plain", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181)

