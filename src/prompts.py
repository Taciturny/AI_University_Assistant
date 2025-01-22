from typing import Dict
import json

class PromptManager:
    def __init__(self, base_prompt_path: str = "./docs/prompts/base_prompts.json",
                 refined_prompt_path: str = "./docs/prompts/refined_prompts.json"):
        self.base_prompts = self._load_prompts(base_prompt_path)
        self.refined_prompts = self._load_prompts(refined_prompt_path)
        self.current_prompts = self.refined_prompts  # Default to refined prompts

    def _load_prompts(self, path: str) -> Dict:
        with open(path, 'r') as f:
            return json.load(f)

    def get_prompt(self, prompt_type: str, sub_type: str,
                   use_refined: bool = True, **kwargs) -> str:
        """Get formatted prompt based on type and parameters"""
        prompts = self.refined_prompts if use_refined else self.base_prompts

        if prompt_type not in prompts or sub_type not in prompts[prompt_type]:
            raise ValueError(f"Invalid prompt type: {prompt_type}.{sub_type}")

        prompt_template = prompts[prompt_type][sub_type]
        if isinstance(prompt_template, dict):
            return prompt_template
        return prompt_template.format(**kwargs)

    def switch_prompt_version(self, use_refined: bool = True) -> None:
        """Switch between base and refined prompts"""
        self.current_prompts = self.refined_prompts if use_refined else self.base_prompts
