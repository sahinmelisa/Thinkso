from database import Firebase
import json


def get_user_info():  # used for getting custom user info, REPLACE THIS WITH A FLASK PAGE
    email = input("enter email: ")
    password = input("enter password: ")
    first_name = input("enter name: ")
    notes = list()
    return {
        "email": email,
        "password": password,
        "first_name": first_name,
        "notes": notes
    }


def get_note_info():  # used for getting custom note info, REPLACE THIS WITH A FLASK PAGE
    note_data = input("Note Data : ")
    user_id = input("Used id : ")
    return {
        "data": note_data,
        "user_id": user_id
    }


if __name__ == "__main__":

    firebase = Firebase()  # DB Yönetmek için Firebase objesi yaratır, '../website/database.py' içine gidip Firebase class'ını inceleyebilirsin detaylı bilgiler için.

    user_info = get_user_info()  # yukarıda tanımladığım bir method, kullanıcıdan email/şifre/name alıyor ve dictionary olarak döndürüyor
    firebase.add_user(user_info["email"], user_info["password"], user_info["first_name"], user_info["notes"])  # oto id yarattı + firebase'e ekledi

    note_info = get_note_info()  # yukarıda tanımladığım bir method, kullanıcıdan note_data/user_id alıyor ve dictionary olarak döndürüyor
    firebase.add_note(note_info["data"], note_info["user_id"])  # oto id ve date yarattı ve firebase'e ekledi

    print("\nUSERS")  # DB'den userleri alıp yazdırıyor alt satır.
    print(json.dumps(firebase.get_users(), indent=4))  # tüm kullanıcıları çekiyor firebase'ten (array of dicts)

    print("\nNOTES") # DB'den note'ları alıp yazdırıyor alt satır.
    print(json.dumps(firebase.get_notes(), indent=4))  # tüm note'ları çekiyor firebase'ten (array of dicts)
    # dikkat: henüz çözemediğim bir sebepten dolayı users[0] ve notes[0] 'null' geliyor fakat 0. indexten sonrası normal geliyor
    # örnek çıktı resmine bakabilirsin

    emails = firebase.get_emails()  # tüm e-mail'leri çekmek için yazılmış bir fonksiyon, bu sayede kayıt olurken girilen
    print("\nEMAILS:")              # e posta db'deki e postalarla kıyaslanıp eğer mevcutsa 'başka e posta seç, bu mevcut'
    print(emails)                   # diye uyarı verilebilecek kolayca.

