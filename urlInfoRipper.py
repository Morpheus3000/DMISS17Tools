
import argparse
import pandas as pd
import urlInfoExtractor


__author__ = "Partha Das"
__version__ = "1.0.1"

def rip(csv, column, output):
    with open(csv, 'r') as f:
        df = pd.read_csv(f)


    urls = df[column]
    title = []
    domain = []
    for idx, url in enumerate(urls):
        print("[%d] Processing url: %s" % (idx, url), end='\r')
        tmp = urlInfoExtractor.getInfo(url)
        if len(tmp[0])> 0 :
            domain.append(tmp[0])
        else:
            domain.append("N/A")
        if len(tmp[1])> 0 and tmp[1] is not None:
            title.append(tmp[1])
        else:
            title.append("N/A")
        print("[%d] Processed url: %s.....Done!" % (idx, url))


    df = df.assign(domain=domain, title=title)
    df.to_csv(output, index=False)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input csv file",
                        required=True)
    parser.add_argument("-c", "--column", help="""Name of the column which has
                        the urls""", required=True)
    parser.add_argument("-o", "--output", help="""Name of the output file that
                        is to be saved. If it the same file as the input csv,
                        then it will just be the original csv with 2 more
                        columns added""", required=True)

    args = parser.parse_args()
    input = args.input
    column = args.column
    output = args.output

    print("Job Parameters: ")
    print("""\n\tInput file: %s\n\tTarget Column: %s\n\tOutput Location: %s\n"""
                                                                   % (input,
                                                                       column,
                                                                       output
                                                                      ))
    print("Job Started....\n\n")

    rip(input, column, output)
    print('Done')
