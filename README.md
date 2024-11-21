### **RAPOR**  

**Müşteri ve Satış Verisi Analizi**  

#### **Amaç:**  
Bu projenin amacı, müşteri ve satış verilerini kullanarak:  
1. **Satış Trendlerini** analiz etmek.  
2. **Müşteri Davranışlarını** anlamak.  
3. **Ürün Kategorilerinin Performansını** değerlendirmek.  
4. Veri temizleme, zaman serisi analizi ve görselleştirme yöntemlerini uygulayarak, iş kararlarına yön verebilecek anlamlı içgörüler üretmektir.  

---  

#### **Veri Setleri:**  
1. **`satis_verisi_5000.csv`**: Satış detaylarını içerir.  
   - `musteri_id`, `kategori`, `fiyat`, `adet`, `tarih` sütunlarından oluşur.  
2. **`musteri_verisi_5000_utf8.csv`**: Müşteri bilgilerini içerir.  
   - `musteri_id`, `yas`, `cinsiyet`, `sehir`, `harcama_miktari` sütunlarından oluşur.  

---

#### **Kullanılan Yöntemler:**  

##### **1. Veri Temizleme ve Manipülasyon:**  
- **Eksik Veriler:** Eksik alanlar sütunun medyan değeri ile dolduruldu.  
- **Aykırı Değerler:**  
  - IQR yöntemiyle tespit edildi ve veri setindeki aşırı değerler düzenlendi.  
- **Dönüşümler:** Kategorik veriler sayısal forma dönüştürüldü.  

##### **2. Veri Birleştirme:**  
- Müşteri ve satış veri setleri, `musteri_id` sütunu üzerinde birleştirildi.  

##### **3. Zaman Serisi Analizi:**  
- Tarih bilgileri üzerinden haftalık ve aylık trendler çıkarıldı.  
- İlk ve son satış tarihleri belirlendi.  

##### **4. Kategorik ve Sayısal Analiz:**  
- Ürün kategorileri ve müşteri demografilerine göre satışlar incelendi.  
- Yaş gruplarına ve cinsiyete göre harcama alışkanlıkları analiz edildi.  

##### **5. Gelişmiş Veri Manipülasyonu:**  
- Şehir bazında müşteri harcamaları sıralandı.  
- Ürünlerin aylık büyüme oranları hesaplandı.  
- Kategori bazında satış trendleri görselleştirildi.  

---

#### **Elde Edilen Sonuçlar:**  

##### **1. Zaman Serisi Analizi:**  
- Satışlar, yılın 3. ve 4. aylarında zirveye ulaştı.  
- Kasım ayında (11. ay) beklenmedik bir düşüş gözlemlendi.  

##### **2. Demografik Analiz:**  
- 50 yaş üstü müşteriler en fazla harcamayı gerçekleştiren grup oldu.  
- Kadın müşterilerin ortalama harcama miktarının erkeklere göre daha yüksek olduğu belirlendi.  

##### **3. Kategori Performansı:**  
- Elektronik ürünler, satış miktarı ve gelir katkısı açısından en başarılı kategori oldu.  
- Modaya ait ürünlerin satışları diğer kategorilere göre daha düşük gerçekleşti.  

---

#### **Görselleştirme:**  
1. **Haftalık Satış Trendleri**:  
   - Zaman serisine göre haftalık satış eğilimleri çizgi grafiği ile görselleştirildi.  

2. **Kategori Bazında Satış Değişimleri**:  
   - Kategori performansları zaman içinde kıyaslandı ve artış/azalışlar grafiklerle sunuldu.  

---

#### **Yapılan Çalışmanın Önemi:**  
- **Satış Trendlerini Anlama:** İşletmeler, en yoğun satış yapılan dönemleri belirleyerek stok yönetimini optimize edebilir.  
- **Hedef Müşteri Kitlesini Tanımlama:** Yaş ve cinsiyete dayalı analizler, pazarlama stratejilerinin daha etkili hale gelmesine katkı sağlar.  
- **Kategori Performansı:** Hangi ürün kategorilerinin daha fazla gelir sağladığını görmek, ürün çeşitliliği kararlarını destekler.  

---

#### **Sonuç ve Öneriler:**  
1. Kasım ayındaki düşüş için özel promosyonlar veya kampanyalar uygulanabilir.  
2. 50 yaş üstü müşterilere yönelik özel ürün paketleri sunularak gelir artırılabilir.  
3. Elektronik kategorisine daha fazla yatırım yapılabilirken, moda kategorisinde çeşitlilik artırılabilir.  

#### **Teknik Yetkinliklerin Gösterilmesi:**  
Bu çalışma, Python ve veri analitiği kütüphanelerini kullanarak güçlü veri manipülasyon ve görselleştirme yetkinliklerini sergilemektedir.  

#### **Ek Notlar:**  
Bu rapor, müşteri ve satış analizi projelerinin benzer yapıdaki problemleri için bir rehber niteliğindedir. 
