### Crawler from /r/politics and its representation through graph
# data_collection

This code requires Python 3.7 or later, then you need to install the dependencies in order to run the script:
```
cd data_collection
pip install -r requirements.txt
```
## crawler.py
It crawls submission and related comments from /r/politics for a given time interval.

usage: python `crawler.py` [-h] [--output-dir OUTPUT_DIR] startingDate endingDate:  
- `startingDate`: timestamp from which start crawling
- `endingDate`: timestamp beyond which the crawler stops
- `--output-dir`: the path in which to save the output files, by default the output directory is `./data/chunks/`
- `--max-iter`: maximum number of iteration of the crawler, by default (0) there is no limit on the number of  iterations, each iterations is composed by 100 submissions.
- `--users-file`: file containing previous users in order to improve the speed avodining retrieve the same information, default value is `./data/users.json`
## cdata.py
It creates a cleaned version of the crawled data.

usage: python `cdata.py` [-h] [--outputFile OUTPUTFILE] [--dataDirectory DATADIRECTORY]
- `--outputFile`:  output file that will contains all the submissions, default is ./data/data.json
- `--dataDirectory`: directory containing all the chunks crawled, default is ./data/chunks/

## busers.py
It creates the users file from the cleaned data.

usage: `busers.py` [-h] [--outputFile OUTPUTFILE] [--dataFile DATAFILE]
- `--outputFile`: output file that will contains all the users, default is ./data/users.json
- `--dataFile`: file that contains all the submissions, default is ./data/data.json

## bgraph.py
It builds the network given the crawled data, the geographical informations and the labels (toxicity and political leaning).

usage: `bgraph.py` [-h] [--usersFile USERSFILE] [--dataFile DATAFILE]
                 [--outputFile OUTPUTFILE]
- `--usersFile `: file containing all the users crawled
- `--dataFile`: file containing all the data crawled
- `--outputFile`: output file in gexf format, default is ./data/BG.gexf
- `--geoFile`: file containing geo information, default is ./model/geo.json
- `--labelsFile`: file containing labels information, default is ./data/labels.json
