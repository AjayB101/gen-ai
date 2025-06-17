from langchain_huggingface import HuggingFaceEndpoint

def get_hf_endpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
):
    """Initialize and return a reusable HuggingFaceEndpoint LLM."""
    return HuggingFaceEndpoint(
        repo_id=repo_id,
        task="text-generation",
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        repetition_penalty=repetition_penalty,
        huggingfacehub_api_token="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",
    )
