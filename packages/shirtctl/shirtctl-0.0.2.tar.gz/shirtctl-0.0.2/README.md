# shirtctl Python SDK

This is the shirtctl Python SDK.


## Push to PyPi

```
rm -rf dist/*
python3 setup.py sdist
pip3 install twine
python3 -m twine upload dist/*
```

Now you can `pip install shirtctl`