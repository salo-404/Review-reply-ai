def build_prompt(review: str, business_type: str, tone: str, language: str) -> str:
    return f"""
SYSTEM:
You are a strict JSON generator.
You MUST return valid JSON only.
Do NOT include explanations, markdown, or extra text.
If you cannot comply, return an empty JSON object {{}}.

TASK:
Analyze the customer review for a {business_type} and return a JSON object
that follows EXACTLY this schema:

{{
  "sentiment": "positive | neutral | negative",
  "issue_type": "delivery | service | quality | price | app_or_website | other",
  "key_points": ["string", "string"],
  "replies": {{
    "best": "string",
    "short": "string",
    "alternative": "string"
  }},
  "internal_fix_suggestions": ["string", "string"]
}}

RULES:
- Tone for replies: {tone}
- Language for replies: {language}
- Replies must be respectful and professional.
- Do NOT ask questions in the reply.
- Do NOT mention AI.
- If negative: apologize + address issue + next step.
- If positive: thank the customer.
- Keep replies under 6 sentences.

CUSTOMER REVIEW:
\"\"\"{review}\"\"\"

OUTPUT:
Return ONLY the JSON object.
"""
