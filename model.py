import os
from configs import MODEL_PATH, OPENAI_API
from cli import args


if args.model == "local":
    from llama_index.llms.huggingface import HuggingFaceLLM
    os.environ["CUDA_VISIBLE_DEVICES"]="0,1"
    llm = HuggingFaceLLM(
        model_name=MODEL_PATH,
        tokenizer_name=MODEL_PATH,
        max_new_tokens=8192,
        generate_kwargs={"temperature": 0.8, "top_k": 100, "top_p": 0.95},
        device_map="auto",
    )
elif args.model == "openai":
    from llama_index.llms.openai import OpenAI
    os.environ["OPENAI_API_KEY"] = OPENAI_API
    llm = OpenAI(model=args.openai_model)
else:
    raise ValueError("Unknown model type: choose 'local' or 'openai'")
