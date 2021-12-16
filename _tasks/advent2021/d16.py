import math

input = '''C20D718021600ACDC372CD8DE7A057252A49C940239D68978F7970194EA7CCB310088760088803304A0AC1B100721EC298D3307440041CD8B8005D12DFD27CBEEF27D94A4E9B033006A45FE71D665ACC0259C689B1F99679F717003225900465800804E39CE38CE161007E52F1AEF5EE6EC33600BCC29CFFA3D8291006A92CA7E00B4A8F497E16A675EFB6B0058F2D0BD7AE1371DA34E730F66009443C00A566BFDBE643135FEDF321D000C6269EA66545899739ADEAF0EB6C3A200B6F40179DE31CB7B277392FA1C0A95F6E3983A100993801B800021B0722243D00042E0DC7383D332443004E463295176801F29EDDAA853DBB5508802859F2E9D2A9308924F9F31700AA4F39F720C733A669EC7356AC7D8E85C95E123799D4C44C0109C0AF00427E3CC678873F1E633C4020085E60D340109E3196023006040188C910A3A80021B1763FC620004321B4138E52D75A20096E4718D3E50016B19E0BA802325E858762D1802B28AD401A9880310E61041400043E2AC7E8A4800434DB24A384A4019401C92C154B43595B830002BC497ED9CC27CE686A6A43925B8A9CFFE3A9616E5793447004A4BBB749841500B26C5E6E306899C5B4C70924B77EF254B48688041CD004A726ED3FAECBDB2295AEBD984E08E0065C101812E006380126005A80124048CB010D4C03DC900E16A007200B98E00580091EE004B006902004B00410000AF00015933223100688010985116A311803D05E3CC4B300660BC7283C00081CF26491049F3D690E9802739661E00D400010A8B91F2118803310A2F43396699D533005E37E8023311A4BB9961524A4E2C027EC8C6F5952C2528B333FA4AD386C0A56F39C7DB77200C92801019E799E7B96EC6F8B7558C014977BD00480010D89D106240803518E31C4230052C01786F272FF354C8D4D437DF52BC2C300567066550A2A900427E0084C254739FB8E080111E0'''

data = [int(v, 16) for v in input]
data = ''.join([f'{v:04b}' for v in data])

versions_sum = 0
def get_packet(data, indx):
    #if (len(data) - indx) < 6:
    #    return
    v = int(data[indx:indx+3], 2)
    global versions_sum
    versions_sum += v
    indx += 3
    t = int(data[indx:indx+3], 2)
    indx += 3
    if t == 4:  # literal
        value = []
        while data[indx] == '1':
            value.append(data[indx+1:indx+5])
            indx += 5
        value.append(data[indx + 1:indx + 5])
        value = int(''.join(value), 2)
        indx += 5
        print('literal', indx, value)
        return indx, value
    else:  # operation
        len_type_id = data[indx]
        indx += 1
        result = [t]
        if len_type_id == '0':
            l15 = int(data[indx:indx + 15], 2)
            print('subpacket len', l15)
            indx += 15
            saved_indx = indx + l15
            while True:
                indx, v = get_packet(data, indx)
                result.append(v)
                assert indx <= saved_indx
                if indx >= saved_indx:
                    break
            return saved_indx, result
        else:
            l11 = int(data[indx:indx + 11], 2)
            indx += 11
            print('subpacket cnt', l11)
            while l11:
                indx, v = get_packet(data, indx)
                result.append(v)
                l11 -= 1
            return indx, result

_, packets = get_packet(data, 0)
print(versions_sum)

def eval_packets(packets):
    if isinstance(packets, int):
        return packets
    else:
        t = packets[0]
        values = [eval_packets(p) for p in packets[1:]]
        print(t, values)
        if t == 0:
            return sum(values)
        elif t == 1:
            return math.prod(values)
        elif t == 2:
            return min(values)
        elif t == 3:
            return max(values)
        elif t == 5:
            assert len(values) == 2
            return 1 if values[0] > values[1] else 0
        elif t == 6:
            assert len(values) == 2
            return 1 if values[0] < values[1] else 0
        elif t == 7:
            assert len(values) == 2
            return 1 if values[0] == values[1] else 0
        else:
            assert False

v = eval_packets(packets)
print(v)