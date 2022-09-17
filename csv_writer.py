import csv
def write_csv(filename, header, data):
    """Write provided data to CSV file.
    :param str filename: name of file to which data should be written
    :param list header: header for columns in csv file
    :param list data: list of list mapping values to columns
    """
    try:
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(data)
    except (IOError, OSError) as csv_file_error:
        print("Unable to write contents to csv file. Exception: {}".format(csv_file_error))

if __name__ == '__main__':
    header = ['name', 'age', 'gender']
    data = [['Richard', 32, 'M'], \
            ['Mumzil', 21, 'F'], \
            ['Melinda', 25, 'F']]
    filename = 'sample_output.csv'
    write_csv(filename, header, data)