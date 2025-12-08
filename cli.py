import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True, type=str, help="README를 작성할 프로젝트 경로")
parser.add_argument("--temperature", type=float, default=0.1, help="Model Temperature")
parser.add_argument("--top_p", type=float, default=0.1, help="Model Top-P")
parser.add_argument("--max_tokens", type=int, default=8192, help="Model Max Tokens")

args = parser.parse_args()