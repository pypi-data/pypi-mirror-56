import pandas as pd
import numpy as np


class PatternGenerator:
    null_word = "0v{:016x}".format(0x0)
    null_header_length = 6
    bx_per_packet = 18
    frames_per_bx = 9
    packet_size = bx_per_packet * frames_per_bx

    def __init__(self, links):
        assert not hasattr(links, 'strip') \
            and (hasattr(links, '__getitem__') or hasattr(links, '__iter__')),\
            "links must be an iterable object of integers."
        self.links = pd.DataFrame(columns=links)

    def generateHeader(self):
        self.header = [
            "Board x1",
            "Quad/Chan :        " + "              ".join(
                ["q{:02d}c{:01d}".format(i//4, i % 4) for i in self.links]),
            "Link :         " + "                ".join(
                ["{:03d}".format(i) for i in self.links])
        ]
        return self.header

    def padAndSegmentData(self, data):
        def headerNotComplete(data):
            header_slice = data[
                i*self.packet_size,
                i*self.packet_size+self.null_header_length
            ]
            return np.all(header_slice != self.null_word)
        data = np.array(data)
        num_packets = int(np.ceil(
            data.size/(self.packet_size - self.null_header_length)))
        for i in range(num_packets):
            while headerNotComplete(data):
                data = np.insert(data, i*self.packet_size, self.null_word)
        return data

    def buildLink(self, index, data, pad=True):
        if pad:
            data = self.padAndSegmentData(data)
        else:
            data = np.array(data)
        self.links[index] = data
        return self.links[index]

    def writeToFile(self, filename):
        self.links = self.links.fillna(self.null_word)
        header = self.generateHeader()
        values = self.links.values
        frames = ["Frame %04d : " % i + (" ").join(
            values[i]) for i in range(len(values))
        ]
        pattern = header + frames
        f = open(filename, "w")
        for i in pattern:
            f.write(i + "\n")
        f.close()
        return header + frames
