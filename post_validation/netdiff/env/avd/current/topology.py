import netdiff
import sys

def from_dut(in_data):

    topology_dict = dict()
    for hostname, details in in_data['duts'].items():
        for peer in details['show lldp neighbors']['lldpNeighbors']:
            new_peer_entry = {
                peer['port']: {
                    'neighbor_port_name': peer['neighborPort'],
                    'neighbor_hostname': peer['neighborDevice']
                }
            }
            if hostname in topology_dict.keys():
                topology_dict[hostname].update(new_peer_entry)
            else:
                topology_dict.update({hostname: new_peer_entry})
    
    return topology_dict


if __name__ == "__main__":
    eval_check_list = [  # list all functions allowed for eval() here
        'from_dut',
    ]
    args = netdiff.tools.parsers.src_dst_parser()
    in_data = netdiff.read._from(args.src_format, args.src_filename)
    if args.case in eval_check_list:
        out_data = eval(args.case + f'({in_data})')
        netdiff.write.to_file(args.dst_filename, args.dst_format, out_data)
    else:
        sys.exit(f'ERROR: Specified case {args.case} is not supported!')