import yaml
from typing import Dict, Any

class PromptManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_prompt(self, name: str, **kwargs) -> Dict[str, str]:
        prompt_config = self.config['prompts'][name]
        template = prompt_config['template']
        variables = {**prompt_config.get('variables', {}), **kwargs}
        
        return {
            'system': prompt_config.get('system', ''),
            'user': template.format(**variables)
        }

# Usage with any LLM
pm = PromptManager('prompts.yaml')
prompt = pm.get_prompt('code_review', language='Python', code='def test(): pass')