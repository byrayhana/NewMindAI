import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.options.display.float_format = '{:.2f}'.format

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
    df[colname] = df[colname].astype(float)
    median_value = df[colname].median()
    df[colname] = df[colname].fillna(median_value)
    return df[colname]

satis_df["toplam_satis"] = ObjtoFloat(satis_df,"toplam_satis")
satis_df["fiyat"] = ObjtoFloat(satis_df,"fiyat")
satis_df.describe().T
satis_df.info()
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
    print(f"Alt Sınır: {low_limit}, Üst Sınır: {up_limit}")
    return low_limit, up_limit
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

replace_with_thresholds(satis_df,"toplam_satis")

'''
Kategori bazli  toplam_satis outlier 
  count    mean     std     min     25%     50%      75%      max
toplam_satis 5000.00 9779.81 9376.72   22.28 2293.68 6643.45 14084.71 32381.22


Kategori bazlı olmayan toplam satis outlier
               count    mean     std     min     25%     50%      75%      max
toplam_satis 5000.00 9785.05 9387.77   22.28 2293.68 6643.45 14084.71 31771.26
Çok önemli bir fark yok o yüzden normal outlier ile devam 
'''
replace_with_thresholds(satis_df,"fiyat")
replace_with_thresholds(musteri_df,"harcama_miktari")
satis_df.describe().T
musteri_df.describe().T



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
satis_df['tarih'] = pd.to_datetime(satis_df['tarih'])
# analiz icin toplam satisi hesaplayalım
satis_df["toplam_satis"] = satis_df["fiyat"] * satis_df["adet"]
#  Haftalık ve Aylık toplam satis trendlerin analizi icin
# ISO takvimine gore hafta ve ay bilgisi alalim (Yiln kacinci hafta ve ayine denk geliyor?) hafta 1-52 ay 1-12
satis_df['hafta'] = satis_df['tarih'].dt.isocalendar().week
satis_df['ay'] = satis_df['tarih'].dt.month

#aylik ve haftalik satislarin hesaplanmasi
haftalik_satis = satis_df.groupby('hafta')['toplam_satis'].sum()
aylik_satis = satis_df.groupby('ay')['toplam_satis'].sum()

## GOREV 2.2
ayin_ilk_satis_gunu = satis_df.groupby("ay")["tarih"].min()
ayin_son_satis_gunu = satis_df.groupby("ay")["tarih"].max()

haftalik_adet_satisi = satis_df.groupby("hafta")["adet"].sum()
aylik_adet_satisi =  satis_df.groupby("ay")["adet"].sum()

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
# Aylık Adet Satışı
plt.figure(figsize=(10, 5))
plt.plot(aylik_adet_satisi.index, aylik_adet_satisi.values, marker='o', color='b', label='Aytlık Satış')
plt.title('Aylık Adet Trendleri')
plt.xlabel('Ay')
plt.ylabel('Adet')
plt.grid(True)
plt.show()

## KAtegıri bazli satis trendleri
kategori_aylik_satis = satis_df.groupby(['kategori', 'ay'])['toplam_satis'].sum().reset_index()
plt.figure(figsize=(12, 6))

# Her kategori için ayrı bir trend çizimi
for kategori in kategori_aylik_satis['kategori'].unique():
    kategori_data = kategori_aylik_satis[kategori_aylik_satis['kategori'] == kategori]
    plt.plot(
        kategori_data['ay'],
        kategori_data['toplam_satis'],
        marker='o',
        label=kategori
    )

plt.title('Kategori Bazında Aylık Satış Trendleri')
plt.xlabel('Ay')
plt.ylabel('Toplam Satış')
plt.legend(title="Kategori")
plt.grid(True)
plt.show()

'''
 YORUM
 aylık ve haftalık satış ve adet trendleri incelendiğinde en az satışın 6. ayda yapıldığını gözlemliyoruz.
 en çok satışın ise 3. ve 4. ayda yapılıyor. yani tahmin edilidiğinin aksine 11.ayda (kasım indrimleri) satışlar yüksek değil.
'''
###############
'''
Görev 3: Kategorisel ve Sayısal Analiz (%25)
1.	Ürün kategorilerine göre toplam satış miktarını ve her kategorinin tüm satışlar içindeki oranını hesaplayın.
2.	Müşterilerin yaş gruplarına göre satış eğilimlerini analiz edin. (Örnek yaş grupları: 18-25, 26-35, 36-50, 50+)
3.	Kadın ve erkek müşterilerin harcama miktarlarını karşılaştırın ve harcama davranışları arasındaki farkı tespit edin.
'''
## GOREV 3.1
kat_topalm_satis= satis_df.groupby("kategori")["toplam_satis"].sum()
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
satis_df['yas_grubu'] = satis_df['yas'].apply(lambda x: '18-25' if 18 <= x <= 25
                                  else '26-35' if 26 <= x <= 35
                                  else '36-50' if 36 <= x <= 50
                                  else '50+')
yas_grubu_satis =  satis_df.groupby("yas_grubu")["toplam_satis"].sum()

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
'''
YORUM:
Yaşlılar daha fazla satış yapmış. En fazla satış yapan kategori Elektronik hem adet olarak hem fiyat olarak daha fazla katkı sağlamış. 
'''
## GOREV 3.3
ort_cinsiyet_harcama = satis_df.groupby("cinsiyet")["harcama_miktari"].mean()

cinsiyet_toplam_harcama = satis_df.groupby("cinsiyet")["harcama_miktari"].sum()

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
sehir_toplam_harcama= musteri_df.groupby("sehir")["harcama_miktari"].sum().sort_values(ascending=False)
print(sehir_toplam_harcama)
# Gorsellestirme
plt.figure(figsize=(8, 6))
sehir_toplam_harcama.plot(kind='bar', color='blue', title="Şehir Bazlı Toplam Harcama Miktarı")
plt.ylabel("Harcama Miktarı")
plt.show()

## GOREV 4.2
urun_aylik_satis = satis_df.groupby(['ay', 'ürün_kodu'])['toplam_satis'].sum().reset_index()

urun_aylik_satis['satis_degisim'] = urun_aylik_satis.groupby('ürün_kodu')['toplam_satis'].pct_change()  #yuzdesel degisim hesapla
ortalama_satis_artisi = urun_aylik_satis.groupby('ürün_kodu')['satis_degisim'].mean()
print(ortalama_satis_artisi)



## GOREV 4.3

kat_aylik_satis = satis_df.groupby(['ay', 'kategori'])['toplam_satis'].sum().reset_index()
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

''' Görev 5: Ekstra (BONUS)
1.	Pareto Analizi: Satışların %80’ini oluşturan ürünleri belirleyin (80/20 kuralını uygulayın). Bu ürünleri grafikte gösterin.
2.	Cohort Analizi: Müşterilerin satın alım alışkanlıklarını analiz etmek için Pandas ile cohort analizi yapın. Örneğin, ilk kez satın alan müşterilerin tekrar alım oranlarını inceleyin.
3.	Tahmin Modeli: Aylık veya haftalık satış miktarlarını tahmin etmek için basit bir regresyon modeli (örneğin Linear Regression) uygulayın. sklearn kullanarak train/test split işlemi ile modeli eğitin ve modelin doğruluğunu ölçün.
'''

# Pareto Analizi
# Urun bazli toplan satisi hesapla
urun_satislari = satis_df.groupby("ürün_adi")["toplam_satis"].sum().sort_values(ascending=False).reset_index()

# cumulative yüzdeyi hesapla
urun_satislari['cumulative_percent'] = 100 * urun_satislari['toplam_satis'].cumsum() / urun_satislari['toplam_satis'].sum()

# Satışların %80'ini oluşturan ürünleri hesapla
pareto_urunleri = urun_satislari[urun_satislari['cumulative_percent'] <= 80]

fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar grafiği (toplam satışlar)
ax1.bar(urun_satislari['ürün_adi'], urun_satislari['toplam_satis'], color="skyblue", label="Satış Hacmi")
ax1.set_xlabel("Ürünler")
ax1.set_ylabel("Toplam Satış", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_xticklabels(urun_satislari['ürün_adi'], rotation=90)

# İkinci Y-ekseni (kümülatif yüzde)
ax2 = ax1.twinx()
ax2.plot(
    urun_satislari['ürün_adi'],
    urun_satislari['cumulative_percent'],
    color="red", marker="o", label="Kümülatif Yüzde"
)
ax2.axhline(y=80, color="green", linestyle="--", label="80% Eşiği")
ax2.set_ylabel("Kümülatif %", color="red")
ax2.tick_params(axis="y", labelcolor="red")

plt.title("Pareto Analizi - Satışların %80'ini Oluşturan Ürünler")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.tight_layout()
plt.show()

''' YORUM:
 Kalem Telefon Çanta Defter Fırın Mouse Su sisesi (ilk 7 ürün) toplam satışların %80nini karşılıyor. 
 Kalan iki ürün (Kulaklık ve bilgisayar) niş ürün diye tabir edebileceğimiz
doğru kampanya, fiyatlandırma veya pazarlama stratejileri ile daha büyük katkı sağlayabilecek ürünlerdir.

'''


