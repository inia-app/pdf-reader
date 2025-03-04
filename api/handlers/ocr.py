from markitdown import MarkItDown
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import requests
from markdown import markdown
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY")) 
md = MarkItDown(llm_client=client, llm_model='gpt-4o-mini')
prompt = '''Write detailed description. Extract text and nothing more. write in portuguese'''


async def read(file):
    try:
        response = md.convert_stream(file)
        if not response.text_content:
            response = md.convert_stream(file, llm_prompt = prompt, prompt= prompt)
            if not response.text_content:
                raise Exception
        mk = markdown(response.text_content)
        return mk
    except Exception as e:
        return f"Erro ao realizar OCR: {e}"

async def read_url(url):
    try:
        test_response = requests.get(url)
        if test_response.ok:
            response = md.convert_url(url)
            if not response.text_content:
                response = md.convert_url(url, llm_prompt = prompt)
                if not response.text_content:
                    raise "OCR FAILED"
            return markdown(response.text_content)
        else:
            raise f"Erro na URL "        
    except Exception as e:
        raise f"Erro ao realizar OCR: {e}"    


async def main(path):
    with open (path, 'rb') as f: 
        c = await read(f)
    print(c)
if __name__ == '__main__':
     asyncio.run(main('files/153.pdf'))