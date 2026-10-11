# Fraud Detection

A small fraud-detection application with a FastAPI prediction API, Kafka transaction
processing, Prometheus metrics, and Grafana dashboards.

## Run with Docker

From the project directory:

```powershell
docker compose up --build
```

Services:

- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana is provisioned automatically with Prometheus at:

```text
http://prometheus:9090
```

## API

Send a transaction to the prediction endpoint:

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{ "amount": 100, "transaction_time": 12.5, "user_age": 35, "is_international": 0 }'
```

## Metrics

Useful Prometheus queries include:

```promql
fraud_predictions_total
fraud_prediction_latency_seconds
fraud_prediction_memory_peak_bytes / 1024 / 1024
```

The API metrics are available at `/metrics`, and consumer metrics are exposed on
port `8001` inside the Docker network.