import random

from django.contrib.localflavor.us.models import USStateField
from django.contrib.localflavor.us.us_states import US_STATES
from django.db import models


class Group(models.Model):
    """ Guests are invited in groups """

    RESPONSE_CHOICES = (
        (0, 'No Response'),
        (1, 'Attending'),
        (2, 'Not Attending'),
    )
    PARTY_CHOICES = (
        (0, 'Bride'),
        (1, 'Groom'),
    )

    name = models.CharField(max_length=80)
    response = models.IntegerField(choices=RESPONSE_CHOICES, default=0)
    party = models.IntegerField(choices=PARTY_CHOICES, default=0)
    code = models.CharField(max_length=6, editable=False)

    # Contact Information
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    address = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = USStateField(choices=US_STATES, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    # Admin Only
    number_guests = models.PositiveSmallIntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)

    announcement_required = models.BooleanField()
    announcement_sent = models.DateField(blank=True, null=True)

    invitation_required = models.BooleanField()
    invitation_sent = models.DateField(blank=True, null=True)

    thank_you_required = models.BooleanField()
    thank_you_sent = models.DateField(blank=True, null=True)

    gift_received = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('apps.rsvp.views.rsvp_detail', (), {
            'code': self.code,
        })

    def save(self, *args, **kwargs):
        if self.invitation_required:
            self.announcement_required = True
        if self.gift_received:
            self.thank_you_required = True
        if not self.code:
            self.code = ''.join(random.sample('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', 6))
        super(Group, self).save(*args, **kwargs)

    def full_address(self):
        return "%s %s, %s %s" % (self.address, self.city, self.state, self.zipcode)

    class Meta:
        ordering = ('name', )


class Guest(models.Model):
    """ Capture information about each guest """

    MEAL_CHOICES = (
        (0, 'Meat'),
        (1, 'Fish'),
        (2, 'Veggie'),
    )

    group = models.ForeignKey(Group)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    meal = models.IntegerField(choices=MEAL_CHOICES, default=0)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ('last_name', 'first_name', )
