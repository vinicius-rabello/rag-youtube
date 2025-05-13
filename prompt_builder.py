from langchain_core.prompts import ChatPromptTemplate

# Gera um prompt a partir de um arquivo, substituindo os placeholders por informações específicas
def build_prompt_from_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        base_template = f.read()
    full_prompt = base_template.format(context="{context}", input="{input}")
    return ChatPromptTemplate.from_template(full_prompt)