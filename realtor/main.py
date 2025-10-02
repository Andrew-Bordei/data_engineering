from extract import Extract
from transform import Transform
from load import Load

def realtor_pipeline(city: str, state_abbr: str):
    extract = Extract(1, 39)
    transform = Transform()
    load = Load()

    data = extract.extraction_process(city, state_abbr)
    df = transform.transform(data)
    # df.to_csv("realtor_2025-09-14")
    load_df = load.controller('database', df)

    return load_df 

if __name__ == '__main__':
    realtor_pipeline('Boise', 'ID')