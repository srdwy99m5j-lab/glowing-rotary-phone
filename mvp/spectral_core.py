# Чистый модуль спектрального ядра — ввод без вывода (без CLI/веб/тестов)
import re
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class SpectralPacket:
    """Пакет данных, проходящий через спектральный анализатор доменов.

    Все значения доменов ограничены диапазоном [0.0, 1.0].
    """
    raw_input: str
    domains: Dict[str, float] = field(default_factory=lambda: {
        "factuality": 0.0,
        "biology": 0.0,
        "situational": 0.0,
        "defense": 0.0,
    })
    resonance_score: float = 0.0
    action_modifier: str = "standard"
    response_strategy: str = ""

    def __post_init__(self):
        for k in ("factuality", "biology", "situational", "defense"):
            self.domains.setdefault(k, 0.0)
            try:
                v = float(self.domains[k])
            except (TypeError, ValueError):
                v = 0.0
            self.domains[k] = max(0.0, min(1.0, v))


class ThoughtChamber:
    """Изолированная камера размышлений для конкретного домена (эвристический детектор)."""

    def __init__(self, domain_name: str):
        self.domain_name = domain_name

    def process(self, text: str) -> float:
        text_lower = (text or "").lower()

        def any_trigger(triggers):
            for trigger in triggers:
                pattern = r"\b" + re.escape(trigger) + r"\b"
                if re.search(pattern, text_lower):
                    return True
            return False

        if self.domain_name == "biology":
            triggers = ["не спал", "устал", "ночь", "истощен", "выгорел", "сил нет", "без сил"]
            return 0.9 if any_trigger(triggers) else 0.1

        if self.domain_name == "defense":
            triggers = ["все врут", "отстань", "не лезь", "вы ничего не понимаете", "идите к черту", "оставьте меня"]
            return 0.85 if any_trigger(triggers) else 0.1

        if self.domain_name == "factuality":
            triggers = ["докажи", "факт", "данные", "логика", "архитектура", "код", "конкретно", "подтверждение"]
            return 0.9 if any_trigger(triggers) else 0.4

        if self.domain_name == "situational":
            triggers = ["сейчас", "сегодня", "на улице", "контекст", "место", "ситуация"]
            return 0.7 if any_trigger(triggers) else 0.5

        return 0.2


class SpectralEqualizer:
    """Динамический оркестратор спектрального резонанса."""

    def __init__(self):
        self.chambers = {
            "factuality": ThoughtChamber("factuality"),
            "biology": ThoughtChamber("biology"),
            "situational": ThoughtChamber("situational"),
            "defense": ThoughtChamber("defense"),
        }

    @staticmethod
    def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    def evaluate(self, packet: SpectralPacket) -> SpectralPacket:
        """Заполнить packet.domains и вычислить resonance_score и стратегию.

        Функция полностью автономна и не выполняет сетевых вызовов.
        """
        for name, chamber in self.chambers.items():
            packet.domains[name] = chamber.process(packet.raw_input)

        factuality = float(packet.domains.get("factuality", 0.0))
        biology = float(packet.domains.get("biology", 0.0))
        defense = float(packet.domains.get("defense", 0.0))
        situational = float(packet.domains.get("situational", 0.0))

        raw_score = (factuality * 0.45) - (biology * 0.35) - (defense * 0.5) + (situational * 0.1)
        packet.resonance_score = self._clamp(raw_score, -1.0, 1.0)

        if biology > 0.6:
            packet.action_modifier = "tactful_slowdown"
            packet.response_strategy = (
                "Биологический перегруз: избегаем токсичной эмпатии. "
                "Замедляем темп, предлагаем отдых/перерыв и краткие, понятные инструкции."
            )
        elif defense > 0.6:
            packet.action_modifier = "deaf_defense_mirror"
            packet.response_strategy = (
                "Обнаружена глухая защита: снижаем давление фактов. "
                "Используем зеркальное отражение, предложим выбор и варианты действий с мягким тоном."
            )
        else:
            packet.action_modifier = "direct_structural_reflection"
            packet.response_strategy = "Нормальный контур: выдача беспристрастной структурной логики и фактов."

        return packet


def analyze_text(text: str) -> None:
    """Обработка входного текста без возврата или внешней публикации результатов.

    Функция выполняет локальный анализ и не возвращает значения и не выполняет
    сетевых или логирующих действий. Используйте отдельный модуль, если
    требуется экспорт/сериализация результатов.
    """
    packet = SpectralPacket(raw_input=text or "")
    # выполняем анализ локально и целенаправленно НЕ возвращаем результат
    SpectralEqualizer().evaluate(packet)
    return None
