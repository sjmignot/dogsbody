from os import listdir, system, remove
from os.path import dirname, realpath, isfile, join
from pathlib import Path

mypath = dirname(realpath(__file__))

files = [
    f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-5:] == 'ipynb'
]

for f in files:
    with open(f'../{Path(f).parent}/{Path(f).stem}.md', 'w+') as nf:
        nf.write(
            f'title: "Using sklearn Pipelines and Voting Classifier\n'
            f'details: "Using sklearn Pipelines and Voting Classifiers for Kaggle\'s Titanic Challenge"\n'
            f'date: 2020-02-25\n'
            f'lastmod: 2020-02-25\n\n')
        system(
            f'jupyter nbconvert --to html {join(mypath,f)} --template=basic.tpl --output tmp.html'
        )
        with open(f'{join(mypath, "tmp.html")}') as f2:
            nf.write(f2.read())

        remove('tmp.html')
