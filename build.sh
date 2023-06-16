set -o errexit

pip install --upgrade pip
python -m pip install --upgrade pywin32
python Scripts/pywin32_postinstall.py -install
pip install -r requirements.txt
