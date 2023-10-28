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

    output_rows = []
    
    with open('output.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        for filename in os.listdir("txt"):
            fn = os.path.join("txt", filename)
            with open(fn) as f:

                lines = []
                for line in f:
                    l = line.lower().strip() # convert to lowercase, strip whitespace/newlines.
                    lines.append(l)
 
                for i in range(len(lines)):
                    l = lines[i]
                    for p in phrases:
                        if p in l:
                            print(f"file: {filename}, num:{i}, line:{l}")
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
                            lineNumberLink = f'<a href="https://github.com/kzrl/enterprise-agreements/blob/master/txt/{filename}#L{i+1}">{i+1}</a>'
                            #csvwriter.writerow([filename,lineNumberLink, p, contextStr])
                            csv_row = [filename,i, p, contextStr]
                            html_row = [filename,lineNumberLink, p, contextStr]
                            output_rows.append(html_row)
                            csvwriter.writerow(csv_row)
                            #csvwriter.writerow([filename,p, i, l, "match"])
                            #print(f"file: {filename} phrase: {p} linenum: {i} match:{l}")

                write_html(output_rows)

def highlight_match(s, keyword):
    return s.replace(keyword, f"<b>{keyword}</b>")
                
def write_html(rows):

    css = """
<style>table, th, td { border: 1px solid black;}
    td { padding: 0.5em; }
    table { border-collapse: collapse; }
    .filename {font-size: 0.8em;}
    .match { white-space: pre;
    font-family: monospace; }
</style>
"""
    
    with open("index.html", "w") as f:
        f.write(f"<!DOCTYPE html><html><head><title>Output</title>{css}</head><body><table><thead><tr>")
        f.write("<td>Filename</td><td>Line</td><td>Keyword</td><td>Match</td></tr><tbody>")
        for row in rows:
            f.write(f"<tr><td><span class=\"filename\">{row[0]}</span></td><td>{row[1]}</td><td>{row[2]}</td><td class=\"match\">{highlight_match(row[3], row[2])}</td></tr>")
        f.write("</tbody></table></body></html>")

if __name__ == "__main__":
    main()
