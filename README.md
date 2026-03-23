# 🤖 AI Operations Assistant (CodeWar 2.0)

An agent-based AI system that transforms natural language requests into actionable workflows using a **multi-agent architecture**.

Unlike traditional chatbots, this system plans, executes, and verifies tasks using real-world APIs.

---

## 🚀 Problem Statement

Build an **AI Operations Assistant** that:

1. Understands a user request
2. Breaks it into structured steps
3. Executes real API calls
4. Verifies correctness before responding

❗ Constraint:  
A **single prompt solution is NOT allowed**. The system must use a **3-agent architecture**.

---

## 🧠 Architecture Overview

The system is divided into three independent agents:

### 1. Planner Agent (Brain)
- Converts user input into a **strict JSON plan**
- Decides:
  - Which tools to use
  - Order of execution
- Ensures structured output

---

### 2. Executor Agent (Hands)
- Reads the JSON plan
- Executes API calls step-by-step
- Handles:
  - API failures
  - Retry logic
  - Data collection

---

### 3. Verifier Agent (QA)
- Validates collected data
- Ensures:
  - Completeness
  - Correct schema
- Formats final output for the user

---
