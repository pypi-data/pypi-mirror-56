import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from typing import List, Iterable


class PatternGenerator:
    """
    A Class to produce pattern files for the EMP framework.

    Methods
    -------
    __init__(self, links)
        Initialises class, links argument must be an iterable object of
        integers, denoting the links to be used for the pattern file.
    buildLink(self, index, data, pad)
        Provide data for a given link ID.
    writeToFile(filename)
        Write link data to file.
    plot()
        Plot current pattern file.
    """

    null_word: str = "0v{:016x}".format(0x0)
    null_header_length: int = 6
    bx_per_packet: int = 18
    frames_per_bx: int = 9
    packet_size: int = bx_per_packet * frames_per_bx

    def __init__(self, links: Iterable[int]) -> None:
        """
        Parameters
        ----------
        links : Iterable[int]
            Iterable object containing the link IDs (e.g. range(0, 18))
        """

        assert not hasattr(links, 'strip') \
            and (hasattr(links, '__getitem__') or hasattr(links, '__iter__')),\
            "links must be an iterable object of integers."
        self.links: pd.DataFrame = pd.DataFrame(columns=links)

    def generateHeader(self) -> List[str]:
        self.header: List[str] = [
            "Board x1",
            "Quad/Chan :        " + "              ".join(
                ["q{:02d}c{:01d}".format(i//4, i % 4) for i in self.links]),
            "Link :         " + "                ".join(
                ["{:03d}".format(i) for i in self.links])
        ]
        return self.header

    def padAndSegmentData(self, data) -> np.ndarray:
        def headerComplete(data, i) -> bool:
            header_slice = data[
                i*self.packet_size:i*self.packet_size+self.null_header_length
            ]
            return np.all(header_slice == self.null_word)
        data = np.array(data)
        num_packets: int = int(np.ceil(
            data.size/(self.packet_size - self.null_header_length)))
        for i in range(num_packets):
            while not headerComplete(data, i):
                data = np.insert(data, i*self.packet_size, self.null_word)
        return data

    def buildLink(
        self, index: int, data: Iterable[str], pad: bool = True
    ) -> pd.Series:
        """
        Provide data for a given link ID.

        Parameters
        ----------
        index : int
            Link index for the data to be entered on.
        data : Iterable[str]
            Iterable object of strings containing the data for the link.
        pad : bool
            If true, the data will be padded such that there is at least 6
            frames of null data at the start of the first packet. Data will
            also be segmented into packets of the correct length.
        """

        if pad:
            data = self.padAndSegmentData(data)
        else:
            data = np.array(data)
        self.links[index] = data
        return self.links[index]

    def writeToFile(self, filename: str) -> List[str]:
        """
        Write link data to file.

        Parameters
        ----------
        filename : str
            Path for output file.
        """

        self.links = self.links.fillna(self.null_word)
        header = self.generateHeader()
        values = self.links.values
        frames = ["Frame %04d : " % i + (" ").join(
            values[i]) for i in range(len(values))
        ]
        pattern: List[str] = header + frames
        f = open(filename, "w")
        for i in pattern:
            f.write(i + "\n")
        f.close()
        return header + frames

    def plot(self):
        sns.heatmap(self.links.applymap(lambda x: int(x[2:], 16)), cbar=False)
        plt.xlabel('Links')
        plt.ylabel('Frames')
