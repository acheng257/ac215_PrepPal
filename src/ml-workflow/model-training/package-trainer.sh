rm -f trainer.tar trainer.tar.gz
tar cvf /tmp/trainer.tar package
gzip /tmp/trainer.tar
cp /tmp/trainer.tar.gz /app/
python upload_trainer_code.py
