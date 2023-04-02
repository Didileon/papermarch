from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory



def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'flatpages/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}',
        }
    )

    msq = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )

    msq.attach_alternative(html_content, 'text/html')
    msq.send()

#1
#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(sender, instance, **kwargs):
 #   print("I'm signal!!!")
  #  if kwargs['action'] == 'post_add':
   #     print("I'm ready!!!")
    #    categories = instance.postCategory.all()
     #   subscribers: list[str] = []


      #  for category in categories:
       #     subscribers += category.subscribers.all()
        #subscribers = [s.email for s in subscribers]

        #send_notifications(instance.preview(), instance.pk, instance.title, subscribers)



#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(sender, instance, **kwargs):
 #   print("I'm signal!!!")
  #  if kwargs['action'] == 'post_add':
   #     print("I'm ready!!!")

    #    categories = instance.postCategory.all()
     #   print(f'{categories = }')

      #  subscribers: list[str] = []
       # print(f'{subscribers = }')

        #for category in categories:
         #   subscribers += category.subscribers.all()

        #subscribers = [s.email for s in subscribers]
        #print(f'{subscribers = }')

    #send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


#2
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action']== 'post_add':
        categories = instance.postCategory.all()
        print(f'{categories = }')

        subscribers: list[str] = []
        print(f'{subscribers = }')

        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]
        print(f'{subscribers = }')

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)






#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(sender, instance, **kwargs):
 #   if kwargs['action'] == 'post_add':
        #categories = instance.postCategory.all()
        #subscribers: list[str] = []
        #for category in categories:
         #   subscribers += category.subscribers.all()

        #subscribers = [s.email for s in subscribers]

        #send_notifications(instance.preview(), instance.pk, instance.title, subscribers)