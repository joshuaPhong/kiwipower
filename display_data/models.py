from django.db import models


class ContinentConsumption(models.Model):
    """
    this model will contain the data for the power consumption of each
    continent or continental group
    """
    year = models.IntegerField()
    world = models.FloatField()
    oecd = models.FloatField()
    brics = models.FloatField()
    europe = models.FloatField()
    north_america = models.FloatField()
    latin_america = models.FloatField()
    asia = models.FloatField()
    pacific = models.FloatField()
    africa = models.FloatField()
    middle_east = models.FloatField()
    cis = models.FloatField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.year)


class CountryConsumption(models.Model):
    """
    this model will contain the data for the power consumption of each country
    """

    year = models.IntegerField()
    china = models.IntegerField()
    usa = models.IntegerField()
    belgium = models.IntegerField()
    croatia = models.IntegerField()
    france = models.IntegerField()
    germany = models.IntegerField()
    italy = models.IntegerField()
    netherlands = models.IntegerField()
    poland = models.IntegerField()
    portugal = models.IntegerField()
    romania = models.IntegerField()
    spain = models.IntegerField()
    sweden = models.IntegerField()
    uk = models.IntegerField()
    norway = models.IntegerField()
    turkey = models.IntegerField()
    kazakhstan = models.IntegerField()
    russia = models.IntegerField()
    ukraine = models.IntegerField()
    uzbeckistan = models.IntegerField()
    argentina = models.IntegerField()
    canada = models.IntegerField()
    chile = models.IntegerField()
    colubia = models.IntegerField()
    mexico = models.IntegerField()
    venezuela = models.IntegerField()
    indonesia = models.IntegerField()
    japan = models.IntegerField()
    malaysia = models.IntegerField()
    south_korea = models.IntegerField()
    taiwan = models.IntegerField()
    thailand = models.IntegerField()
    india = models.IntegerField()
    australia = models.IntegerField()
    new_zealand = models.IntegerField()
    algeria = models.IntegerField()
    egypt = models.IntegerField()
    nigeria = models.IntegerField()
    south_africa = models.IntegerField()
    kuwait = models.IntegerField()
    saudi_arabia = models.IntegerField()
    u_a_e = models.IntegerField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.year)


class NonRenewablesTotalPowerGenerated(models.Model):
    mode_of_generation = models.CharField(max_length=100)
    contribution_twh = models.FloatField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.mode_of_generation)


class RenewablesPowerGenerated(models.Model):
    year = models.IntegerField()
    hydro = models.FloatField()
    biofuels = models.FloatField()
    solar = models.FloatField()
    geo_thermal = models.FloatField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.year)


class RenewableTotalPowerGenerated(models.Model):
    mode_of_generation = models.CharField(max_length=100)
    contribution_twh = models.FloatField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.mode_of_generation)


class TopTwentyRenewableCountries(models.Model):
    country = models.CharField(max_length=100)
    hydro = models.FloatField()
    biofuels = models.FloatField()
    solar = models.FloatField()
    geo_thermal = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        """
        This will show the year in the admin. Instead of showing object 1...n
        """
        return str(self.country)
