import requests

url = 'http://localhost:5000/get_questions/'  # url of api
data = {'questions_num': 1}  # number of requests

response = requests.post(url, json=data)

if response.status_code == 200:
    questions = response.json()
    print(questions)
    for question in questions:
        print(f"Question ID: {question['id']}")
        print(f"Question Text: {question['question_text']}")
        print(f"Answer Text: {question['answer_text']}")
        print(f"Created Date: {question['created_date']}")
else:
    print(f"Failed to retrieve questions. Status code: {response.status_code}")

