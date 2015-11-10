from django.db import models

class Department(models.Model):
    code = models.FloatField(primary_key=True, db_column='coddepar')
    name = models.CharField(max_length=60, db_column='nomdepar')

    class Meta:
        managed = False
        db_table = 'departamentos'

class Section(models.Model):
    department = models.ForeignKey(Department, db_column='coddepar')
    code = models.FloatField(primary_key=True, db_column='codseccion')
    name = models.CharField(max_length=100, blank=True, null=True, db_column='nomseccion')

    class Meta:
        managed = False
        db_table = 'secciones'

class Contributor(models.Model):
    charter = models.CharField(primary_key=True, max_length=15, db_column='ctrcedula')    
    name = models.CharField(max_length=120, blank=True, null=True, db_column='ctrnombre')        
    email = models.CharField(max_length=60, blank=True, null=True, db_column='ctremail')
    state = models.CharField(max_length=20, blank=True, null=True, db_column='ctrestado')

    class Meta:
        managed = False
        db_table = 'contribuyentes'

class Employee(models.Model):
    contributor = models.ForeignKey('Contributor', db_column='bicodcon')
    code = models.CharField(primary_key=True, max_length=2, db_column='biprvcodigo')    
    department = models.FloatField(blank=True, null=True, db_column='bicoddep')
    section = models.FloatField(blank=True, null=True, db_column='bicodsec')    

    class Meta:
        managed = False
        db_table = 'bicondep'

