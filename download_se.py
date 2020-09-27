from pymatgen import MPRester
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='The materialsproject.org API key')
    args = parser.parse_args()

    client = MPRester(args.key)

    criteria= {
        # "elements": {
        #     "$all": ["Se"]
        # },
        "e_above_hull": 0.0
    }

    properties = ['structure', 'band_gap']

    print('Fetching data...')

    result = client.query(criteria, properties)

    print('Converting to dataframe...')

    gaps_data = pd.DataFrame(result)

    print('Pickling...')

    gaps_data.to_pickle('stable_o_gaps_data.pkl')
