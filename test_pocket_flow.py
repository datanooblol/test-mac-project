from package.bedrock import BedrockChat
from pocketflow import Node, Flow
import yaml
class InputNode(Node):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def prep(self, shared):
        user_input = input("\033[43;37mYou: \033[0m")
        if user_input.lower() == "exit":
            return None
        
        if "messages" not in shared:
            shared['messages'] = []
        
        return user_input

    def exec(self, prep_res):
        return prep_res
    
    def post(self, shared, prep_res, exec_res):
        shared['messages'].append(self.model.UserMessage(text=prep_res))
        if prep_res:
            return "router"

class RouterNode(Node):
    def __init__(self, system_prompt, model):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def prep(self, shared):
        user_message = shared['messages'][-1]['content'][0]['text']
        return user_message
    
    def exec(self, user_message):
        response = self.model(system_prompt=self.system_prompt, messages=[self.model.UserMessage(text=user_message)])
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        action = yaml.safe_load(yaml_str)
        return action['action']

    def post(self, shared, prep_res, exec_res):
        shared['action'] = exec_res
        return exec_res

class AnswerNode(Node):
    def __init__(self, system_prompt, model):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def prep(self, shared):
        return shared['messages']
    
    def exec(self, messages):
        response = self.model(self.system_prompt, messages)
        print(f"\033[42;37mAI: \033[0m{response}")
        return response
    
    def post(self, shared, prep_res, exec_res):
        shared["messages"].append(self.model.AIMessage(text=exec_res))
        return "continue"
 
router_prompt = """\
classify a user's intent based on the input messages. 
Intent options are:
1. continue if nothing goes wrong
2. farewell if a user's message indicate that he or she wants to go somewhere

Return your response in codeblock with this following yaml format:
```yaml
action: either continue or farewell
```

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
"""

answer_prompt = "You are a helpful assistant"

model = BedrockChat()
input_node = InputNode(model=model)
router_node = RouterNode(router_prompt, model)
answer_node = AnswerNode(answer_prompt, model)

input_node - "router" >> router_node
router_node - "answer" >> answer_node
router_node - "continue" >> answer_node
answer_node - "continue" >> input_node

flow = Flow(start=input_node)

if __name__=='__main__':
    shared={}
    flow.run(shared)