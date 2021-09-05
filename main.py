from analyzer import Analyzer


def read_file(file_path):
    file = open(file_path, "r")
    return file.readlines()


if __name__ == '__main__':
    path_file = "example/duplicate_expression.c"
    file_content = read_file(path_file)
    anl = Analyzer(file_content)
    anl.analyze()
    anl.fix()
