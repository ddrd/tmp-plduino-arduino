from make_json import *
from make_json.paths import *

open(OUT_JSON, "w").write(make_json())
print "done"
