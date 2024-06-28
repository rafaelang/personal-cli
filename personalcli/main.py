#!python3
import sys

import typer
from pydantic_settings import SettingsConfigDict, BaseSettings
import google.generativeai as genai
from loguru import logger as l
import getpass

l.remove()
l.add(sys.stderr, level="WARNING")


class Settings(BaseSettings):
    GEMINI_VERSION: str = "gemini-1.0-pro-latest"
    GOOGLE_API_KEY: str
    model_config = SettingsConfigDict(env_prefix="PERSONALCLI_")


app = typer.Typer()

def query_gemini(instruction, message):
    settings = Settings()

    query = instruction.format(message=message)
    model = genai.GenerativeModel(settings.GEMINI_VERSION)
    response = model.generate_content(query)
    l.debug(f'Querying Gemini: "{message}" -> "{response.text}"')
    return response.text


@app.command()
def main(question: str, interactive: bool = False) -> str:
    settings = Settings()
    genai.configure(api_key=settings.GOOGLE_API_KEY)

    while True:
        l.debug(question)
        username = getpass.getuser()
        l.debug(f"Logged in user: {username}")
        typer.echo(typer.style(f"\n{username}:", bold=True, fg=typer.colors.BRIGHT_CYAN) + typer.style(f" {question}\n", fg=typer.colors.BRIGHT_CYAN))
        response = query_gemini("{message}", question)
        typer.echo(typer.style("Gemini:", bold=True, fg=typer.colors.BRIGHT_GREEN) + typer.style(f" {response}\n", fg=typer.colors.BRIGHT_GREEN))
        
        if not interactive:
            break

        typer.echo(typer.style(f"\n Algo mais {username}?  (CTRL + C para encerrar)\n", bold=True, fg=typer.colors.BRIGHT_GREEN))
        question = typer.prompt(typer.style(f"\n{username}  ", bold=True, fg=typer.colors.BRIGHT_CYAN))


