from langchain.tools import BaseTool
import torch

from vision_model.image_captions import load_image
from transformers import AutoModel, AutoTokenizer


model = (
    AutoModel.from_pretrained(
        "5CD-AI/Vintern-1B-v2",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    .eval()
    .cuda()
)
tokenizer = AutoTokenizer.from_pretrained(
    "5CD-AI/Vintern-1B-v2", trust_remote_code=True, use_fast=True
)


def extract_text_from_image(image_file):
    pixel_values = load_image(image_file, max_num=12).to(torch.bfloat16).cuda()
    generation_config = dict(
        max_new_tokens=1024,
        do_sample=False,
        num_beams=3,
        repetition_penalty=2.5,
        return_dict=True,
    )
    question = "<image>\nMô tả chi tiết thông tin trong hình ảnh"
    response, history = model.chat(
        tokenizer,
        pixel_values,
        question,
        generation_config,
        history=None,
        return_history=True,
    )
    return response


class Captioning_Image(BaseTool):
    name:str = "image_description"
    description:str = """
        Use this tool when you need to extract or describe information inside an image.
    """
    def _run(self, image_file):
        image_file = image_file.replace("'", "").replace("`", "").strip()
        response = extract_text_from_image(image_file)
        return response

    def _arun(self, image_file):
        raise NotImplementedError("This tool does not support async")
