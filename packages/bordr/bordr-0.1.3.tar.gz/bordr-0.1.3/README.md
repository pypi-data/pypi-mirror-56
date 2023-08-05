## bordr ##

A pip installable version of RDRPOSTagger with Tibetan-specific changes.

 - See the original [RDRPOSTagger](https://github.com/datquocnguyen/RDRPOSTagger) for documentation.
 - Check the [modifications](https://github.com/Esukhia/bordr/blob/master/CHANGELOG.md) implemented in this repo.
 - See [rdr-data](https://github.com/Esukhia/rdr-data) for RDR models for Tibetan.
 - See [usage.py](https://github.com/Esukhia/bordr/blob/master/usage.py) for the programmatic interface available in bordr

### Maintenance

Build the source dist:

```bash
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```bash
twine upload dist/*
```