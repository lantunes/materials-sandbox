import pandas as pd


if __name__ == '__main__':
    df = pd.read_pickle("out/all_stable_bandgap.pkl")

    with open("all_stable_bandgap_corpus.txt", "wt") as f:
        for i in range(len(df['structure'])):
            struct = df['structure'][i]
            f.write(" ".join(struct.symbol_set) + "\n")
