from dotenv import load_dotenv
from graph.graph import app


load_dotenv()




if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(app.invoke(input = {"question":"What is Agent memory"}))