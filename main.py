import pilot as pilot_reader
import pilot_log as pilot_log_reader
import club as club_reader
import invoice


def get_logs_for_pilot(pilot, logs):
    logs_to_return = []
    for l in logs:
        if l.pilot == pilot.short_name:
            logs_to_return.append(l)
    return logs_to_return


def main():
    pilots = pilot_reader.get_pilot_objects("data/pilot.csv")
    logs = pilot_log_reader.get_log_objects("data/pilot_log.csv")
    club = club_reader.get_club_info("data/club.csv")

    for p in pilots:
        p.logs = get_logs_for_pilot(p, logs)
        p.club = club

    print(pilots)

    for p in pilots:
        i = invoice.Invoice(p)
        i.build_invoice_for_pilot("output")


if __name__ == "__main__":
    main()
