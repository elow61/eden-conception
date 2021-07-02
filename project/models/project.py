from django.db import models
from user.models import User


class ProjectManager(models.Manager):

    def add_member(self, email, project):
        user = User.objects.filter(email__contains=email)
        import pdb; pdb.set_trace();

        if not user.exists():
            return

        project.user_ids.add(user.get().id)
        return True


class Project(models.Model):

    name = models.CharField(max_length=120, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    user_ids = models.ManyToManyField(User, related_name='member')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    number_task = models.IntegerField(default=0)

    objects = models.Manager()
    objects_project = ProjectManager()

    @property
    def get_number_task(self):
        self.number_task = 0
        project_lists = self.list_set.all()
        for li in project_lists:
            self.number_task += li.task_set.all().count()

        return self.number_task

    def save(self, *args, **kwargs):
        self.number_task = self.get_number_task
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
