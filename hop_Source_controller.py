
from pyfastbss_testbed import pyfbss_tb

class hop_Source_controller:

    def __init__(self, folder_address, duration, source_number, mixing_type, max_min, mu_sigma) -> None:
        super().__init__()
        self.folder_address = folder_address
        self.duration = duration
        self.source_number = source_number
        self.mixing_type = mixing_type
        self.max_min = max_min
        self.mu_sigma = mu_sigma
        self.S, self.A, self.X = pyfbss_tb.generate_matrix_S_A_X(
            self.folder_address, self.duration, self.source_number, self.mixing_type, self.max_min, self.mu_sigma)

    def get_S(self):
        return self.S

    def get_A(self):
        return self.A

    def get_X(self):
        return self.X


# if __name__ == "__main__":
#     # 测试一下这个类



