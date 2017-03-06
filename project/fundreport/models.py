from django.db import models


class Fund(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    market_summary = models.TextField()
    
    def __unicode__(self):
        return self.name

class Theme(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    target_PL = models.IntegerField()
    fund = models.ForeignKey('fundreport.Fund')
    region = models.ForeignKey('fundreport.Region')
    country = models.ForeignKey('fundreport.Country')
    asset_class = models.ForeignKey('fundreport.AssetClass')
    live = models.BooleanField() # Entry = True, Exit = False, see Rationale

    def __unicode__(self):
        return '%s - %s' %(self.name , self.fund)
    
    @property
    def live_rationale(self):
        try:
            rationale = Rationale.objects.get(theme=self, action='Entry')
        except:
            rationale = False
        return rationale

    @property
    def closed_rationale(self):
        try:
            rationale = Rationale.objects.get(theme=self, action='Exit')
        except:
            rationale = False
        return rationale


class Position(models.Model):
    # current P&L position for a Theme
    theme = models.OneToOneField('fundreport.Theme')
    var = models.IntegerField()
    cvar = models.IntegerField()
    LTD = models.IntegerField()
    SL = models.IntegerField()

    def __unicode__(self):
        return 'position for theme %s ' % self.theme.name


class Rationale(models.Model):
    #Rationale for either Entry or Exit of a Theme
    theme = models.ForeignKey('fundreport.Theme')
    action = models.CharField(max_length=10) #Entry or Exit 
    rationale = models.TextField()
    date = models.DateField()
  
    def __unicode__(self):
        return 'trade rationale for theme %s ' % self.theme.name

    
    
class Region(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    region = models.ForeignKey('fundreport.Region')

    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

    
class AssetClass(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    
    class Meta:
        verbose_name_plural = "Asset Classes"

    def __unicode__(self):
        return self.name


class FundValue(models.Model):
    fund = models.ForeignKey(Fund)
    date = models.DateField()
    value = models.IntegerField()

    def __unicode__(self):
        return '%d is the value of %s at %s' % (self.value, self.fund.name, self.date)

class IndexValue(models.Model):
    date = models.DateField()
    value = models.IntegerField()

    def __unicode__(self):
        return '%d is the value of the index at %s' % (self.value, self.date)
