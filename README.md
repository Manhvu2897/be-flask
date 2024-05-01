# ✨ REST API Python module

This the api backend of api.tradersrescue.com.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to run the following command to install dependencies.

```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Copy file `.env.local.example`.

```bash
cp .env.local.example .env.local
```

2. Change the dependent variables.

```env
QUANT_CONNECT_BASE_URL=https://www.quantconnect.com/api/v2
QUANT_CONNECT_TOKEN=`YOUR_TOKEN`
QUANT_CONNECT_USER_ID=`YOUR_USER_ID`
```

3. Run project
```bash
python ./api/index.py
```

Finally, the project is run at http://localhost:8080/api/v1/

## 🚀 Unit test

- Run the following command to display code coverage

```bash
pytest
```
