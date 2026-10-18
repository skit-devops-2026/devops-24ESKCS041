const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const promClient = require("prom-client");

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URL = process.env.MONGO_URL || "mongodb://localhost:27017/todos";

// Default process metrics
promClient.collectDefaultMetrics();

// Counter: only goes up
const todosCreatedTotal = new promClient.Counter({
  name: "todos_created_total",
  help: "Total number of to-dos ever created",
});

// Gauge: current count, can go up or down
const todosCount = new promClient.Gauge({
  name: "todos_count",
  help: "Current number of to-dos in the list",
});

// Histogram: bucketed request duration
const httpRequestDuration = new promClient.Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "route", "status_code"],
  buckets: [0.01, 0.05, 0.1, 0.3, 0.5, 1, 2],
});

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Timing middleware
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on("finish", () => {
    end({ method: req.method, route: req.path, status_code: res.statusCode });
  });
  next();
});

mongoose
  .connect(MONGO_URL)
  .then(() => console.log("Connected to MongoDB at", MONGO_URL))
  .catch((err) => console.error("MongoDB connection error:", err.message));

const todoSchema = new mongoose.Schema({
  text: { type: String, required: true },
  done: { type: Boolean, default: false },
});

const Todo = mongoose.model("Todo", todoSchema);

app.get("/todos", async (req, res) => {
  try {
    const todos = await Todo.find().sort({ _id: -1 });
    res.json(todos);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/todos", async (req, res) => {
  try {
    const todo = await Todo.create({ text: req.body.text });
    todosCreatedTotal.inc(); // +1, never decreases
    todosCount.set(await Todo.countDocuments());
    res.json(todo);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete("/todos/:id", async (req, res) => {
  try {
    await Todo.findByIdAndDelete(req.params.id);
    todosCount.set(await Todo.countDocuments()); // snapshot, can go down
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Metrics endpoint for Prometheus
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

app.listen(PORT, () => console.log(`To-do app listening on port ${PORT}`));
