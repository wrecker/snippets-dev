import os
import pathlib
import sys
import re
import validators

from collections import defaultdict

root = pathlib.Path(__file__).parent.resolve()
repo = os.getenv("GITHUB_REPOSITORY", "wrecker/til")

bookmark_re = re.compile("^.*?\[(.*)\]\((.*)\).*$")
index_re = re.compile(r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
count_re = re.compile(r"<!\-\- count starts \-\->.*<!\-\- count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"


def build_database(repo_path):
    snippets = defaultdict(list)
    for filepath in root.glob("*/*.md"):
        fp = filepath.open()
        path = str(filepath.relative_to(root))
        topic = path.split("/")[0].replace("_", " ")
        if filepath.name.endswith("url.md"):
            line = fp.readline()
            match = bookmark_re.match(line)
            if match:
                title = match.group(1)
                url = match.group(2)
                record_type = "bookmark"
                if isinstance(validators.url(url), validators.ValidationFailure):
                  continue
            else:
                continue
        else:
            title = fp.readline().lstrip("#").strip()
            url = "https://github.com/{}/blob/master/{}".format(repo, path)
            record_type = "memo"
        snippets[topic].append((title, url, record_type))
    return snippets

def update_readme(snippets):
    index = ["<!-- index starts -->"]
    topics = sorted(snippets.keys())
    count = 0
    for topic in topics:
        rows = snippets[topic]
        index.append("## {}\n".format(topic))
        for row in rows:
            index.append("* :{}: [{}]({})".format(row[2], row[0], row[1]))
            count += 1
        index.append("")
    if index[-1] == "":
        index.pop()
    index.append("<!-- index ends -->")
    if "--rewrite" in sys.argv:
        readme = root / "README.md"
        index_txt = "\n".join(index).strip()
        readme_contents = readme.open().read()
        rewritten = index_re.sub(index_txt, readme_contents)
        rewritten = count_re.sub(COUNT_TEMPLATE.format(count), rewritten)
        readme.open("w").write(rewritten)
    else:
        print("\n".join(index))

if __name__ == '__main__':
    update_readme(build_database(root))
