from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from datetime import date

class AthleteProfile(models.Model):
    # Basic athlete information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True) 
    age = models.IntegerField(null=False) 
    sport = models.CharField(max_length=150) 

    # Funding related details
    goal = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # Financial goal for the athlete
    funds_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Automatically updated as pledges come in
    is_open = models.BooleanField(default=True)  # Is the campaign still accepting funds?

    # Transparency and impact features
    funding_breakdown = models.TextField(null=True)  
    achievements = models.TextField(null=True)  

    # Community and media
    image = models.URLField(blank=True, null=True) 
    video = models.URLField(blank=True, null=True)  
    progress_updates = models.TextField(blank=True, null=True)

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_athlete_profiles'
    )

    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.sport}"

    class Meta:
        ordering = ['-date_created']  # Orders profiles by most recent first

    def funds_remaining(self):
        # Ensure funds_remaining returns a minimum of 0 if funds_raised exceeds the goal
        return max(self.goal - self.funds_raised, 0)
    
    def clean(self):
        # Ensure age is within the range 5 to 18
        if not (5 <= self.age <= 18):
            raise ValidationError({'age': 'Age must be between 5 and 18.'})

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super(AthleteProfile, self).save(*args, **kwargs)


class Pledge(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    is_fulfilled = models.BooleanField(default=True)

    athlete_profile = models.ForeignKey(
    'AthleteProfile',
    on_delete=models.CASCADE,
    related_name='pledges',
    # null=True,  # Allow null values
    # blank=True  # Allow blank values
)


    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )

    def __str__(self):
        return f"{self.supporter} pledged {self.amount} to {self.athlete_profile}"

    def clean(self):
        if not self.athlete_profile:
            raise ValidationError({'athlete_profile': 'An athlete profile is required.'})
        if not self.athlete_profile.is_open:
            raise ValidationError({'athlete_profile': 'Pledging is not allowed on closed campaigns.'})
        if self.amount <= 0:
            raise ValidationError({'amount': 'Pledge amount must be greater than zero.'})



    def save(self, *args, **kwargs):
        self.clean()
        with transaction.atomic():  # Ensure atomic database updates
            super(Pledge, self).save(*args, **kwargs)
            if self.athlete_profile:
                self.athlete_profile.funds_raised += self.amount
                self.athlete_profile.save()
        print(f"Updating funds for AthleteProfile {self.athlete_profile.id}")



    def check_for_badges(self):
        total_pledged = Pledge.objects.filter(supporter=self.supporter).aggregate(models.Sum('amount'))['amount__sum']
        try:
            top_donor_badge = Badge.objects.get(name="Top Donor")
        except Badge.DoesNotExist:
            return

        if total_pledged >= 100:
            top_donor_badge.award_badge(self.supporter)
        self.check_for_first_donor_badge()

    def check_for_first_donor_badge(self):
        if Pledge.objects.filter(athlete_profile=self.athlete_profile).count() == 1:
            try:
                first_donor_badge = Badge.objects.get(name="First Donor")
            except Badge.DoesNotExist:
                return

            first_donor_badge.award_badge(self.supporter)




class ProgressUpdate(models.Model):
    athlete_profile = models.ForeignKey(
        'AthleteProfile',  # Links the update to the athlete
        on_delete=models.CASCADE,
        related_name='updates'
    )
    title = models.CharField(max_length=200)  # Title of the update
    content = models.TextField()  # The body of the update (e.g., progress, results, news)
    date_posted = models.DateTimeField(auto_now_add=True)  # Timestamp for the update
    
    def __str__(self):
        return f"Update: {self.title} for {self.athlete_profile}"

class Badge(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    image = models.URLField(blank=True)
    date_awarded = models.DateField(null=True, blank=True)  
    
    # Linking badges to users (donors)
    supporters = models.ManyToManyField(
        get_user_model(),
        related_name='badges',
        blank=True
    )

    # date_awarded = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    def award_badge(self, user):
    # """Award badge to the user based on specific conditions."""
        if user not in self.supporters.all():
            self.supporters.add(user)
            self.date_awarded = date.today()  # Use only the date part
            self.save()
            print(f"Awarded {self.name} badge to {user}.")