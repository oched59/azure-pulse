import openai

OPENAI_API_KEY = "a4afc38d3a6246d3b855a8adcca0d0f1"
prompt = "Tell me something funny"
openai.api_type = "azure"
openai.api_base = "https://cog-oaxatpknic6wq.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = OPENAI_API_KEY

model_name = "gpt-35-turbo"
deployment_name ="chat"


output = openai.Completion.create(
    model = model_name,
    prompt = prompt ,
    max_tokens = 200,
    temperature = 0

)
print(output)