import re

from django.db import models

def slugify(string):
	slug = re.sub('[^\w+]', '-', string)
	return slug.lower()

def createShortCode(string, len):
	sc = ""
	for i in string.lower().split():
		if len == 0:
			sc += i[0]
		else:
			sc = "%s%s%s" % (i[0], i[1], i[2])
	return sc

class Property(models.Model):
	name = models.CharField(max_length=300)
	reference = models.CharField(max_length=300, unique=True)
	house = models.CharField(max_length=200)
	street = models.CharField(max_length=220)
	city = models.ForeignKey('City')
	postcode = models.CharField(max_length=15)
	property_type = models.ForeignKey('PropertyChoice')
	sale_type = models.ForeignKey('SaleStatus')
	furnished = models.NullBooleanField()
	price = models.FloatField()
	rooms = models.IntegerField()
	bathrooms = models.IntegerField()
	garden = models.NullBooleanField()
	garden_type = models.ForeignKey('GardenChoice')
	pool = models.BooleanField()
	parking = models.BooleanField()
	parking_type = models.ForeignKey('ParkingChoice')
	property_desc = models.TextField()
	location_desc = models.TextField()
	schedule = models.ForeignKey('Schedule')
	floorplan = models.ForeignKey('FloorPlan', default='None')
	featured = models.BooleanField()
	#image_gallery = models.ForeignKey(Gallery, default='None')

	def __unicode__(self):
		return "%s for %s " % (self.reference, self.name)
	
	def get_city_name(self):
		return self.city.name
	
	def get_property_type(self):
		return "A %s Property" % self.property_type
	
	class Meta:
		verbose_name = "Property"
		verbose_name_plural = "Properties"

class FeaturedProperty(models.Model):
	property = models.ForeignKey('Property')
	

	def __unicode__(self):
		return self.property

	class Meta:
		verbose_name = "Featured Property"
		verbose_name_plural = "Featured Properties"


class PropertyChoice(models.Model):
	option = models.CharField(max_length=150, unique=True)
	value = models.CharField(max_length=150,  unique=True)

	def __unicode__(self):
		return self.option

	class Meta:
		verbose_name = "Property Choice"
		verbose_name_plural = "Property Choices"

class SaleStatus(models.Model):
	option = models.CharField(max_length=150, unique=True)
	value = models.CharField(max_length=150,  unique=True)

	def __unicode__(self):
		return self.option

	class Meta:
		verbose_name = "Sales Status"
		verbose_name_plural = "Sales Status"

class GardenChoice(models.Model):
	option = models.CharField(max_length=150, unique=True)
	value = models.CharField(max_length=150,  unique=True)

	def __unicode__(self):
		return self.option

	class Meta:
		verbose_name = "Garden Choice"
		verbose_name_plural = "Garden Choices"

class ParkingChoice(models.Model):
	option = models.CharField(max_length=150, unique=True)
	value = models.CharField(max_length=150,  unique=True)

	def __unicode__(self):
		return self.option

	class Meta:
		verbose_name = "Parking Choice"
		verbose_name_plural = "Parking Choices"
	
class Country(models.Model):
	name = models.CharField(max_length=150)
	slug = models.CharField(max_length=200, blank=True)
	short_code = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.name)
			self.short_code = createShortCode(self.name, 0)
			for sc in Country.objects.all():
				print sc.short_code
				if self.short_code == sc.short_code:
					print " Short Code : %s exists" % self.short_code
					self.short_code = createShortCode(self.name, 3)
		super(Country, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Country"
		verbose_name_plural = "Countries"

class City(models.Model):
	country = models.ForeignKey('Country')
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return "%s in %s" % (self.name, self.country)

	class Meta:
		verbose_name = "City"
		verbose_name_plural = "Cities"

class Schedule(models.Model):
    name = models.CharField(default='None', blank=True, null=True, max_length=50)
    schedule = models.FileField(default='None', blank=True, null=True, upload_to='property/schedule/')

    def __unicode__(self):
    	return self.name

    class Meta:
		verbose_name = "Schedule"
		verbose_name_plural = "Schedules"

class FloorPlan(models.Model):
    name = models.CharField(default='None', blank=True, null=True, max_length=50)
    floorplan = models.FileField(default='None', blank=True, null=True, upload_to='property/floorplan/')

    def __unicode__(self):
    	return "%s plan" % (self.name)

    class Meta:
		verbose_name = "Floor Plan"
		verbose_name_plural = "Floor Plans"
