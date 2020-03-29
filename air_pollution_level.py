class AirPollutionLevel:
    def __init__(self, good, moderate, unhealthy, poor, very_unhealthy, hazardous):
        self.good = good
        self.moderate = moderate
        self.unhealthy = unhealthy
        self.poor = poor
        self.very_unhealthy = very_unhealthy
        self.hazardous = hazardous


city_aqi = AirPollutionLevel("""
Air quality is considered satisfactory, and air pollution poses little or no risk
""",
"""Air quality is acceptable; however, for some pollutants there may be a moderate
health concern for a very small number of people who are unusually sensitive to air pollution.
""",
"""Members of sensitive groups may experience health effects. The general public is not likely to be affected.
""",
"""Everyone may begin to experience health effects; members of sensitive groups may
experience more serious health effects
""",
"""Health warnings of emergency conditions. The entire population is more likely to be affected.
""",
"""Health alert: everyone may experience more serious health effects
"""
)
