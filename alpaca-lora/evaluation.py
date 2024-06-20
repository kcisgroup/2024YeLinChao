import os
import sys

import fire
import torch
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

from utils.prompter import Prompter

device = "cpu"

def main(
    load_8bit: bool = True,
    base_model: str = "./chinese-alpaca-plus-7b-hf",
    lora_weights: str = "lora-alpaca-TCM",
    prompt_template: str = "template",  # The prompt template to use, will default to alpaca.
):
    base_model = base_model or os.environ.get("BASE_MODEL", "")
    prompter = Prompter(prompt_template)
    tokenizer = LlamaTokenizer.from_pretrained(base_model)
    model = LlamaForCausalLM.from_pretrained(
        base_model, device_map={"": device}, low_cpu_mem_usage=True
    )
    model = PeftModel.from_pretrained(
        model,
        lora_weights,
        device_map={"": device},
    )
    # unwind broken decapoda-research config
    # model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    # model.config.bos_token_id = 1
    # model.config.eos_token_id = 2

    if not load_8bit:
        model.half()  # seems to fix bugs for some users.
    model.eval()


    # testing code for readme
    for input_word in [
        # "[MASK]属水，咸入[MASK]，[MASK]属火而主[MASK]，咸主[MASK]即以水胜火之意",
        # "[MASK]，即指药物具有寒、热、温、凉四种不同的药性",
        '人体是以[MASK]为中心的',
        "描述肾的概念",
        '描述胰的概念',
        '描述肾和胰的关系',
        '描述脾和胰的关系'
    ]:
        print("Instruction:", input_word)
        prompt = prompter.generate_prompt(instruction=input_word, input=None)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        generation_config = GenerationConfig(
            temperature=0.04,
            top_p=0.2,
            top_k=10,
            num_beams=4,
        )

        # Without streaming
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=128,
            )
        s = generation_output.sequences[0]

        print(tokenizer.decode(s))

        print()



if __name__ == "__main__":
    fire.Fire(main)
