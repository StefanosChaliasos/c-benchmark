c-benchmark
-----------

Docker
------

```bash
sudo docker build -t test .
docker run --rm -it test /bin/bash
# Inside docker container
python3 run-benchmark.py
```

Local
-----

* Install [CScout](https://github.com/dspinellis/cscout)
* To run `cd test-suite && python run-benchmark.py`
