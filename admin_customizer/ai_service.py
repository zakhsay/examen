import openai
from django.conf import settings

def get_openai_client():
    """Initializes and returns an OpenAI client."""
    openai.api_key = settings.OPENAI_API_KEY
    return openai

def generate_text_with_openai(prompt_text, model="gpt-3.5-turbo", max_tokens=150):
    """
    Generates text using OpenAI's Chat Completions API.
    """
    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example of another potential AI function (e.g., for LangChain)
# from langchain.llms import OpenAI as LangchainOpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# def generate_text_with_langchain(prompt_text):
#     llm = LangchainOpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0.7)
#     prompt = PromptTemplate(
#         input_variables=["topic"],
#         template="Tell me a short story about {topic}.",
#     )
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(topic=prompt_text)