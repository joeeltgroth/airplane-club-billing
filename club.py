import csv


def read_csv(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        for row in csv.reader(csvfile):
            rows.append(row)
    # Ignore the 2 header rows.
    return rows[2:len(rows)]


class Club:

    def __init__(self, club_name, club_addr1, club_addr2, club_city, club_state, club_zip,
                 bill_name, bill_addr1, bill_addr2, bill_city, bill_state, bill_zip):
        self.club_name = club_name
        self.club_addr1 = club_addr1
        self.club_addr2 = club_addr2
        self.club_city = club_city
        self.club_state = club_state
        self.club_zip = club_zip

        self.bill_name = bill_name
        self.bill_addr1 = bill_addr1
        self.bill_addr2 = bill_addr2
        self.bill_city = bill_city
        self.bill_state = bill_state
        self.bill_zip = bill_zip


def load(rows):
    row = rows[0]
    club = Club(row[0], row[1], row[2], row[3], row[4], row[5],
                row[6], row[7], row[8], row[9], row[10], row[11])
    return club


def get_club_info(filename):
    data_rows = read_csv(filename)
    club = load(data_rows)
    return club


def main():
    club = get_club_info("data/club.csv")

    print(club.club_name, club.club_addr1, club.bill_addr1)


if __name__ == "__main__":
    main()
