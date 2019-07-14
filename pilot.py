
def read_pilots_file():
    pilots = []
    with open('pilot.csv', 'r') as pilots_file:
        first_line = True
        for l in pilots_file:
            if first_line:
                first_line = False
                continue
            pilot = l.split(',')
            pilots.append(pilot)
    return pilots


for pilot in read_pilots_file():
    print(pilot)

