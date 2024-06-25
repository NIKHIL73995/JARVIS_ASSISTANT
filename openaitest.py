import os
import google.generativeai as genai
from config import apikey
# Set your API key from environment variables
genai.configure(api_key=apikey)

# Create the model with generation configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Define the chat history (resignation template)
chat_history = [
    {
      "role": "user",
      "parts": [
        "write a code to the boss for resignation\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Resignation Code:\n\n**Subject: Resignation - [Your Name]**\n\nDear [Boss's Name],\n\nPlease accept this email as formal notification that I am resigning from my position as [Your Position] at [Company Name]. My last day of employment will be [Your Last Day].\n\nI would like to thank you for the opportunity to work at [Company Name] for the past [Number] years/months. I have learned and grown significantly during my time here, and I am grateful for the experiences I have gained.\n\n[Optional: Briefly mention your reason for leaving, e.g., \"I am pursuing a new opportunity that aligns more closely with my career goals.\"]\n\nI am committed to ensuring a smooth transition during my remaining time at [Company Name] and will do everything I can to assist with the handover of my responsibilities.\n\nI wish you and the company all the best in the future.\n\nSincerely,\n\n[Your Name]\n\n**Additional Tips:**\n\n* **Keep it professional and brief.** This is a formal document. \n* **Be polite and positive.**  \n* **Offer to help with the transition.**\n* **Proofread carefully.**\n* **Consider sending a separate, personal thank-you note to your boss.**\n\n**Please remember to customize this template to fit your specific situation and company culture.** \n",
      ],
    },
]

# Start a chat session with the model
chat_session = model.start_chat(history=chat_history)

# Replace "INSERT_INPUT_HERE" with your specific input for the model
response = chat_session.send_message("I am resigning from my position effective immediately due to personal reasons.")

# Print the generated resignation letter
print(response.text)
