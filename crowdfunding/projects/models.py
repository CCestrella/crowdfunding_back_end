from django.db import models
from django.contrib.auth import get_user_model


class AthleteProfile(models.Model):
    # Basic athlete information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)  # Athlete's background and story
    age = models.IntegerField()  # Athlete's age
    sport = models.CharField(max_length=150)  # Type of sport (e.g., boxing, swimming)

    # Funding related details
    goal = models.DecimalField(max_digits=10, decimal_places=2)  # Financial goal for the athlete
    funds_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Automatically updated as pledges come in
    is_open = models.BooleanField(default=True)  # Is the campaign still accepting funds?

    # Transparency and impact features
    funding_breakdown = models.TextField(null=True)  # Explain how funds will be used (e.g., travel, equipment)
    achievements = models.TextField(null=True)  # Athlete's achievements and accolades

    # Community and media
    image = models.URLField(blank=True, null=True)  # URL to athlete's image
    video = models.URLField(blank=True, null=True)  # Optional video introducing the athlete
    progress_updates = models.TextField(blank=True, null=True)  # Updates on the athlete's progress

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
        return self.goal - self.funds_raised



class Pledge(models.Model):
    amount = models.IntegerField()  # The amount of money the donor is pledging
    comment = models.TextField(blank=True)  # An optional comment from the donor (extended length)
    anonymous = models.BooleanField(default=False)  # Whether the donor wants to stay anonymous
    is_fulfilled = models.BooleanField(default=True)  # Tracks whether the pledge has been completed
    
    # Linking the pledge to an athlete
    athlete_profile = models.ForeignKey(
        'AthleteProfile',  # This links the pledge to a specific athlete
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    
    # Linking the pledge to the user (supporter)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    
    def __str__(self):
        return f"{self.supporter} pledged {self.amount} to {self.athlete_profile}"


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
    name = models.CharField(max_length=100)  # Badge name (e.g., "Top Supporter", "First Donor")
    description = models.TextField()  # Description of what this badge represents
    image = models.URLField(blank=True)  # Optional URL to an image representing the badge
    
    # Linking badges to users (donors)
    supporters = models.ManyToManyField(
        get_user_model(),
        related_name='badges',
        blank=True
    )
    
    def __str__(self):
        return self.name
