import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True, type=str, help="README를 작성할 프로젝트 경로")

args = parser.parse_args()