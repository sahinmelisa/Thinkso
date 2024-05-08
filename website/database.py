import firebase_admin
from firebase_admin import credentials, db
import pyrebase
import json

from models import User, Note  # Bizim yarattığımız User ve Note classları (../website/models.py içine bakabilirsin detaylar için)

config = json.load(open("../config/db_config.json", "r"))   # Database config bilgileri. Bunlar githuba atılmaz o yüzden bilgiler ayrı dosyadan okunuyor
certificate_file_path = "../config/serviceAccountKey.json"  # aynı sebepten bu sertifika bilgisi de ayrı dosyadan okunuyor, bu dosyalar ../config klasöründe
                                                            # ve o config klasörü de .gitignore'a eklendi yanlışlıkla github'a pushlanmasın diye.
firebase = pyrebase.initialize_app(config)  # config dosyasını kullanarak firebase'i başlatıyor.


class Firebase:
    def __init__(self):
        global config
        self.config = config
        self.cred = credentials.Certificate(certificate_file_path)  # Credentials'a sertifikaların dosyasını veriyoruz
        firebase_admin.initialize_app(   # sertifikalı credentiallerimiz ile database URL'imize bağlanıyoruz (config dosyasında yazıyor url)
            self.cred,
            {
                "databaseURL": config["databaseURL"]
            },
        )
        self.ref_root = db.reference("/")  # Databaseimizin ana dizini (root)
        self.ref_notes = db.reference("/notes")  # ana dizin'in (root) içindeki "notes" klasörü (note'ları buraya kaydediyoruz)
        self.ref_users = db.reference("/users")  # ana dizin'in (root) içindeki "users" klasörü (user'ları buraya kaydediyoruz)

    def get_emails(self):              # tüm e-mail'leri çekmek için yazılmış bir fonksiyon, bu sayede kayıt olurken
        emails = []                    # girilen e posta db'deki e postalarla kıyaslanıp eğer mevcutsa "başka e posta
        users = self.ref_users.get()   # seç, bu mevcut" diye uyarı verilebilecek kolayca.
        for user in users:  # self.ref_users.get() ile "users" klasöründeki user bilgilerini (array of dict) çekiyor
            if user is not None:  # eğer user 'null' değil ise (0. indexte bir 'nulL' var sebebini henüz bilmiyorum)
                emails.append(user["email"])  # o user'in email bilgisini emails arrayine ekle
        return emails  # emails'i return et

    def get_last_id(self, user_or_note="user"):  # user_or_note'a "user" veya "note" ver, sana seçtiğin şey ne ise
        if user_or_note == "user":               # onun en son eklenen üyesinin id'sini return etsin.
            users = self.ref_users.get()  # tüm userları çekiyor
            if users is not None and users[-1] is not None:  # eğer user mevcutsa ve sonuncu user 'null' değilse
                return users[-1]["id"]  # o user'in id'sini return et.
            return 0  # diğer türlü 0 return et (ilk user olacağı için)
            # (belki baştaki null buradan kaynaklanıyor olabilir, buna bir ara 0 değil de -1 vermeyi denemek lazım
            # db'deki userları sildikten ve buna -1 verdikten sonra tekrar denemek lazım yine 0. user null olacak mı diye)
        else:
            notes = self.ref_notes.get()  # yukarıda user için yapılan her şeyi note için yapıyor
            if notes is not None and notes[-1] is not None:
                return notes[-1]["id"]
            return 0

    def add_user(self, user_dictionary):  # aşağıdaki diğer add_user fonksiyonunun overload hali dictionary desteklemesi için.
        self.add_user(user_dictionary["email"], user_dictionary["password"], user_dictionary["first_name"], user_dictionary["notes"])

    def add_note(self, note_dictionary):  # aşağıdaki diğer add_note fonksiyonunun overload hali dictionary desteklemesi için.
        self.add_note(note_dictionary["data"], note_dictionary["user_id"])

    def add_user(self, email, password, first_name, notes):  # asıl add_user fonksiyonu
        user_id = self.get_last_id("user")+1  # son user id'i alıp 1 ekliyor
        user = User(user_id, email, password, first_name, notes)  # yeni user objesi yaratıyor models.py/user classından
        self.ref_users.child(str(user_id)).set(user.__dict__)  # user'i user_id'siyle beraber db'ye kaydediyor

    def add_note(self, data, user_id):  # asıl add_note fonksiyonu
        note_id = self.get_last_id("note")+1  # son note id'i alıp 1 ekliyor
        note = Note(note_id, data, user_id)  # yeni note objesi yaratıyor models.py/note classından
        self.ref_notes.child(str(note_id)).set(note.__dict__)  # note'u note_id'siyle beraber db'ye kaydediyor

    def get_users(self):  # db'deki tüm userları return ediyor (array of dicts)
        return self.ref_users.get()

    def get_notes(self): # db'deki tüm note'ları return ediyor (array of dicts)
        return self.ref_notes.get()

