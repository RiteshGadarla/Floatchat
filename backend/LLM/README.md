# Gemma & Gemini Model Overview

This document provides a summary of various Gemma and Gemini language models, their sizes, capabilities, and recommended use cases.

**Rate Limits:** [Documentation](https://ai.google.dev/gemini-api/docs/rate-limits)


---

## Gemma Models

### 1. Gemma 3n E2B
- **Identifier:** `gemma-3n-e2b-it`
- **Size:** Small
- **Description:** Lightweight open model; efficient on low-resource devices; basic reasoning capabilities.
- **Use Case:** Suitable for low-resource environments or simple reasoning tasks.

### 2. Gemma 3n E4B
- **Identifier:** `gemma-3n-e4b-it`
- **Size:** Slightly larger than E2B
- **Description:** Still lightweight; slightly better reasoning than E2B.
- **Use Case:** Slightly more demanding reasoning tasks while maintaining efficiency.

### 3. Gemma 3 1B
- **Identifier:** `gemma-3-1b-it`
- **Size:** Smallest full Gemma 3 model
- **Description:** Good for text-only tasks; low latency.
- **Use Case:** Text processing where speed is crucial.

### 4. Gemma 3 4B
- **Identifier:** `gemma-3-4b-it`
- **Size:** Medium
- **Description:** Handles larger text inputs; improved reasoning and context retention.
- **Use Case:** Tasks requiring more context and reasoning.

### 5. Gemma 3 12B
- **Identifier:** `gemma-3-12b-it`
- **Size:** Large
- **Description:** Can handle complex tasks, including multimodal inputs; strong reasoning.
- **Use Case:** Complex text and multimodal tasks requiring advanced reasoning.

### 6. Gemma 3 27B
- **Identifier:** `gemma-3-27b-it`
- **Size:** Largest Gemma 3 model
- **Description:** Top-tier open model; excels at complex reasoning and multimodal tasks.
- **Use Case:** High-end tasks with heavy reasoning and multimodal needs.

---

## Gemini Models

### 1. Gemini 1.5 Flash
- **Identifier:** `gemini-1.5-flash`
- **Description:** Deprecated; older Google model; basic reasoning and chat capabilities.
- **Use Case:** Legacy tasks with basic chat functionality.

### 2. Gemini 2.0 Flash-Lite
- **Identifier:** `gemini-2.0-flash-lite`
- **Size:** Small
- **Description:** Cost-efficient; moderate reasoning.
- **Use Case:** Budget-friendly tasks needing moderate reasoning.

### 3. Gemini 2.0 Flash
- **Identifier:** `gemini-2.0-flash`
- **Description:** Full 2.0 model; stronger reasoning and context handling; balanced general-purpose chat.
- **Use Case:** General-purpose chat and reasoning tasks.

### 4. Gemini 2.5 Flash-Lite
- **Identifier:** `gemini-2.5-flash-lite`
- **Size:** Small
- **Description:** Stronger reasoning than 2.0; suitable for scaled usage.
- **Use Case:** Scaled applications needing more advanced reasoning.

### 5. Gemini 2.5 Flash
- **Identifier:** `gemini-2.5-flash`
- **Description:** Full 2.5 model; very strong reasoning and thinking budgets; good for coding and complex tasks.
- **Use Case:** Coding, problem-solving, and complex reasoning tasks.

### 6. Gemini 2.5 Pro
- **Identifier:** `gemini-2.5-pro`
- **Description:** Top-tier Google model; excels at coding, complex reasoning, and large-scale tasks; smartest model available.
- **Use Case:** Highest-demand tasks including coding, research, and large-scale multistep reasoning.

---

**Note:**  
- `n` in Gemma models typically refers to “nano” or small variants.  
- `B` denotes billions of parameters (e.g., 1B = 1 billion parameters).  
- Gemini models are Google's proprietary models, optimized for chat, reasoning, and coding.  

