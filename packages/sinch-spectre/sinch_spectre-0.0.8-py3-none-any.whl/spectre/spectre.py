import argparse
from generation import generator

def main():
    parser = argparse.ArgumentParser(description='Generation of API specifications from your data schema')
    parser.add_argument('path', help='The path to a file containing your data model specified in JSON')
    args = parser.parse_args()
    generator.generate(args.path)

if __name__== "__main__":
    main()