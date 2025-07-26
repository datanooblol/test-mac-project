from pocketflow import Node
from prompt_manager import PromptManager

class PromptNode(Node):
    def __init__(self, prompt_name: str, prompt_manager: PromptManager):
        super().__init__()
        self.prompt_name = prompt_name
        self.pm = prompt_manager
    
    def exec(self, shared):
        prompt_data = self.pm.get_prompt(self.prompt_name, **shared.get('variables', {}))
        model = shared['model']
        
        return model(prompt_data['system'], [model.UserMessage(text=prompt_data['user'])])

# Usage
pm = PromptManager('prompts.yaml')
review_node = PromptNode('code_review', pm)