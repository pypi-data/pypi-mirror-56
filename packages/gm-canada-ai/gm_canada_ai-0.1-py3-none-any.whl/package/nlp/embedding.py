import numpy as np


class Embedding:
    def __init__(self, model='default_model', max_len=100, dim=300,
                 return_result=0,
                 save_result=0):
        self.max_len = max_len
        self.dim = dim
        self.model = model
        self.return_result = return_result
        self.save_result = save_result

    def transform_text_to_vector(self, path_out, row):
        temp = np.zeros((self.max_len, self.dim))

        if not row:
            row = 'missing verbatim'

        row = row.split(' ')
        for i, row_ in enumerate(row):
            if i < self.max_len:
                temp[i, :] = np.array(self.model[row_]).reshape(-1, self.dim)
            else:
                break
            # [:self.max_len, :self.dim]

        if self.return_result:
            return temp
        elif self.save_result:
            np.save(path_out, temp)
