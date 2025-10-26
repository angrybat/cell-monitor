import dagger

from .charge_guru import ChargeGuru

@dagger.object_type
class CellMonitor:
    @dagger.function
    def charge_guru(self) -> ChargeGuru:
        return ChargeGuru()