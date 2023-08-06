import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str, required=True,  help="Private gitlab API token")
    parser.add_argument("-s", "--server", type=str, required=True,  help="Server URL")
    parser.add_argument("-o", "--output", type=str, help="Output file to write csv")
    return parser.parse_args()
