import json
import datetime

class SupportEngine:
    def __init__(self):
        self.storage_file = "support_logs.json"
        # Profesyonel Analiz Sözlüğü
        self.priority_map = {
            "CRITICAL": {"words": ["çalışmıyor", "hata", "acil", "bozuk", "erişim"], "sla": 2},
            "FINANCIAL": {"words": ["iade", "fatura", "ödeme", "kart", "para"], "sla": 24},
            "TECHNICAL": {"words": ["şifre", "ayarlar", "güncelleme", "kurulum"], "sla": 48}
        }

    def analyze_and_create(self, user_id, message):
        msg_lower = message.lower()
        level = "NORMAL"
        resolution_time = 72 # Standart çözüm süresi (saat)

        # Akıllı Öncelik ve Çözüm Süresi Analizi
        for status, data in self.priority_map.items():
            if any(word in msg_lower for word in data["words"]):
                level = status
                resolution_time = data["sla"]
                break

        ticket = {
            "ticket_id": f"REQ-{datetime.datetime.now().strftime('%M%S')}",
            "user": user_id,
            "content": message,
            "status": level,
            "sla_hours": resolution_time,
            "timestamp": str(datetime.datetime.now())
        }
        
        self._save_to_database(ticket)
        return ticket

    def _save_to_database(self, data):
        # Veriyi profesyonel JSON formatında kalıcı hale getirir
        with open(self.storage_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

# --- SİSTEMİ ÇALIŞTIR ---
engine = SupportEngine()

print("--- Smart Logic Support Engine Active ---")
request = input("Lütfen talebinizi yazın: ")
result = engine.analyze_and_create("User_01", request)

print(f"\n[ANALİZ SONUCU]")
print(f"Durum: {result['status']}")
print(f"Hedef Çözüm Süresi: {result['sla_hours']} Saat")
print(f"Takip Numarası: {result['ticket_id']}")