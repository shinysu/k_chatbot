import csv
fallback_file = 'fallback.csv'


def write_fallback_csv(text):
    print(text)
    with open(fallback_file, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([text])
