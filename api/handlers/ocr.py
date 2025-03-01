from markitdown import MarkItDown
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import requests

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY")) 
md = MarkItDown(llm_client=client, llm_model='gpt-4o-mini')
prompt = '''Write detailed description. Extract text and nothing more.'''


async def read(file):
    try:
        response = md.convert_stream(file)
        if not response.text_content:
            response = md.convert_stream(file, llm_prompt = prompt)
            if not response.text_content:
                raise Exception
        return response.text_content
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
            return response.text_content
        else:
            raise f"Erro na URL "        
    except Exception as e:
        raise f"Erro ao realizar OCR: {e}"    


async def main(path):
    c = await read_url(path)
    print(c)
if __name__ == '__main__':
     asyncio.run(main('https://temp-files-0.sfo3.cdn.digitaloceanspaces.com/b4292e7e-da9a-4fc6-9412-85b95924f869/page_1.pdf'))