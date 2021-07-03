# Demo for Jaeger OpenTracing using Python

Instructions:

```bash
pip install -r requirements.txt

# terminal one
./runCLM

# terminal two
./runAPI

# terminal three
./runHadoop

# terminal four
./runES

# another terminal
./runJaeger

python verifyConnection.py
python runBackupJob.py

./runCronjb
```
