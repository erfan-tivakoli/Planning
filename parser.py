
def parse(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            