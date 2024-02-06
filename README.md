# WordWeave
Reddit style news site

[live-site](https://word-weave-eb35426ae0cb.herokuapp.com/)

## Technologies Used

* GitHub – storage and deployment
* Sublime Text - Editor

### Languages Used

Python, CSS, Java Script

### Frameworks, Libraries & Programs Used

Github

## User Experience

### Target Audience


### User stories

## Design


### Wireframes


#### Mobile

#### Desktop

## Features 

### Existing Features

### Features Left to Implement

### Accessibility

#### Fonts and Font Sizes


#### Colors


#### Structural HTML


## Testing


#### Lighthouse Test


#### Jigsaw CSS Validator


#### W3C Validator


#### Accessibility
The result of the WAVE Web Accessibility Evaluation Tool shows .... Errors.


#### JS Hint


### Manual Testing

### Automatic Testing
Unittests

### Unfixed Bugs


### Fixed Bugs
### The Situation:
When a user deletes their profile, all threads, comments and votes the user has made on the platform should get deleted with it. 
The current set up is as followed:

```

class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"The title of this thread is {self.title}"

    # Creating the slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def up_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.thread_votes.filter(user=user).exists():
            self.votes = F('votes') + 1
            self.save()
            self.thread_votes.create(user=user, value=1)
        elif self.thread_votes.get(user=user, thread_id=self.id).value == -1:
            self.votes = F('votes') + 2
            self.save()
            vote = self.thread_votes.get(user=user, thread_id=self.id)
            vote.value = 1
            vote.save()
        # Here need to come an exception that gets handle to inform the user that they have already voted.

    def down_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.thread_votes.filter(user=user).exists():
            self.votes = F('votes') - 1
            self.save()
            self.thread_votes.create(user=user, value=-1)
        elif self.thread_votes.get(user=user, thread_id=self.id).value == 1:
            self.votes = F('votes') - 2
            self.save()
            vote = self.thread_votes.get(user=user, thread_id=self.id)
            vote.value = -1
            vote.save()

class ThreadVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_votes")

```

### The Problem:
After Deleting a User, their votes (as instances of the Vote Model) get deleted, but the value "votes" of the Thread itselfs is never. Since the Votes for each thread is are the Thread.values that get displayed. The Votes in the website are never updated.

### Possible solutions:
The idea is to write a function for the ThreadVote Model that adjusts the value of the belonging thread, everytime one ThreadVote gets deleted.

I tried this by overwriting the delete() function.

```

class ThreadVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_votes")

    def delete(self, *args, **kwargs):
        # Update the thread's vote count before deleting the vote instance
        if self.value == 1:
            self.thread.votes = F('votes') - 1
        elif self.value == -1:
            self.thread.votes = F('votes') + 1

        self.thread.save()
        super().delete(*args, **kwargs)

```

This wasn't working, because as it turns out, for results of a cascading delete an overwritten delete function is not used.. The Django Docs suggest to use pre_delete, which works perfectly and solved the problem:

```

@receiver(pre_delete, sender=ThreadVote)
def update_thread_votes(sender, instance, **kwargs):
    if instance.value == 1:
        instance.thread.votes = F('votes') - 1
    elif instance.value == -1:
        instance.thread.votes = F('votes') + 1
    instance.thread.save()

```

## Deployment


### Local Development

#### How to Clone

1. Click the code button and copy the link of your preferred clone option.
2. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
3. Type 'git clone' into the terminal, paste the link you copied in step 1 and press enter.

More detailed steps are provided by github: [github guide to clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)


#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project.
3. Click the Fork button in the top right corner.

## Credits
* user story structure: https://community.atlassian.com/t5/Jira-Content-Archive-questions/Default-Description-Text-on-Create/qaq-p/2359579
* log in screen: https://learndjango.com/tutorials/django-login-and-logout-tutorial
* sign up in django: https://learndjango.com/tutorials/django-signup-tutorial
* tags https://github.com/jazzband/django-taggit
* profile pictures by https://de.freepik.com/vektoren-kostenlos/handgezeichnetes-flaches-profilsymbol_17539361.htm#query=profile%20picture&position=42&from_view=search&track=ais&uuid=594c74d8-53ba-48f7-9d10-3770ce010d32
* navbar https://www.flaticon.com/free-icon/menu-bar_8860952?term=navigation&page=1&position=42&origin=search&related_id=8860952
* django-image-uploader-widget https://pypi.org/project/django-image-uploader-widget/
* django unittests https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
* svg icons: https://www.svgrepo.com/svg/513800/add-square
* image resizing: https://github.com/matthewwithanm/django-imagekit
* follow and unfollow concept https://www.youtube.com/watch?v=vFWobmzLUII
* text in star https://stackoverflow.com/questions/45346098/content-number-inside-a-shape-symbol
* paginator https://dontrepeatyourself.org/post/django-pagination-with-class-based-view/