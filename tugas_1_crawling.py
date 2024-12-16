# -*- coding: utf-8 -*-
"""tugas-1-crawling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19vGzv00n9-WbX2Gw-qiz1t1Zo4tpSMV5

# Crawling Web Berita CNBC Indonesia

## Apa itu Crawling?

Crawling adalah proses di mana mesin pencari mengunjungi halaman-halaman web untuk menemukan dan mengindeks konten. Dalam proses ini, bot atau robot yang dikenal sebagai "crawler" atau "spider" mengumpulkan informasi dari berbagai halaman web untuk memastikan bahwa konten terbaru dan relevan tersedia dalam indeks mesin pencari.

## Proses Crawling

Pada contoh ini, proses crawling dilakukan pada website CNBC Indonesia untuk mengumpulkan data berita. Artikel-artikel berita akan diambil dari beberapa kategori yang berbeda, seperti Research, News, Tech, dan Market.

## Tool atau libray yang diperlukan
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

"""- **Requests** digunakan untuk mengambil konten HTML/HTTP dari sebuah website.
- **BeautifulSoup** berfungsi untuk mengurai dan memproses data dari HTML/XML.
- **Pandas** digunakan untuk menyimpan data dalam format yang mudah dibaca dan diproses.

## Code Program

#### Inisialisasi Variabel dan URL
"""

judul = []
tanggal = []
isi = []
url_list = []
kategori_list = []

base_urls = [
    "https://www.cnbcindonesia.com/research/indeks/127/",
    "https://www.cnbcindonesia.com/news/indeks/3/",
    "https://www.cnbcindonesia.com/tech/indeks/12/",
    "https://www.cnbcindonesia.com/market/indeks/5/"
]
categories = [
    "Research",
    "News",
    "Tech",
    "Market"
]

"""Variabel-variabel ini digunakan untuk menyimpan data yang akan diambil dari website. `base_urls` adalah daftar URL yang akan dikunjungi untuk mengambil artikel.

#### Proses Pengambilan Data
"""

payload = {'tipe': 'artikel'}

for news, category in zip(base_urls, categories):
    for page in range(1, 11):  # Mengambil dari halaman 1 hingga 10
        url = f"{news}{page}"
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article")

            # Menambahkan kategori ke dalam list
            kategori = category  # Menggunakan kategori dari list `categories`

            # Pada kode dibawah ini akan mengunjungi satu persatu artikel yang ada di halaman ke-n
            for article in articles:
                link = article.find("a")["href"]  # Untuk mendapatkan link
                article_response = requests.get(link)
                if article_response.status_code == 200:
                    articleFull = BeautifulSoup(article_response.content, "html.parser")
                    judulArtikel = articleFull.find(
                        "h1", class_="mb-4 text-32 font-extrabold"
                    ).text.strip()  # Untuk mendapatkan judul artikel
                    tanggalArtikel = articleFull.find(
                        "div", class_="text-cm text-gray"
                    ).text.strip()  # Untuk mendapatkan tanggal artikel diterbitkan

                    # Isi artikel terdapat pada tag div dengan class detail-text
                    artikel_element = articleFull.find("div", class_="detail-text")
                    # Mengambil semua isi artikel yang terdapat di tag p
                    artikelTeks = [p.get_text(strip=True) for p in artikel_element.find_all("p")]
                    artikel_content = "\n".join(artikelTeks)

                    # Menambahkan judul, tanggal, isi, dan url ke dalam list yang sudah diinisialisasikan
                    judul.append(judulArtikel)
                    tanggal.append(tanggalArtikel)
                    isi.append(artikel_content)
                    url_list.append(link)
                    kategori_list.append(kategori)
                else:
                    print(f"Error: {article_response.status_code}")
        else:
            print(f"Error : {response.status_code}")

"""Setiap artikel diambil dan data seperti judul, tanggal, dan isi artikel diproses dan disimpan dalam list yang telah disiapkan. Jika ada error dalam pengambilan data, status error akan diprint

##### Mengecek apakahh panjang hasil scrapping sama
"""

print(len(judul), len(tanggal), len(isi), len(url_list), len(kategori_list))

"""### Convert data ke dalam csv"""

# Membuat dataframe dari list data
df = pd.DataFrame({"judul": judul, "tanggal": tanggal, "isi": isi, "url": url_list, "kategori": kategori_list})

# Menyimpan dataframe ke file csv
df.to_csv("data-artikel-cnbc.csv", index=False)

"""Setelah semua data dikumpulkan, data tersebut disimpan ke dalam sebuah dataframe menggunakan Pandas dan disimpan dalam format CSV untuk analisis lebih lanjut.

"""

df.head()

df["kategori"].value_counts()

df["kategori"].value_counts().plot(kind="bar")
plt.show()

"""## Kesimpulan

Dengan menggunakan requests, BeautifulSoup, dan Pandas, kita dapat melakukan web scraping untuk mengumpulkan data dari berbagai halaman web. Ini memungkinkan kita untuk menganalisis data dari website dengan lebih efisien.
"""