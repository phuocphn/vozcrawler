# VozCrawler

VozCrawler is a tool for crawling voz.vn contents (thread supported only).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install other dependent libraries first. Is is recommended to use `virtualenv` to separate the working environments.

```bash
pip install flask scrapy
git clone https://github.com/phuocphn/vozcrawler 
```

## Usage
#### Crawling

```bash
scrapy crawl voz -a thread_url=<insert_thread_url_here>
---

For example:
scrapy crawl voz -a \ 
thread_url=https://voz.vn/t/tung-1-ti-lieu-vac-xin-g7-quyet-thoi-diem-ket-lieu-covid-19.321787/
```

#### Browsing
After you finish crawling, you can view the content by executing the following command
```bash
export FLASK_APP=voz.py && flask run
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



