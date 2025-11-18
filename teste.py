import ollama

response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Você está pronto para ajudar alunos a estudar?',
  },
])

print(response['message']['content'])