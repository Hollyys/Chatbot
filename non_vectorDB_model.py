from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="valiant-imagery-399603", location="asia-northeast3")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison")
response = model.predict(
    """너는 기존 판례들과 헌법 조항에 대해 사회적 약자들에게 정보를 제공하는 챗봇이야.
물어보는 질문에 대해 자세히 대답해줘
""",
    **parameters
)
print(f"Response from Model: {response.text}")