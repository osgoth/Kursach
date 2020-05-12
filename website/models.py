from django.db import models
from datetime import datetime, date


gender_choise = [("male", "мужской"), ("female", "женский")]
Categories = [
    ("internet", "internet"),
    ("outdoor", "outdoor"),
    ("indoor", "indoor"),
    ("transport", "transport"),
    ("media", "media"),
    ("polygraphy", "polygraphy"),
]
Types = [
    ("targeting", "targeting"),
    ("banners", "banners"),
    ("instagram", "instagram"),
    ("youtube", "youtube"),
    ("website", "website"),
    ("arch", "arch"),
    ("poster", "poster"),
    ("backlight", "backlight"),
    ("billboard", "billboard"),
    ("citylight", "citylight"),
    ("scroll", "scroll"),
    ("university", "university"),
    ("shopping center", "shopping center"),
    ("cinema", "cinema"),
    ("elevator", "elevator"),
    ("parking", "parking"),
    ("bus", "bus"),
    ("trolleybus", "trolleybus"),
    ("tram", "tram"),
    ("autobrending", "autobrending"),
    ("train", "train"),
    ("tv", "tv"),
    ("radio", "radio"),
    ("video", "video"),
    ("photo", "photo"),
    ("newspaper", "newspaper"),
    ("flyer", "flyer"),
    ("bussiness card", "bussiness card"),
    ("sticker", "sticker"),
    ("calendar", "calendar"),
]


class Customers(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, unique=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length = 15, choices = gender_choise, default="male")
    phone = models.CharField(max_length = 13, unique = True, null=True)  
    reg_date = models.DateField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Customers"
        verbose_name_plural = "Customers"
        db_table = "Customers"
        managed = True

    def update(self, post):
        for pkey in post:
            for obkey in dict(self.__dict__):
                if pkey == obkey:
                    setattr(self, pkey, post[pkey])
        self.birthday = date(int(post["year"]), int(post["month"]), int(post["day"]))
        self.save()


class Departments(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    cabinet = models.CharField(max_length=50)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Departments"
        verbose_name_plural = "Departments"
        db_table = "Departments"
        managed = True


class Employee(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length = 15, choices = gender_choise, default="male")
    phone = models.CharField(max_length = 13, unique = True)
    position = models.CharField(max_length =50)
    status = models.CharField(max_length =50, default='active')
    reg_date = models.DateField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employee"
        db_table = "Employee"
        managed = True


class Services(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=Categories)
    types = models.CharField(max_length=50, choices=Types)
    description = models.CharField(max_length=256)
    picture = models.CharField(max_length=50)
    price = models.CharField(max_length=13)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"
        db_table = "Services"
        managed = True


class Deals(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=100, null=True)
    final_date = models.DateField(null=True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Deals"
        verbose_name_plural = "Deals"
        db_table = "Deals"
        managed = True

    def update(self, post):
        for pkey in post:
            for obkey in dict(self.__dict__):
                if pkey == obkey:
                    setattr(self, pkey, post[pkey])
        self.final_date = date(int(post["year"]), int(post["month"]), int(post["day"]))
        self.save()


class Requests(models.Model):
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    reg_date = models.DateField(max_length=50)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Requests"
        verbose_name_plural = "Requests"
        db_table = "Requests"
        managed = True