import csv

def parse_file(theFile):
    art_list = []
    with open(theFile) as f:
        for line in f:
            csv_reader = csv.reader(f, delimiter = ',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'line: {line_count}, count: {len(row)}, {row[9]}, {row[47]}')
                    line_count += 1

                    if (row[9] and row[47]): #confirm that title, artist, link exist
                        art_obj = Art(row[9], row[17] + " " + row[18], row[11], row[12], row[28],
                            row[31], row[32], row[47]) #title, artist, period, dynasty, date, medium, dimensions, resource_link
                        art_list.append(art_obj)
            print(f'Processed {line_count} lines.')
    return art_list

def get_line_count(theFile):
    line_count = 0
    with open(theFile) as f:
        for line in f:
            line_count += 1
    return line_count

def get_row(theFile, index):
    art_obj = None
    with open(theFile) as f:
        csv_reader = csv.reader(f, delimiter = ',')
        for i in range(index):
            next(csv_reader)
        row = next(csv_reader)
        if (row[9] and row[47]): #confirm that title, artist, link exist
            art_obj = Art(row[9], row[17] + " " + row[18], row[11], row[12], row[28],
                row[31], row[32], row[47]) #title, artist, period, dynasty, date, medium, dimensions, resource_link
    return art_obj

class Art:
    def __init__(self, title, artist, period, dynasty, date, medium, dimensions, resource_link):
        self.title = title #required
        self.artist = artist #required
        self.period = period
        self.dynasty = dynasty
        self.date = date
        self.medium = medium
        self.dimensions = dimensions
        self.resource_link = resource_link #required


    def __str__(self): 
        return_string = ""
        if self.title:
            return_string += "\"" + self.title + "\""
        if self.artist.strip() != "":
            return_string += ", " + self.artist + "\n"
        if self.period:
            return_string += self.period + " "
        if self.dynasty:
            return_string += self.dynasty + " "
        if self.date:
            return_string += self.date + " "
        if self.medium:
            return_string += self.medium + " "
        if self.dimensions:
            return_string += ", " + self.dimensions
        return_string += "\n" + self.resource_link
        return return_string


