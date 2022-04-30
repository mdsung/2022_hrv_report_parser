import re
from dataclasses import dataclass


class Parser:
    def __init__(self, html_path):
        self.html_path = html_path
        self.html_list = self.read_html_file()

    def process(self):
        html_chucks = self.create_html_generator()

        return (
            General.from_html(html_chucks[0]),
            TimeDomain.from_html(html_chucks[1]),
            FrequencyDomain.from_html(html_chucks[2]),
            Nonlinear.from_html(html_chucks[3]),
        )

    def create_html_generator(self):
        keywords = ["General", "Time-Domain", "Frequency-Domain", "Nonlinear"]
        keyword_indexes = [
            self.html_list.index(f"<h3>{key}</h3>") for key in keywords
        ]
        keyword_indexes.append(len(self.html_list))

        return [
            self.html_list[keyword_indexes[i] : keyword_indexes[i + 1]]
            for i in range(len(keyword_indexes) - 1)
        ]

    def read_html_file(self):
        with open(self.html_path, "r") as f:
            return [l.strip() for l in f.readlines()]


@dataclass
class General:
    start_analysis: str
    end_analysis: str
    total_included_beat: int
    normal_beat: int
    ectopic_beat: int

    def __post_init__(self):
        self.total_included_beat = int(self.total_included_beat)
        self.normal_beat = int(self.normal_beat)
        self.ectopic_beat = int(self.ectopic_beat)

    @classmethod
    def from_html(cls, html_list):
        ids = [
            i for i, html in enumerate(html_list) if 'class="rowtitle"' in html
        ]
        args = [
            remove_td(html_list[rowtitle_index + 1]) for rowtitle_index in ids
        ]

        return General(*args)


@dataclass
class TimeDomain:
    average_rr: float
    median_rr: float
    SDRR: float
    SDARR: float
    CVRR: float
    average_rate: float
    sd_rate: float
    SDSD: float
    RMSSD: float
    pRR50: float

    @classmethod
    def from_html(cls, html_list):
        ids = [
            i for i, html in enumerate(html_list) if 'class="rowtitle"' in html
        ]
        args = [
            parse_number(remove_td(html_list[rowtitle_index + 1]))
            for rowtitle_index in ids
        ]
        return TimeDomain(*args)


@dataclass
class FrequencyDomain:
    total_power_ms2: int
    vlf_power_ms2: int
    vlf_power_percent: float
    lf_power_ms2: float
    lf_power_percent: float
    lf_power_nu: float
    hf_power_ms2: float
    hf_power_percent: float
    hf_power_nu: float
    hf_lf_power_percent: float

    @classmethod
    def from_html(cls, html_list):
        min_index = html_list.index('<table class="table_power">')
        max_index = [
            i for i, html in enumerate(html_list) if "</table>" in html
        ][1]
        args = parse_numbers("".join(html_list[min_index:max_index]))
        return FrequencyDomain(*args)  # type: ignore


@dataclass
class Nonlinear:
    sd1: float
    sd2: float

    @classmethod
    def from_html(cls, html_list):
        ids = [
            i for i, html in enumerate(html_list) if 'class="rowtitle"' in html
        ]
        args = [
            parse_number(remove_td(html_list[rowtitle_index + 1]))
            for rowtitle_index in ids
        ]
        return Nonlinear(*args)


def remove_td(text):
    return text.replace("<td>", "").replace("</td>", "")


def parse_number(text):
    return float(re.findall(r"[0-9.]+", text)[0])


def parse_numbers(text):
    return [float(number) for number in re.findall(r"[0-9.]+", text)]
