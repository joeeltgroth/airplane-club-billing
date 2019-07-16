import csv
from dateutil.parser import parse


def read_csv(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        for row in csv.reader(csvfile):
            rows.append(row)
    # There are two header rows. Return only data.
    return rows[2:len(rows)]


def validate_rows(rows):
    pilot_logs = []
    for row in rows:
        pilot_log = Log(row[0], row[1], row[2], row[3], row[4], row[5],
                        row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        pilot_logs.append(pilot_log)
    return pilot_logs


class Log:

    def __init__(self, flight_date, pilot, plane, tach_in, tach_out, tach,
                 hobbs_in, hobbs_out, hobbs, gallons, price, fuel, misc):
        self.flight_date = parse(flight_date)
        self.pilot = pilot
        self.plane = plane
        self.tach_in = float(tach_in)
        self.tach_out = float(tach_out)
        self.tach = float(tach)
        self.hobbs_in = float(hobbs_in)
        self.hobbs_out = float(hobbs_out)
        self.hobbs = float(hobbs)
        self.gallons = 0
        if len(gallons) > 0:
            self.gallons = float(gallons)
        self.price = 0
        if len(price) > 0:
            self.price = float(price)
        self.fuel = 0
        if len(fuel) > 0:
            self.fuel = float(fuel.strip("$"))
        self.misc = 0
        if len(misc) > 0:
            self.misc = float(misc.strip("$"))

    def get_log_as_array(self):
        rate = 0
        if self.plane == "29265":
            rate = 92
        if self.plane == "741T":
            rate = 46
        due = self.hobbs * rate
        log = [[self.flight_date.strftime("%x")], [self.plane], [str(self.tach_out)], [str(self.tach_in)],
               [str(self.hobbs_out)], [str(self.hobbs_in)],
               [str(rate)], [str(self.tach)], [str(self.hobbs)], ['${:,.2f}'.format(due)], [str(self.gallons)],
               [str(self.price)], [str(self.fuel)], [str(self.misc)]]
        return log


def get_log_objects(filename):
    data_rows = read_csv(filename)
    log_entries = validate_rows(data_rows)
    return log_entries


def main():
    log_entries = get_log_objects('data/pilot_log.csv')

    for r in log_entries:
        print(r.pilot, r.price, r.tach_in, r.fuel)


if __name__ == "__main__":
    main()
