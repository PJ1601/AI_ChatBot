**AI Chatbot with OpenAI API**

![Chatbot](chatbot_image.png)

**Overview**

The AI Chatbot is a project developed in Python and Django, designed to provide dynamic and contextually relevant responses to user queries. Leveraging the power of OpenAI API, this chatbot offers solutions and assistance to users, addressing their questions and problems.

**Features**

- Utilizes Python and Django framework for robust development.
- Integrates SQLite3 database for efficient data storage.
- Employs OpenAI API with two models:
  - text-davinci-003 for text completion
  - gpt-4 for conversational engagement
- Implements async views in Django for enhanced performance.
- Utilizes JsonResponse to return responses as JSON data.

**Installation**

1. Clone the repository: `git clone https://github.com/PJ1601/AI_ChatBot.git`
2. Install required packages: `pip install -r requirements.txt`
3. Set up OpenAI API credentials in `./chatbot/.env`.
4. Run `python manage.py migrate` to create the chat_bot models.
5. Run the Django development server: `python manage.py runserver`

**Usage**

1. Access the chatbot interface at `http://localhost:8000/chatbot`.
2. Input your query in the provided text box and click 'Submit'.
3. The chatbot will analyze the query and provide a context-specific response.

**Contributing**

Contributions are welcome! Please create a pull request for any improvements or bug fixes.

**License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Disclaimer**

This chatbot is powered by OpenAI API, and its responses are based on the capabilities and limitations of the models used. While it strives to offer helpful and accurate information, it may not always provide definitive answers. Use the chatbot responsibly and verify critical information when needed.

![OpenAI Logo](openai_logo.png)

_This project is not officially affiliated with or endorsed by OpenAI._
