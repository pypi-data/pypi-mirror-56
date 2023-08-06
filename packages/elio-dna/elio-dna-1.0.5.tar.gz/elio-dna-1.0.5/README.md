![](https://elioway.gitlab.io/eliothing/dna/elio-dna-logo.png)

> Dropping the pretense one thing is so different from another **the elioWay**

# dna ![experimental](https://elioway.gitlab.io/static/experimental.png "experimental")

Django models, views, forms, and templates, built out of schema.org "Things", the elioWay.

- [dna Documentation](https://elioway.gitlab.io/eliothing/dna)

## Installing

```bash
pip install elio-dna
```

- [Installing dna](https://elioway.gitlab.io/eliothing/dna/installing.html)

## Seeing is believing

```bash
git clone https://gitlab.com/eliothing/dna.git
cd dna
virtualenv --python=python3 venv-dna
source venv-dna/bin/activate
pip install -r requirements/local.txt
./init_chromosomes.sh
```

## Testing

Because the core feature of **dna** is building **Django** Models dynamically, some tests need to be run isolated.

## Nutshell

```
django-admin runserver
black .
```

- [dna Quickstart](https://elioway.gitlab.io/eliothing/dna/quickstart.html)
- [dna Credits](https://elioway.gitlab.io/eliothing/dna/credits.html)

![](https://elioway.gitlab.io/eliothing/dna/apple-touch-icon.png)

## License

[MIT](LICENSE) [Tim Bushell](mailto:tcbushell@gmail.com)
