from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
  '''
  The createadmin command allows you to specify a user, password, and email for the admin superuser
  '''
  def add_arguments(self, parser):
    # Named (optional) arguments
    parser.add_argument(
        '--user',
        default='admin',
        help='Admin username',
    )
    parser.add_argument(
        '--email',
        default='',
        help='Admin email',
    )
    parser.add_argument(
        '--password',
        default='admin',
        help='Admin password',
    )


  def handle(self, *args, **options):
    if not get_user_model().objects.filter(username=options['user']).exists():
      get_user_model().objects.create_superuser(
        options['user'], options['email'], options['password'])
