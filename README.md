# AI-Powered Chatbot with Document Knowledge Base

This chatbot application allows users to **upload PDF documents**, process their content, and interact with an AI-powered chatbot that answers questions based on the uploaded documents. The chatbot utilizes **Phi-2**, a small but powerful NLP model, and employs **semantic search** using embeddings and FAISS.

---

## **Features**
- **Upload PDFs** – Users can upload single or multiple PDF documents.  
- **Automatic Text Extraction** – Extracts text from uploaded PDFs.  
- **Vector Store for Semantic Search** – Uses embeddings to store and retrieve relevant document information.  
- **AI-Powered Chatbot** – Answers questions based on the extracted knowledge using **Phi-2**.  
- **FastAPI-based API** – A lightweight backend for seamless chatbot interactions.  
- **Docker Support** – Easily deploy the application in a Docker container.  

---

## **Setup Instructions**

### **Clone the Repository**
`git clone [<your-github-repo-link>](https://github.com/aliai22/ChatBot)`

`cd chatbot`

### **Create a Virtual Environment**

`python -m venv venv`

`source venv/bin/activate`  # On macOS/Linux

`venv\Scripts\activate`      # On Windows

### **Install Dependencies**

`pip install -r requirements.txt
`
### **Run the Application**

`uvicorn app.main:app --reload`

## **API Documentation**

This chatbot application is powered by FastAPI, which provides an interactive API documentation. You can access it at:

`http://127.0.0.1:8000/docs
`

## **Running with Docker**

- Build the Docker Image:

`docker build -t chatbot-app .
`

- Run the Container:

`docker run -p 8000:8000 chatbot-app
`

- Access the Chatbot:

`http://127.0.0.1:8000/
`
