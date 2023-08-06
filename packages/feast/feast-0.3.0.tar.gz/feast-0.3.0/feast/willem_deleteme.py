import numpy as np

import pandas as pd

import pyarrow as pa

df = pd.DataFrame(
    {
        "one": [-1, np.nan, 2.5],
        "two": ["foo", "bar", "baz"],
        "three": [True, False, True],
    },
    index=list("abc"),
)

table = pa.Table.from_pandas(df)  # type: pa.table
batches = table.to_batches()

for batch in batches:
    batch = batch  # type: pa.RecordBatch
    print(batch.schema)
    print(batch.columns)
    print(batch.to_pydict())
    print(batch.to_pandas())
    print(batch.to_pandas().dtypes)
