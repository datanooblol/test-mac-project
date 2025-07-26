class PromptTemplate:
    def __init__(self, template, variables=None):
        self.template = template
        self.variables = variables or {}
    
    def format(self, **kwargs):
        return self.template.format(**{**self.variables, **kwargs})

# Usage
code_review_prompt = PromptTemplate(
    "Review this {language} code for {focus}:\n\n{code}\n\nProvide feedback on:",
    {"focus": "bugs and performance"}
)

# Use with any LLM
prompt = code_review_prompt.format(language="Python", code="def hello(): print('hi')")