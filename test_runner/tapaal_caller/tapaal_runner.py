import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_dir)

from test_runner.base_test_runner import BaseTestRunner

from engine import Engine
from query import Query
from search_strategies import SearchStrategies

# Running: C:\Users\Henrik\Downloads\tapaal-4.0.0-win64\tapaal-4.0.0-win64\bin\verifypn64.exe --k-bound 13  --search-strategy RPFS  --reduction 1  --write-reduced C:\Users\Henrik\AppData\Local\Temp\reduced-18379011265041693289.pnml --ctl-algorithm czero --xml-queries 1 --col-reduction 1  C:\Users\Henrik\AppData\Local\Temp\verifyta15995705590230202181.xml C:\Users\Henrik\AppData\Local\Temp\verifyta10761695144415050781.xml

engine = Engine("C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe")

query = Query(
    search_strategy=SearchStrategies.random_heuristic,
    k_bound=13,
    pnml_path="C:/Users/Henrik/AppData/Local/Temp/verifyta15995705590230202181.xml",
    query_path="C:/Users/Henrik/AppData/Local/Temp/verifyta10761695144415050781.xml",
    reductions_enabled=True,
    reductions_colored_enabled=True,
    path_to_write_reduced=None
)



def run():
    result = query.run(engine)

    print(result)

# asyncio.run(run())


run()
