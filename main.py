import os
import csv
import re

phrases = ["zone of discretion","salary advancement",
           "maternity leave", "paternity leave","parental leave","study assistance","professional development",
           "flextime","flextime provisions","travel","overtime","recognition of travel time",
           "travel allowance","salary packaging","bandwidth","health and wellbeing reimbursement",
           "health and wellbeing","health and wellbeing allowance","influenza vaccine","donating blood",
           "study leave","long service leave","flexible work arrangements"]


def main():
    context = 30 # number of lines of context after matches to show.
    tocRegex = re.compile(r'\.{4}') # Terms of Contents lines appear to have 4 or more . characters.
    
    
    with open('output.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        for filename in os.listdir("txt"):
            fn = os.path.join("txt", filename)
            with open(fn) as f:

                lines = []
                for line in f:
                    l = line.lower().strip() # convert to lowercase, strip whitespace/newlines.
                    if l == "":
                        continue
                    lines.append(l)
 
                for i in range(len(lines)):
                    l = lines[i]
                    for p in phrases:
                        if p in l:

                            tocMatch = tocRegex.search(l)

                            # skip toc lines
                            if tocMatch is not None:
                                continue
                            
                            # found a match, print the context lines after the match.
                            contextLines = lines[i:i+context]

                            # try and filter out the terms of contents lines.
                            foundToc = False
                            for cl in contextLines:
                                tocMatch = tocRegex.search(cl)
                                if tocMatch is not None:
                                    foundToc = True
                            if foundToc:
                                continue
                            
                            contextStr = "\n".join(contextLines)
                            csvwriter.writerow([filename,i, p, contextStr])
                            #csvwriter.writerow([filename,p, i, l, "match"])
                            #print(f"file: {filename} phrase: {p} linenum: {i} match:{l}")
                


if __name__ == "__main__":
    main()
