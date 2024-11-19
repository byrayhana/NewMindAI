import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

''' 
Görev 1: Veri Temizleme ve Manipülasyonu (%25)
1.	Eksik verileri ve aykırı (outlier) verileri analiz edip temizleyin. Eksik verileri tamamlamak için çeşitli yöntemleri (ortalama, medyan gibi) kullanarak eksiklikleri doldurun.
2.	Fiyat ve harcama gibi değişkenler için aykırı değerleri tespit edip verisetinden çıkarın veya aykırı değerleri belirli bir aralık içine çekin.
3.	Müşteri verisi ile satış verisini musteri_id üzerinden birleştirerek geniş bir veri seti oluşturun.

'''
## GOREV 1.1
satis_dff = pd.read_csv("C:/NewMindAI/ODEV1/satis_verisi_5000.csv")
satis_df=satis_dff.copy()
musteri_dff= pd.read_csv("C:/NewMindAI/ODEV1/musteri_verisi_5000_utf8.csv")
musteri_df=musteri_dff.copy()
satis_df.info()


def ObjtoFloat(df,colname):
    '''
    Bu metod, obj formatını floata cevirir.
    Problemli değerler varsa, sütunun medyanı ile doldurur.
    :param df: dataframe
    :param colname: çevirmek istenen sütun
    :return: df[colname]
    '''
    df[colname] = df[colname].astype(str)
    problematic_values = df[colname][~df[colname].str.replace(".", "", regex=False).str.isnumeric()]
    if not problematic_values.empty:
        print(f"'{colname}' sütununda problemli değerler tespit edildi:")
        print(problematic_values)
    # tarih formatlı olan degerleri değiştirmek için NAN işaretle
    df[colname] = pd.to_numeric(df[colname], errors="coerce")
    # Sütunun medyanını hesapla
    median_fiyat = df[colname].median()
    df[colname] = df[colname].fillna(median_fiyat)
    df[colname] = df[colname].astype(float)
    return df[colname]

satis_df["toplam_satis"] = ObjtoFloat(satis_df,"toplam_satis")
satis_df["fiyat"] = ObjtoFloat(satis_df,"fiyat")
satis_df.describe().T
satis_df.isnull().values.any()

musteri_df.info()   #null deger yok
musteri_df.describe().T
musteri_df.isnull().values.any()

### iki verisetinde null deger olmadigi icin islem yapılmadı

###############################
## GOREV 1.2  Aykırı deger tespiti
# outlier threshold fonskiyonlastirma
def outlier_thresholds(dataframe, col_name, q1=0.25, q3=0.75):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

# satis df icin outlier kontrol
'''Boxplot analizinden aykırı değer olmadığını görebiliriz. Sağlamasını yapmak için 
q1 q3 kullanarak alt üst sınırları hesaplayıp bakalım.'''

outlier_thresholds(satis_df, "fiyat")
low, up = outlier_thresholds(satis_df, "fiyat")
satis_df[(satis_df["fiyat"] < low) | (satis_df["fiyat"] > up)].head() # Empty DataFrame

# musteri df icin outlier kontrol
outlier_thresholds(musteri_df, "harcama_miktari")
low, up = outlier_thresholds(musteri_df, "harcama_miktari")
musteri_df[(musteri_df["harcama_miktari"] < low) | (musteri_df["harcama_miktari"] > up)].head() # Empty DataFrame

outlier_thresholds(musteri_df, "yas")
low, up = outlier_thresholds(musteri_df, "yas")
musteri_df[(musteri_df["yas"] < low) | (musteri_df["yas"] > up)].head() # Empty DataFrame

### İki veriseti icin aykiri deger bulunamadı
##############################

## GOREV 1.3 Veri seti Birleştirme

df_merged = pd.merge(satis_df, musteri_df, on='musteri_id', how='inner')
df_merged.head()
df_merged.info()
df_merged.describe().T

'''
Görev 2: Zaman Serisi Analizi (%25)
1.	Satış verisi üzerinde haftalık ve aylık bazda toplam satış ve ürün satış trendlerini analiz edin.
2.	tarih sütununu kullanarak, her ayın ilk ve son satış günlerini bulun. Ayrıca, her hafta kaç ürün satıldığını hesaplayın.
3.	Zaman serisindeki trendleri tespit etmek için grafikler çizdirin (örneğin: aylık satış artışı veya düşüşü).
'''
## GOREV 2.1 Satis trendi analizi
# 'tarih' sütununu obj tipinde, datetime'e cevirelim
df_merged['tarih'] = pd.to_datetime(df_merged['tarih'])
# analiz icin toplam satisi hesaplayalım
df_merged["toplam_satis"] = df_merged["fiyat"] * df_merged["adet"]
#  Haftalık ve Aylık toplam satis trendlerin analizi icin
# ISO takvimine gore hafta ve ay bilgisi alalim (Yiln kacinci hafta ve ayine denk geliyor?) hafta 1-52 ay 1-12
df_merged['hafta'] = df_merged['tarih'].dt.isocalendar().week
df_merged['ay'] = df_merged['tarih'].dt.month

#aylik ve haftalik satislarin hesaplanmasi
haftalik_satis = df_merged.groupby('hafta')['toplam_satis'].sum()
aylik_satis = df_merged.groupby('ay')['toplam_satis'].sum()

## GOREV 2.2
ayin_ilk_satis_gunu = df_merged.groupby("ay")["tarih"].min()
ayin_son_satis_gunu = df_merged.groupby("ay")["tarih"].max()

haftalik_adet_satisi = df_merged.groupby("hafta")["adet"].sum()

## GOREV 2.3
# Haftalık Satış Grafiği
plt.figure(figsize=(10, 5))
plt.plot(haftalik_satis.index, haftalik_satis.values, marker='o', color='b', label='Haftalık Satış')
plt.title('Haftalık Satış Trendleri')
plt.xlabel('Hafta')
plt.ylabel('Toplam Satış')
plt.grid(True)
plt.show()
# Aylık Satış Grafiği
plt.figure(figsize=(10, 5))
plt.plot(aylik_satis.index, aylik_satis.values, marker='o', color='b', label='Aytlık Satış')
plt.title('Aylık Satış Trendleri')
plt.xlabel('Ay')
plt.ylabel('Toplam Satış')
plt.grid(True)
plt.show()
# Haftalık Adet Satışı
plt.figure(figsize=(10, 5))
plt.plot(haftalik_adet_satisi.index, haftalik_adet_satisi.values, marker='o', color='b', label='Aytlık Satış')
plt.title('Hatfalık Adet Trendleri')
plt.xlabel('Hafta')
plt.ylabel('Adet')
plt.grid(True)
plt.show()

'''
Görev 3: Kategorisel ve Sayısal Analiz (%25)
1.	Ürün kategorilerine göre toplam satış miktarını ve her kategorinin tüm satışlar içindeki oranını hesaplayın.
2.	Müşterilerin yaş gruplarına göre satış eğilimlerini analiz edin. (Örnek yaş grupları: 18-25, 26-35, 36-50, 50+)
3.	Kadın ve erkek müşterilerin harcama miktarlarını karşılaştırın ve harcama davranışları arasındaki farkı tespit edin.
'''
## GOREV 3.1
kat_topalm_satis= df_merged.groupby("kategori")["toplam_satis"].sum()
kat_satis_orani =  kat_topalm_satis / kat_topalm_satis.sum() * 100

print("Kategori Bazlı Toplam Satış Miktarları:")
print(kat_topalm_satis)
print("\nKategori Bazlı Oranlar (%):")
print(kat_satis_orani)

# Gorsellestirme
plt.figure(figsize=(8, 6))
kat_satis_orani.plot(kind='bar', color='green', title="Kategori Bazlı Satış Oranları")
plt.ylabel("Oran (%)")
plt.show()

## GOREV 3.2
df_merged['yas_grubu'] = df_merged['yas'].apply(lambda x: '18-25' if 18 <= x <= 25
                                  else '26-35' if 26 <= x <= 35
                                  else '36-50' if 36 <= x <= 50
                                  else '50+')
yas_grubu_satis =  df_merged.groupby("yas_grubu")["toplam_satis"].sum()

print("\nYaş Gruplarına Göre Toplam Satış:")
print(yas_grubu_satis)
# Gorsellestirme
plt.figure(figsize=(10, 5))
plt.plot(yas_grubu_satis.index, yas_grubu_satis.values, marker='o', color='b', label='Yaş Grubuna Göre Toplam Satış')
plt.title(' Yaş Grubuna Göre Toplam Satış')
plt.xlabel('Yaş Grubu')
plt.ylabel("Toplam Satış")
plt.grid(True)
plt.show()

## GOREV 3.3
ort_cinsiyet_harcama = df_merged.groupby("cinsiyet")["harcama_miktari"].mean()

cinsiyet_toplam_harcama = df_merged.groupby("cinsiyet")["harcama_miktari"].sum()

print("\nCinsiyete Göre Ortalama Harcama:")
print(ort_cinsiyet_harcama)

print("\nCinsiyete Göre Toplam Harcama:")
print(cinsiyet_toplam_harcama)

##  Kadinlarin toplam harcama ort erkeklerden daha fazla

'''
Görev 4: İleri Düzey Veri Manipülasyonu (%25)
1.	Müşterilerin şehir bazında toplam harcama miktarını bulun ve şehirleri en çok harcama yapan müşterilere göre sıralayın.
2.	Satış verisinde her bir ürün için ortalama satış artışı oranı hesaplayın. 
Bu oranı hesaplamak için her bir üründe önceki aya göre satış değişim yüzdesini kullanın.
3.	Pandas groupby ile her bir kategorinin aylık toplam satışlarını hesaplayın ve değişim oranlarını grafikle gösterin.
'''
## GOREV 4.1
sehir_toplam_harcama= df_merged.groupby("sehir")["harcama_miktari"].sum().sort_values(ascending=False)
print(sehir_toplam_harcama)
# Gorsellestirme
plt.figure(figsize=(8, 6))
sehir_toplam_harcama.plot(kind='bar', color='blue', title="Şehir Bazlı Toplam Harcama Miktarı")
plt.ylabel("Harcama Miktarı")
plt.show()

## GOREV 4.2
urun_aylik_satis = df_merged.groupby(['ay', 'ürün_kodu'])['toplam_satis'].sum().reset_index()

urun_aylik_satis['satis_degisim'] = urun_aylik_satis.groupby('ürün_kodu')['toplam_satis'].pct_change()  #yuzdesel degisim hesapla
ortalama_satis_artisi = urun_aylik_satis.groupby('ürün_kodu')['satis_degisim'].mean()
print(ortalama_satis_artisi)



## GOREV 4.3

kat_aylik_satis = df_merged.groupby(['ay', 'kategori'])['toplam_satis'].sum().reset_index()
kat_aylik_satis["satis_degisim"] =  kat_aylik_satis.groupby('kategori')['toplam_satis'].pct_change()
ort_aylik_satis= kat_aylik_satis.groupby("kategori")["satis_degisim"].mean()
print(ort_aylik_satis)
plt.figure(figsize=(10, 6))
for kat in kat_aylik_satis['kategori'].unique():
    kategori_data = kat_aylik_satis[kat_aylik_satis['kategori'] == kat]
    plt.plot(kategori_data['ay'], kategori_data['satis_degisim'], label=kat)

plt.title('Kategorilerin Aylık Satış Değişim Oranları')
plt.xlabel('Ay')
plt.ylabel('Satış Değişim Oranı')
plt.legend()
plt.grid()
plt.show()