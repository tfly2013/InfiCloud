"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""
import couchdb
import csv
from argparse import ArgumentParser

POSITIVE_SENT = 1
NEGATIVE_SENT = -1
NEUTRAL_SENT = 0


def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Analysis using sentiment and sla with AURIN data."
    )
    parser.add_argument(
        '--topic',
        default=1,
        help='Topic that this search is about.'
    )
    parser.add_argument(
        '--db',
        type=str,
        help='Database name for search.'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path.'
    )
    parser.add_argument(
        '--aurin',
        type=str,
        help='Aurin data.'
    )
    return parser.parse_args()


def search_data(args):
    """
    Aggregate all income and sentiment/happiness measure
    """
    # handling arguments
    topic = args.topic
    dbname = args.db
    aurin_data = args.aurin
    output_path = args.output

    topic = "topic" + str(topic)

    # connect to couchDB
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[dbname]

    # output sla and sentiment
    mapfun = '''function(doc) { 
    if (doc.coordinates != null)
        emit(doc.sla, doc.sentiment);
    }'''

    option = {'map': mapfun}

    # create or update design document
    ddoc = db.get("_design/sla")
    if ddoc:
        ddoc["views"][topic] = option
        db.save(ddoc)
    else:
        design = {'views': {topic: option}}
        db["_design/sla"] = design

    result = db.view('sla/' + topic)

    # divide result in 3 different sentiments
    # count tweets for each of them
    sla_dict = {}
    for row in result:
        sentiment = row.value
        sla = row.key
        if sla in set(sla_dict.keys()):
            if sentiment == POSITIVE_SENT:
                sla_dict[sla]["positive_count"] += 1
            elif sentiment == NEGATIVE_SENT:
                sla_dict[sla]["negative_count"] += 1
            elif sentiment == NEUTRAL_SENT:
                sla_dict[sla]["neutral_count"] += 1
        else:
            sla_dict[sla] = {}
            sla_dict[sla]["positive_count"] = 0
            sla_dict[sla]["negative_count"] = 0
            sla_dict[sla]["neutral_count"] = 0

    new_sla_dict = {}
    # correlate with AURIN data
    with open(aurin_data) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sla = row[0]
            income = row[1]            
            if sla in set(sla_dict.keys()):
                pos_c = float(sla_dict[sla]["positive_count"])
                neg_c = float(sla_dict[sla]["negative_count"])
                neu_c = float(sla_dict[sla]["neutral_count"])
                total_c = pos_c + neg_c + neu_c
                if total_c != 0:
                    new_sla_dict[sla] = {}
                    happiness = pos_c / total_c
                    new_sla_dict[sla]["income"] = round(float(income), 3)
                    new_sla_dict[sla]["happiness"] = round(happiness, 5)

    file_path = output_path
    result_db = couch["scenario_" +  str(args.topic)]
    # output the result
    with open(file_path, 'w') as csvfile:
        for sla in new_sla_dict.keys():
            income = new_sla_dict[sla]["income"]
            happiness = new_sla_dict[sla]["happiness"]
            # put result back into database
            result_data ={"SLA" : sla, "Income": income, "Happiness" : happiness}
            result_db.save(result_data) 
            csvfile.write('{0},{1},{2}\n'.format(sla, income, happiness))


def main():
    args = parse_args()
    search_data(args)

if __name__ == '__main__':
    main()
