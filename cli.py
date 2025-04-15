import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True, type=str, help="README를 작성할 프로젝트 경로")
parser.add_argument("--model", required=True, type=str, default="local", help="사용할 모델 (ex, openai, local)")
parser.add_argument("--openai_model", type=str, default="gpt-4o-mini-2024-07-18", help="openai model")

args = parser.parse_args()