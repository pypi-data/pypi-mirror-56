from abc import ABC


class Gatk_3_3_7(ABC):

    @staticmethod
    def container():
        return "broadinstitute/gatk3:3.7-0"
