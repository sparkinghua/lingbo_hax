import numpy as np

class pool:
    def __init__(self, pool_size = 500000):
        self.pool_size = pool_size
        self.buffer = []

    def submit(self, s, a):
        _len = len(self.buffer)
        if _len < self.pool_size:
            self.buffer.append((s, a))
        else:
            i_ = np.random.randint(_len)
            self.buffer[i_] = (s, a)

    def clean(self):
        self.buffer = []
    
    def len(self):
        return len(self.buffer)
        
    def get(self, batch_size = 2048):
        # if len(self.buffer) > 10000:
        np.random.shuffle(self.buffer)
        batch_ = self.buffer[:batch_size]
        x_batch, y_batch = [],[]
        for (x, y) in batch_:
            x_batch.append(x)
            y_batch.append(y)
        return np.array(x_batch), np.array(y_batch)
