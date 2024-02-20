# Weaver

Weaver is Reddit style news site. Users can create Threads on diverse topics and sparking discussions. Each Thread functions as a dynamic structure where users can share insights, opinions, and reactions through comments. With the ability to upvote/downvote Threads and comments, users actively shape the narrative and show their support or dislike.

Behind the scenes, Weaver is powered by Python, using a Django web framework. The user interface is crafted using Boostrap CSS and JavaScript. Furthermore, Weaver is deployed on Heroku, a cloud platform as a service (PaaS).

You can check out the [live-site.](https://word-weave-eb35426ae0cb.herokuapp.com/)

![Mock Up](static/img/readme/mockup.png)

## Content

<!-- toc -->

- [Technologies Used](#technologies-used)
  * [Languages Used](#languages-used)
  * [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)
- [User Experience](#user-experience)
  * [Target Audience](#target-audience)
  * [User stories](#user-stories)
    + [Workflow](#workflow)
- [Design](#design)
  * [Wireframes](#wireframes)
    + [Timeline](#timeline)
    + [Profile](#profile)
- [Features](#features)
  * [Existing Features](#existing-features)
    + [User Account:](#user-account)
    + [Profile:](#profile)
    + [Threads, Comments, Votes:](#threads-comments-votes)
    + [Tags:](#tags)
    + [Global and Tag-based Timeline:](#global-and-tag-based-timeline)
  * [Features Left to Implement](#features-left-to-implement)
    + [Moderation:](#moderation)
    + [Dark Mode:](#dark-mode)
  * [Accessibility](#accessibility)
    + [Fonts](#fonts)
    + [Colors](#colors)
- [Testing](#testing)
    + [Lighthouse Test](#lighthouse-test)
    + [Jigsaw CSS Validator](#jigsaw-css-validator)
    + [W3C Validator](#w3c-validator)
    + [Accessibility](#accessibility-1)
  * [Manual Testing](#manual-testing)
  * [Automatic Testing](#automatic-testing)
  * [Unfixed Bugs](#unfixed-bugs)
  * [Fixed Bugs](#fixed-bugs)
    + [Cascading Deletes for Votes](#cascading-deletes-for-votes)
      - [The Situation:](#the-situation)
      - [The Problem:](#the-problem)
      - [The Solution:](#the-solution)
    + [Default Pictures get deleted](#default-pictures-get-deleted)
      - [The Situation:](#the-situation-1)
      - [The Problem:](#the-problem-1)
      - [The Solution:](#the-solution-1)
- [Deployment](#deployment)
  * [Local Development](#local-development)
    + [How to Clone](#how-to-clone)
    + [How to Fork](#how-to-fork)
  * [Deploy locally](#deploy-locally)
    + [Usage](#usage)
  * [Deployment Using Heroku](#deployment-using-heroku)
- [Credits](#credits)

<!-- tocstop -->

## Technologies Used

* GitHub – storage and deployment
* Sublime Text - Editor
* Heroku - Deployment
* Cloudflare R2 Storage - Cloud storage for non static images
* [Poetry](https://python-poetry.org/) - dependency management and packaging in Python

### Languages Used

Python, HTML/CSS, Java Script

### Frameworks, Libraries & Programs Used

* Git / Github
* Bootstrap
* [django-allauth](https://docs.allauth.org/en/latest/)
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
* [pillow Imaging Library](https://pypi.org/project/pillow/)
* [django-taggit](https://github.com/jazzband/django-taggit)
* [markdown2](https://pypi.org/project/django-markdown2/)
* [django-image-uploader-widget](https://pypi.org/project/django-image-uploader-widget/)
* django-storages and boto3, for r2 bucket storage
* [django-cleanup](https://github.com/un1t/django-cleanup)

## User Experience

### Target Audience

The target audience for Weaver includes creators, enthusiasts, and curious minds with a focus on engaging young and hip generations through its modern and vibrant design. These individuals are passionate about engaging in conversations on the platform or sharing ideas in the comment section. 

### User stories
Features in this project are structured through [user stories](https://github.com/DasUnicorn/WordWeave/issues?q=is%3Aissue).
Each User Story contains:
- **Dependencies:** This field indicates any external factors or requirements that need to be fulfilled before the user story can be implemented in a form of a list of other user stories.
- **Description Of Service Or Screen:** This field typically describes the specific service, feature, or screen that the user story relates to.
- **User Objective:** This field outlines the user's goal or objective. It should clearly state what the user wants to achieve or accomplish. The format follows: "As a user, I want to [action], so that [reason or benefit]."
- **Acceptance Criteria:** This field specifies the conditions or criteria that must be met for the user story to be considered complete. It helps define the boundaries and expectations for implementing the user story.

#### Workflow
In the development process, a Kanban board in form of a [github project](https://github.com/users/DasUnicorn/projects/2) is used to manage the tasks and track their progress. Initially, all issues are collected and placed in the backlog. During each iteration, a set number of issues are selected to be developed and assigned to the current milestone. These selected issues are then moved to the 'To Do' column on the Kanban board, indicating that they are ready to be worked on.

When working on the tasks begins, the status of the issues is updated to 'In Process'. This signifies that active development is underway. Once the development work is completed, the issues move to the 'Testing' column, where they undergo thorough testing to ensure the acceptions criterias are met.

If an issue passes testing successfully, it is considered 'Done' and is moved to the final column on the Kanban board.

If an issue encounters blockers or dependencies that prevent progress, it is moved to the 'Waiting' column. Here, it remains until the blockers are resolved, allowing work to resume.

Throughout its journey, from 'To Do' to 'Testing' and ultimately 'Done', detailed information including comments, Git commits, and testing results is added to each issue. This approach ensures transparency regarding the path and work undertaken for every issue.

![Kanban-Board](static/img/readme/kanban.png)

## Design
The design process began with the creation of [three concepts:](https://www.figma.com/file/kyb4eClnCRghZT5nCFtHZ7/Untitled?type=whiteboard&node-id=0%3A1&t=HesaSLC53DPFYpXK-1) a retro-inspired theme featuring nostalgic colors and forms, a modern and elegant approach with sleek lines and refined aesthetics, and a hip neon profile.

These concepts were presented to other people for feedback and evaluation. Their insights and preferences were carefully considered to for each design. After thorough deliberation, the trendy cool neon design was the favored choice. Its vibrant colors, dynamic elements, and modern flair resonated most strongly with the audience.

![screenshot trendy neon design idea](static/img/readme/neon-design.png)

### Wireframes

#### Timeline
**Desktop:** \
<img src="static/img/readme/timeline-desktop.png" alt="Wireframe Desktop Timeline" height=400px> \
**Mobile:** \
<img src="static/img/readme/timeline-mobile.png" alt="Wireframe Mobile Timeline" height=400px>

#### Profile
**Desktop:** \
<img src="static/img/readme/profile-desktop.png" alt="Wireframe Desktop profile" height=400px> \
**Mobile:** \
<img src="static/img/readme/profile-mobile.png" alt="Wireframe Mobile profile" height=400px>

## Features 

### Existing Features

#### Navigation Bar
The Navigation Bar guides the User througout the platform.

##### Visitors
People who haven't created a user account yet have the option to sign in. People with user accounts can use the login functionality.
<img src="static/img/readme/nav.png" alt="Navigation Bar"> \
<img src="static/img/readme/nav-mobile.png" alt="Navigation Bar on Mobile" height=200px>

##### Signed-In Users
For people that have signed in, the Navigation Bar gives the Users easy acces to their profile.
<img src="static/img/readme/nav-user.png" alt="Navigation Bar for Signed in Users">

##### Admins
Admins of the platform can reach the django admin panel easily through the Navigation bar.
<img src="static/img/readme/nav-admin.png" alt="Navigation Bar for Signed in Admins">

#### User Account:
The User Accounts in this project are managed by the AllAuth Django package.

##### User Sign up
Users can register on the page with a username, an optional email, and password. After registration all their information is stored in the database.
<img src="static/img/readme/sign-up.png" alt="Sign Up Form">

##### User Login
Registered users can log in to their accounts using their credentials.
<img src="static/img/readme/login.png" alt="Login Form">

##### User Logout
Logged-in users can log out of the site by clicking the logout link in the navigation bar. They have to confirm their decision.
<img src="static/img/readme/sign-out.png" alt="Sign out Confirmation">

##### change Password
Registered users can reset their password.
<img src="static/img/readme/change-password.png" alt="Change Password" height=400px>

##### Reset Password, through mail
If a user has entered a valid email adress, they can reset their password by mail with a verification link. This is especcilly usefull when the user has fergotten their password.
<img src="static/img/readme/reset.png" alt="Reset Password By Mail">

##### Delete User Account
Users have the option to delete their accounts, removing all associated content from the platform.

##### Access Settings
For easier acces to all option, settings are displayed on an additional page, making it easier for a user to find all possibile Account Options.\
<img src="static/img/readme/settings.png" alt="Settings" height=400px>

#### Profile:
Each User on the platform has a User Profile.

##### Profile Picture and Bio
Each user has a profile where they can set a profile picture and update their bio text.
After signing up the user starts with a default picture and default bio text.\
<img src="static/img/readme/personal-profile.png" alt="Profile" height=400px>
<img src="static/img/readme/update-profile.png" alt="Update Profile" height=400px> \
<img src="static/img/readme/default-profile.png" alt="Default User Profile">

##### User Content Display
The profile displays all threads/posts created by the user.
<img src="static/img/readme/your-threads.png" alt="Threadlist from Users Profile"> \
<img src="static/img/readme/profile-threads.png" alt="Threadlist from Users Profile">

##### Vote Collection
Users can collect votes on their posts, threads, and comments. The total number of votes collected across all content is shown on the profile for each user.\
<img src="static/img/readme/user-votes.png" alt="Vote from a Profile" height=200px>

#### Threads, Comments, Votes:
On this platform Users engage by writing Threads. Each Thread can be commented.
Threads, as well as comments can be up- and down voted by Users.

##### Create Threads
Logged-in users can create threads on the platform. Threads appear in the global timeline and can be commented on by other logged-in users.\
<img src="static/img/readme/write-thread.png" alt="Write Thread" height=400px>

##### Create Comments
Logged-in users can create comments on the platform. Comments appear below the thread they relate to.\
<img src="static/img/readme/leave-comment-form.png" alt="Comment Form" height=400px>

##### Upvote and Downvote
Users can upvote or downvote threads and comments to give and collect points on the platform.\
<img src="static/img/readme/vote.png" alt="Vote Option next to a Thread" height=200px>

##### Edit Threads
Logged-in users can edit their threads  on the platform.\
<img src="static/img/readme/edit-thread-buttons.png" alt="Edit and delete buttons" height=400px>

##### Edit Comments
Logged-in users can edit their comments on the platform.\
<img src="static/img/readme/edit-comment-button.png" alt="Edit, Delete buttons" height=400px>
<img src="static/img/readme/edit-comment.png" alt="Edit Comment" height=400px>

##### Delete Threads and Comments
Logged-in users can delete their threads and comments. Confirmation is asked before the deletion is executed.\
<img src="static/img/readme/delete-comment-confirm.png" alt="Delete Comment" height=400px>
<img src="static/img/readme/delete-thread-confirm.png" alt="Delete Thread" height=400px>

##### Change or Delete Votes
Logged-in users can delete or change their votes on threads and comments.
The current vote of each user is displayed with a yellow background behind the up or downvote icon. If the opposite icon is pressed, the vote changes, if the current vote is pressed again, it is removed.\
<img src="static/img/readme/vote.png" alt="Vote Option next to a Thread" height=200px>

#### Tags:
Each Thread can be created with tags. Tags can be followed by users to create personal timelines.

##### Tag Site
Each Tag has their own site, which desplayed all threads created with that tag.
<img src="static/img/readme/tag-site.png" alt="Tag Site">

##### Follow Tags
On Tag Sites, the user has the option to follow a tag by pressing the botton on top of the site.\
<img src="static/img/readme/follow-tag.png" alt="Follow Tag" height=400px>

##### Unfollow Tags
On Tag Sites, the user has an option to unfollow tags, if they follow them.\
<img src="static/img/readme/unfollow-tag.png" alt="Unfollow Tag" height=400px>

##### Overview over all tags you follow
By navigating through the profile setting, a logged-in User can get to a view that shows them all tags they are following. This gives them an easier place to remove them.\
<img src="static/img/readme/all-tags.png" alt="All Tags" height=400px>

#### Global and Tag-based Timeline:

##### Global Timeline
The global timeline is visible to all Users and Visitors, showcasing threads from across the platform.
<img src="static/img/readme/global.png" alt="Global Timeline">

##### Personalized Tag Timeline
Users can follow tags, and threads with these tags appear in their personalized tag-based timeline for a tailored browsing experience.
<img src="static/img/readme/tag-based.png" alt="Tag Based Timeline">

##### Pagination
For a better load time and usage with multiple threads, the timeline has a pagination feature.\
<img src="static/img/readme/pagination.png" alt="Pagination" width=600px>

#### Messages
Users get notified about changes on the platform through the django message system.\
<img src="static/img/readme/message.png" alt="All Tags" height=200px>

#### Django Admin Panel
Inside the Django Admin panel, Administrators have acces to the models of the django project.
<img src="static/img/readme/admin-panel.png" alt="All Tags">

#### Info Page
An information page let's intrested visitors know what Weaver is all about.
<img src="static/img/readme/info.png" alt="Info Page">

### Features Left to Implement

#### Moderation:

* Flagging Content: Users can flag content for review by moderators if it violates community guidelines or is inappropriate.
* Moderator Role: Trusted users can be assigned a moderator role to review flagged content and take appropriate action.
* Content Review: Flagged content is accessible in a separate moderation view where moderators can review it and decide whether to delete or take further action.

#### Dark Mode:

* Color Preferences: Users can choose their color preferences for the site, including the option to switch to a dark mode theme for better visibility in low-light environments or personal preference.

### Accessibility

#### Fonts
The font 'Permanent Marker' was chosen as the font for the logo as well as logo related statement text. It is legible, but also rough and gritty. Breaking the clean visual of the site.

'Alatsi' was chosen for the Headings and Roboto for the general text. Both are easily readable and clean in their optic.

#### Colors
The website's style and vibe are defined by its color scheme. Chosen to resemble a neon spectrum, these colors are selected to provide strong contrast when combined.

#001A23, #FFFFFF, #BAFF2A, #F52789, #FFFF33

![color scheme](static/img/readme/colors.png)

## Data

### Database schema
The Database was planned as the following:
<img src="static/img/readme/db-sketch.png" alt="Database Schema">
After realizing this project, the database structure is the following:
<img src="static/img/readme/db-scheme.png" alt="Current Database Schema">
* Current Database Schema, exported with django-extensions*

## Security

## Testing

#### Lighthouse Test
The Lighthouse Test results show excellent results:
<img src="static/img/readme/lighthouse.png" alt="Lichthouse test Results" width=600px>
<img src="static/img/readme/lighthouse-profile.png" alt="Lighthouse Test Results Profile" width=600px>

#### Jigsaw CSS Validator
The Jigsaw CSS Validator throws one error:
According to the test the Property *text-wrap: pretty* doesn't exist. In reality this is a [fairly new](https://developer.chrome.com/blog/css-text-wrap-pretty) css property. It is not yet implemented for all browser. *(see below)*
![Jigsaw Result](static/img/readme/css-test.png)
![Can I use, screenshot](static/img/readme/wrap-test.png)
*Screenshot From [caniuse.com](https://caniuse.com/?search=text-wrap%3Apretty)*

#### W3C Validator
The W3C HTML Validator shows no errors.
![HTML Check](static/img/readme/html-check.png)
![HTML Check](static/img/readme/html-check-profile.png)

#### Accessibility
The result of the WAVE Web Accessibility Evaluation Tool shows no Errors.
![Wave Check](static/img/readme/wave.png)
![Wave Check](static/img/readme/wave-profile.png)

#### PEP8

The [Pep8 CI](https://pep8ci.herokuapp.com/) Linter was used, returning the following results:

| App            | File      | CI Linter Result                                                                          |
|----------------|-----------|-------------------------------------------------------------------------------------------|
| authentication | forms.py  | All clear, no errors found                                                                |
|                | models.py | All clear, no errors found                                                                |
|                | urls.py   | All clear, no errors found                                                                |
|                | views.py  | All clear, no errors found                                                                |
| follow         | models.py | 16:  E501 line too long (80 > 79 characters)                                              |
|                | urls.py   | All clear, no errors found                                                                |
|                | views.py  | 21:  E501 line too long (93 > 79 characters) 25:  E501 line too long (89 > 79 characters) |
| weave_manager  | forms.py  | All clear, no errors found                                                                |
|                | models.py | All clear, no errors found                                                                |
|                | urls.py   | All clear, no errors found                                                                |
|                | views.py  | All clear, no errors found                                                                |


### Manual Testing

### Automatic Testing
Unittests

### Unfixed Bugs

### Fixed Bugs
#### Cascading Deletes for Votes
##### The Situation:
When a user deletes their profile, all threads, comments and votes the user has made on the platform should get deleted with it. 
The current set up is as followed:

```

class Thread(models.Model):
    (...)

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

##### The Problem:
After Deleting a User, their votes (as instances of the Vote Model) get deleted, but the value "votes" of the Thread itselfs is never. Since the Votes for each thread is are the Thread.values that get displayed. The Votes in the website are never updated.

##### The Solution:
The goal is to create a function within the ThreadVote Model that updates the value of the associated thread whenever a ThreadVote is deleted.

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

The issue arose because, contrary to expectations, an overwritten delete function is not utilized for cascading deletes. Following the recommendation in the Django Docs to use pre_delete resolved the issue effectively.

```
@receiver(pre_delete, sender=ThreadVote)
def update_thread_votes(sender, instance, **kwargs):
    if instance.value == 1:
        instance.thread.votes = F('votes') - 1
    elif instance.value == -1:
        instance.thread.votes = F('votes') + 1
    instance.thread.save()
```
#### Default Pictures get deleted
##### The Situation:
After signing up the user recieves a default profile picture.
The moment any user changes their profile picture, it is gone for everyone.

##### The Problem:
With the storage of pictures in the cloud bucket, it was implemented that the old picture was deleted the moment one of the users deletes their profile picture by chooseing a new one, the default image gets deleted from the bucket.

##### The Solution:
To solve this problem the default picture was removed as a concept from the model and instead implemented in form of a fallback inside the template itself.
The default profile picture is now safely stored inside the static files and can not be deleted by users.

**Before:**
```
<div class="pt-5 d-flex md-rows align-items-center w-100 max-w-75">
    <img src="{{ user.profile_pic.url }}" alt="Profile Picture" class="profile-pic bg-light rounded-circle">
    <div class="bg-light text-dark w-75 p-2 m-3 text-center">
        <h1>{{ user.username }}</h1>
        <p>{{ user.bio }}</p>
    </div>
</div>
```

**After:**
```
<div class="pt-5 d-flex md-rows align-items-center w-100 max-w-75">
    {% if user.profile_pic %}
    <img src="{{ user.profile_pic.url }}" alt="Profile Picture" class="profile-pic bg-light rounded-circle">
    {% else %}
    <img src="{% static 'img/default.png' %}" alt="Profile Picture" class="profile-pic bg-light rounded-circle">
    {% endif %}
    <div class="bg-light text-dark w-75 p-2 m-3 text-center">
        <h1>{{ user.username }}</h1>
        <p>{{ user.bio }}</p>
    </div>
</div>
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

### Deploy locally

Install poetry.
To install the  dependencies for this project, run:
```
poetry install
```

To navigate the project, use the django-admin is Django’s command-line utility for administrative tasks. This [django docs](https://docs.djangoproject.com/en/5.0/ref/django-admin/) outlines all it can do.

#### Usage
django commands follow the following pattern:

```
$ django-admin <command> [options]
$ manage.py <command> [options]
$ python -m django <command> [options]
```

**Development**

```
python manage.py runserver
```
Starts a lightweight development web server on the local machine.

### Deployment Using Heroku

1. Register for an account on Heroku or sign in.
2. Create a new app.
3. Name your App.
5. Connect your github repository to Heroku app.
6. Create a Live Database by adding the postgreSQL add-on.
7. Create a Cloudfare Account and set up a R2 Bucket.
8. Create and Set up an email account for verification mails.
9. Set Config Vars for your cloudfare bucket (*AWS_S3_SECRET_ACCESS_KEY*), database (*DATABASE_URL*) and email(*EMAIL_HOST_PASSWORD*).
10. Deploy from "deploy", or choose an automatic deploy option.

## Credits
* Markdown Table of Content by [Jon Schlinkert](https://github.com/jonschlinkert/markdown-toc)
* The user story structure was used from the [Atlassian Archive](https://community.atlassian.com/t5/Jira-Content-Archive-questions/Default-Description-Text-on-Create/qaq-p/2359579)
* The Tags in this project are provided by [django-taggit](https://github.com/jazzband/django-taggit)
* The default profile picture is by [freepik](https://de.freepik.com/vektoren-kostenlos/handgezeichnetes-flaches-profilsymbol_17539361.htm#query=profile%20picture&position=42&from_view=search&track=ais&uuid=594c74d8-53ba-48f7-9d10-3770ce010d32)
* The navbar icon is from [flaticon](https://www.flaticon.com/free-icon/menu-bar_8860952?term=navigation&page=1&position=42&origin=search&related_id=8860952)
* The [django-image-uploader-widget](https://pypi.org/project/django-image-uploader-widget/) was used for the profile image
* [DrawSQL](https://drawsql.app/) was used to create the database sketch and [django-extensions](https://django-extensions.readthedocs.io/en/latest/graph_models.html) for the final export. 
* I learned a lot about django unittests from 
[The Dumbfounds](https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2)
* All svg icons come from [svgrepo](https://www.svgrepo.com/svg/513800/add-square)
* Avatar Images are free images from [freepik](https://www.freepik.com/free-vector/hand-drawn-people-avatar-set_4077151.htm#from_view=detail_alsolike)
* This project uses image resizing by the [django imagekit](https://github.com/matthewwithanm/django-imagekit)
* [follow and unfollow concept](https://www.youtube.com/watch?v=vFWobmzLUII)
* django [pagination](https://dontrepeatyourself.org/post/django-pagination-with-class-based-view/)
* The markdown in threads get handled with [markdown2](https://pypi.org/project/django-markdown2/)
* Set Up R2 Bucket from [djangotherightway](https://djangotherightway.com/using-cloudflare-r2-with-django-for-storage)