from django.db import models
import random
import string


def random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(256))


class ZipCode(models.Model):
    objects = None
    zip = models.CharField(max_length=5)
    type = models.CharField(max_length=4)
    decommissioned = models.BooleanField()
    primary_city = models.CharField(max_length=28)
    acceptable_cities = models.CharField(max_length=100)
    unacceptable_cities = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    area_codes = models.CharField(max_length=100)
    world_region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    irs_estimated_population = models.IntegerField()

    def __str__(self):
        return self.zip

    class Meta:
        ordering = ['zip']


class AgeRange(models.Model):
    age_range = models.CharField(max_length=100)

    def __str__(self):
        return self.age_range

    class Meta:
        ordering = ['age_range']


class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age_range = models.ForeignKey(AgeRange, on_delete=models.CASCADE)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s (%s)" % (self.last_name, self.first_name, self.zip_code)

    class Meta:
        ordering = ['last_name']


class Question(models.Model):
    question_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    question_id = models.CharField(max_length=256, default=random_id)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['pub_date']

    def images(self):
        return QuestionImage.objects.filter(question=self)


class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/questions/images')

    def __str__(self):
        return "%s (%s)" % (self.question, self.image)

    class Meta:
        ordering = ['question']


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.BooleanField()
    vote_id = models.CharField(max_length=256, default=random_id)
    vote_zip = models.CharField(max_length=5)
    vote_age = models.ForeignKey(AgeRange, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.question, self.vote)

    class Meta:
        ordering = ['question']


class VoterQuestion(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.voter, self.question.id)

    class Meta:
        ordering = ['voter']
