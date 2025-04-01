from utils.formats import formats

class EncodingChain:
    def __init__(self):
        self.chain = []

    def add(self, format_name):
        self.chain.append(formats[format_name]())


    def encode(self, data):
        for encoder in self.chain:
            data = encoder.encode(data)
        return data

    def decode(self, data):
        for decoder in reversed(self.chain):
            try:
                data = decoder.decode(data)
            except Exception as e:
                print(f"Error in {decoder.__class__.__name__} decoding: {e}")
                print(f"Decoding stopped at: {data}")
                return data
        return data

