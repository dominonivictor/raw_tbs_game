class Stats:
    def __init__(self, stats):
        self.max_hp: int = stats.get("max_hp", stats.get("hṕ"))
        self.hp: int = stats.get("hp")
        self.max_ap: int = stats.get("max_ap")
        self.ap: int = stats.get("ap")
        self.at: int = stats.get("at")
        self.df: int = stats.get("df")
        self.sp: int = stats.get("sp")

