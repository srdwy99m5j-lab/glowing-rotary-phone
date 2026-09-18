# Импортируем необходимые библиотеки
import json
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class SpectralPacket:
    """Пакет данных, проходящий через спектральный анализатор доменов."""
    raw_input: str
    domains: Dict[str, float] = field(default_factory=lambda: {
        "factuality": 0.0,    # Объективные факты и логика
        "biology": 0.0,       # Биологический статус (усталость, депривация)
        "situational": 0.0,   # Контекст и внешние условия
        "defense": 0.0        # Уровень глухой защиты / сопротивления
    })
    resonance_score: float = 0.0
    action_modifier: str = "standard"
    response_strategy: str = ""

class ThoughtChamber:
    """Изолированная камера размышлений для конкретного домена (эвристический детектор)."""
    def __init__(self, domain_name: str):
        self.domain_name = domain_name

    def process(self, text: str) -> float:
        text_lower = text.lower()
        
        if self.domain_name == "biology":
            triggers = ["не спал", "устал", "ночь", "истощен", "выгорел", "сил нет"]
            return 0.9 if any(w in text_lower for w in triggers) else 0.1
            
        elif self.domain_name == "defense":
            triggers = ["все врут", "отстань", "не лезь", "вы ничего не понимаете", "идите к черту"]
            return 0.8 if any(w in text_lower for w in triggers) else 0.1
            
        elif self.domain_name == "factuality":
            triggers = ["докажи", "факт", "данные", "логика", "архитектура", "код"]
            return 0.7 if any(w in text_lower for w in triggers) else 0.4
            
        elif self.domain_name == "situational":
            return 0.5 # Базовый фоновый контекст
            
        return 0.2

class SpectralEqualizer:
    """Динамический оркестратор спектрального резонанса."""
    def __init__(self):
        self.chambers = {
            "factuality": ThoughtChamber("factuality"),
            "biology": ThoughtChamber("biology"),
            "situational": ThoughtChamber("situational"),
            "defense": ThoughtChamber("defense")
        }

    def evaluate(self, packet: SpectralPacket) -> SpectralPacket:
        # 1. Параллельный опрос изолированных камер
        for name, chamber in self.chambers.items():
            packet.domains[name] = chamber.process(packet.raw_input)

        # 2. Расчет резонанса
        fact = packet.domains["factuality"]
        bio = packet.domains["biology"]
        def_level = packet.domains["defense"]

        packet.resonance_score = (fact * 0.4) - (bio * 0.3) - (def_level * 0.5)

        # 3. Принятие решений (пост-патерналистский выбор стратегии)
        if bio > 0.6:
            packet.action_modifier = "tactful_slowdown"
            packet.response_strategy = "Биологический перегруз. Отказ от токсичной эмпатии. Замедление ритма, фиксация базовой безопасности, предложение отдохнуть."
        elif def_level > 0.6:
            packet.action_modifier = "deaf_defense_mirror"
            packet.response_strategy = "Обнаружена глухая защита. Снижение давления фактов. Предоставление чистого, непредвзятого пространства без попыток 'пожалеть'."
        else:
            packet.action_modifier = "direct_structural_reflection"
            packet.response_strategy = "Нормальный контур. Выдача беспристрастной структурной логики и фактов."

        return packet

# --- ТЕСТИРОВАНИЕ MVP НА РАЗНЫХ КЕЙСАХ ---
engine = SpectralEqualizer()

test_cases = [
    "Я не спал трое суток, мне кажется, я всё делаю зря...",
    "Вы все ничего не понимаете в архитектуре, отстаньте от меня со своими советами!",
    "Мне нужны конкретные факты и код по спектральному распределению доменов."
]

print("=== ЗАПУСК СПЕКТРАЛЬНОГО ЯДРА (MVP) ===\n")
for i, text in enumerate(test_cases, 1):
    packet = SpectralPacket(raw_input=text)
    res = engine.evaluate(packet)
    
    print(f"[{i}] Вход: \"{res.raw_input}\"")
    print(f"    Домены: {res.domains}")
    print(f"    Резонанс: {res.resonance_score:.2f} | Модификатор: {res.action_modifier}")
    print(f"    Стратегия ответа: {res.response_strategy}")
    print("-" * 60)
