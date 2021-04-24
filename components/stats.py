class Stats:
    def __init__(self, stats):
        self.max_hp: int = stats.get("max_hp")
        self.hp: int = stats.get("hp")
        self.at: int = stats.get("at")
        self.df: int = stats.get("df")
        self.sp: int = stats.get("sp")
        self.max_ap: int = stats.get("max_ap")
        self.ap: int = stats.get("ap")

