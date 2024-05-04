import pickle

def save_data(state, filename="state.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(state, f)


def load_data(filename="state.pkl", default_value=None):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default_value
