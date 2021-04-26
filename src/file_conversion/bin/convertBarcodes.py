from modules.codebookParsing import convertLettersToNumbers
import sys


if __name__ == "__main__":
    path_to_codebook= sys.argv[0]
    path_to_index   = sys.argv[1]
    
    convertLettersToNumbers(path_to_codebook, path_to_index, outfile="parsed_codebook.csv")
