from app.services.config_service import ThresholdService
from app.services.utils import Alert

tv = ThresholdService()
class Decision:
    @staticmethod
    def simple(topic, value):
        if value > tv.get_threshold(topic)['upper'] or value < tv.get_threshold(topic)['lower']:
            return Alert(topic, value)