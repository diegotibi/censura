#!/usr/bin/env python3

import csv
import optparse
import validators

options = None
default_blackhole = '127.0.0.1'
default_bind_block_zonefile = '/etc/bind/zones/dns_block_zone.zone'
out_format_list = ['unbound', 'bind']
in_format_list = ['cncpo', 'aams', 'admt', 'manuale']


def write_unbound_list(outfile, blacklist, blackhole):
    with open(outfile, 'w') as fp:
        fp.write("server:\n")
        for c in blacklist:
            fp.write(f'local-zone: \"{c}\" redirect \n')
            fp.write(f'local-data: \"{c} A {blackhole}\"\n')
    return


def write_bind_data(outfile, blacklist, zonefile):
    with open(outfile, 'w') as fp:
        for c in blacklist:
            fp.write('zone "{}" {{ type master; file "{}"; }};\n'.format(c, zonefile))
    return


def parse_cncpo_list(infile):
    black_list = []
    i = 0

    with open(infile) as csv_file:
        spam_reader = csv.reader(csv_file, delimiter=';')
        for row in spam_reader:
            if i == 0:
                i = 1
                continue
            if row is not None and len(row) > 0:
                data = row[1].strip().lower()
                if len(data) > 0:
                    black_list.append(data)
    return list(set(black_list))


def parse_list(infile):
    black_list = []
    with open(infile) as fp:
        while line := fp.readline():
            data = line.strip().lower()
            if len(data) > 0:
                black_list.append(data)
    return list(set(black_list))


def filter_valid_domain(blacklist):
    return [current_list for current_list in blacklist if validators.domain(current_list)]


def filter_whitelist(blacklist, whitelist):
    if blacklist is None or whitelist is None:
        return []
    if (len(blacklist) == 0) or (len(whitelist) == 0):
        return blacklist
    bls = set(blacklist)
    wls = set(whitelist)
    return list(bls - wls)


def main():
    global options
    # Elaborazione argomenti della linea di comando
    usage = "usage: %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option("-i", "--input", dest="in_file", help="File di elenco degli url in input")
    parser.add_option("-o", "--output", dest="out_file", help="File di output generato")
    parser.add_option("-b", "--blackhole", dest="blackhole", help="Indirizzo stop-page/blackhole")
    parser.add_option("-f", "--oformat", dest="out_format", help="Formato dns in output (unbound, bind)")
    parser.add_option("-d", "--iformat", dest="in_format", help="Formato lista in ingresso (cncp, aams, admt, manuale)")
    parser.add_option("-z", "--zonefile", dest="bind_zonefile", help="Pathname del file di zona bind di blocco")
    parser.add_option("-w", "--whitelist", dest="wl_file", help="File di elenco degli url da mettere in whitelist")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    if len(args) == 1:
        parser.error("Numero di argomenti non corretto")
    if (options.in_file is None) or (options.out_file is None):
        parser.error("Numero di argomenti non corretto")
    if options.out_format is None or options.out_format not in out_format_list:
        parser.error("Formato di output errato")
    if options.in_format is None or options.in_format not in in_format_list:
        parser.error("Formato di input errato")
    if options.verbose:
        print(f"File di input       : {options.in_file}")
        print(f"File di output      : {options.out_dir}")
        print(f"Formato             : {options.out_format}")
    #
    if options.blackhole is None:
        options.blackhole = default_blackhole
    if options.bind_zonefile is None:
        options.bind_zonefile = default_bind_block_zonefile
    wl = parse_list(options.wl_file) if options.wl_file is not None else []
    #
    if options.in_format == 'cncpo':
        dns_bl = parse_cncpo_list(options.in_file)
    elif options.in_format in ['aams', 'admt', 'manuale']:
        dns_bl = parse_list(options.in_file)
    else:
        print("Formato di input non risconosciuto")
        return None
    # Validazione elementi caricati
    dns_bl = filter_valid_domain(dns_bl)
    dns_bl = filter_whitelist(dns_bl, wl)

    # Generazione file di output
    if options.out_format == 'unbound':
        write_unbound_list(options.out_file, dns_bl, options.blackhole)
    elif options.out_format == 'bind':
        write_bind_data(options.out_file, dns_bl, options.bind_zonefile)
    else:
        print("Formato di output non risconosciuto")
        return None
    return


if __name__ == '__main__':
    main()
