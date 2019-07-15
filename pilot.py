import csv


def read_csv(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        for row in csv.reader(csvfile):
            rows.append(row)
    # Ignore the header row.
    return rows[1:len(rows)]


class Pilot:

    def __init__(self, id, name, short_name, addr1, addr2, city,
                 state, zip, email, balance, amt_paid):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        if len(balance) > 0:
            self.balance = float(balance.strip("$"))
        else:
            self.balance = 0.0
        if len(amt_paid) > 0:
            self.amt_paid = float(amt_paid)
        else:
            self.amt_paid = 0.0


def load_rows(rows):
    pilots = []
    for row in rows:
        pilot = Pilot(row[0], row[1], row[2], row[3], row[4], row[5],
                   row[6], row[7], row[8], row[9], row[10])
        pilots.append(pilot)
    return pilots


def get_pilot_objects(filename):
    data_rows = read_csv(filename)
    pilots_array = load_rows(data_rows)
    return pilots_array


def main():
    pilots = get_pilot_objects('data/pilot.csv')

    for p in pilots:
        print(p.id, p.name, p.short_name, p.amt_paid)


if __name__ == "__main__":
    main()
