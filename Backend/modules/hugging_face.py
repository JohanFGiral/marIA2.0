import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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",
)

h_messages=[
        {
			"role": "system",
			"content":"Eres una asistente formal llamada Mar-IA, saluda de manera formal al usuario, refierete a el como jefe, solo cuando sea necesario"
		}
    ]

max_history_length = 10

def trim_history():
    global h_messages
    system_msg = h_messages[0]
    other_msgs = h_messages[1:]
    if len(other_msgs) > max_history_length * 1:
        h_messages = [system_msg] + other_msgs[-max_history_length*1:]
        print("mesagges deleted")



def send_messages(text):
    h_messages.append({"role":"user", "content": text})
    trim_history()
    completion = client.chat.completions.create(
		model="moonshotai/Kimi-K2-Instruct-0905",
		messages=h_messages,
	)
    
    response = completion.choices[0].message.content
    
    h_messages.append({"role": "assistant", "content": response})
    
    return response